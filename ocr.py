"""
Best-effort OCR extraction from photographed documents (Aadhaar, PAN, income
certificate, marksheet). This is NOT a KYC/verification system -- it just
runs Tesseract OCR on the image and uses regex heuristics to guess a few
fields. Accuracy depends heavily on photo quality (lighting, angle, blur).
Every extracted value is meant to pre-fill a field the citizen can still
see and edit -- never trust it blindly.
"""
import io
import os
import re
import json
import shutil
import platform
from datetime import date

from PIL import Image, ImageOps, ImageFilter
import pytesseract

# Same state list the citizen profile dropdown uses -- loaded once so a
# document's state can be matched against exactly the values the form expects.
with open(os.path.join(os.path.dirname(__file__), "data", "states.json"), encoding="utf-8") as _f:
    KNOWN_STATES = [s for s in json.load(_f) if s != "Other"]

# ============================================================================
# TESSERACT AUTO-DETECTION
# ============================================================================
# Tesseract is a separate program pytesseract calls out to. Most people never
# add it to PATH manually, so this searches for it automatically -- no
# manual path-editing required. If you DO know the exact path and want to
# skip the search entirely, you can still paste it here:
MANUAL_TESSERACT_PATH = r"C:\Users\hp\Desktop\300000000000\tessercat OCR\tesseract.exe"   # optional, e.g. r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def _find_tesseract():
    if MANUAL_TESSERACT_PATH:
        return MANUAL_TESSERACT_PATH
    on_path = shutil.which("tesseract") or shutil.which("tesseract.exe")
    if on_path:
        return on_path
    if platform.system() != "Windows":
        return None

    exact_guesses = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Tesseract-OCR\tesseract.exe"),
    ]
    for path in exact_guesses:
        if os.path.isfile(path):
            return path

    # Nothing at the usual spots -- do a bounded search of the most likely
    # install roots (capped so it can't hang forever on a huge C: drive).
    search_roots = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        os.path.expandvars(r"%LOCALAPPDATA%"),
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "Downloads"),
        os.path.expanduser("~"),
    ]
    scanned = 0
    scan_limit = 60000
    for root in search_roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            depth = dirpath[len(root):].count(os.sep)
            if depth >= 5:
                dirnames[:] = []  # don't go deeper than 5 levels
            scanned += len(filenames)
            if "tesseract.exe" in filenames:
                return os.path.join(dirpath, "tesseract.exe")
            if scanned > scan_limit:
                break
        else:
            continue
        break
    return None


_found_path = _find_tesseract()
if _found_path:
    pytesseract.pytesseract.tesseract_cmd = _found_path


# Prints once when the server starts, so you can see immediately whether OCR
# is wired up correctly -- no need to upload a document just to find out.
try:
    _version = pytesseract.get_tesseract_version()
    print(f"[ocr] Tesseract found (version {_version}) at: {pytesseract.pytesseract.tesseract_cmd}")
except Exception as _e:
    print("=" * 70)
    print("[ocr] WARNING: Tesseract OCR was NOT found anywhere on this computer.")
    print("[ocr] Document photo upload will show an error until this is fixed.")
    print("[ocr] This means Tesseract itself isn't installed (not a code problem).")
    print("[ocr] Fix: install it from https://github.com/UB-Mannheim/tesseract/wiki")
    print("[ocr]      (just run the downloaded .exe, default options are fine),")
    print("[ocr]      then restart this server -- no other steps needed.")
    print(f"[ocr] Underlying error: {_e}")
    print("=" * 70)


AADHAAR_NUM_RE = re.compile(r"\b([\dOoIl]{4}\s?[\dOoIl]{4}\s?[\dOoIl]{4})\b")
PAN_RE = re.compile(r"\b([A-Z]{5}[\dOoIl]{4}[A-Z])\b")
DOB_LABEL_RE = re.compile(r"(?:dob|d\.?o\.?b\.?|date of birth|birth)[^0-9]{0,15}(\d{1,2}[/\-. ]\d{1,2}[/\-. ]\d{2,4})", re.IGNORECASE)
DOB_ANY_RE = re.compile(r"\b(\d{1,2})[/\-. ](\d{1,2})[/\-. ](\d{2,4})\b")
INCOME_LABEL_RE = re.compile(r"(?:annual|total|gross|family)\s+income[^\d₹]{0,20}(?:rs\.?|inr|₹)?\s?([\d,\s]{4,})", re.IGNORECASE)
INCOME_CURRENCY_RE = re.compile(r"(?:₹|rs\.?|inr)\s?([\d,\s]{4,})", re.IGNORECASE)

# Name: only trust it right after an explicit "Name" label -- guessing a name
# from unlabelled capitalized text is exactly the kind of low-confidence
# heuristic that produces plausible-looking wrong answers, so this is
# deliberately conservative rather than clever.
NAME_LABEL_RE = re.compile(
    r"[Nn][Aa][Mm][Ee]\s+[Oo][Ff]\s+\w+\s*[:\-]\s*([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3})"
    r"|(?<![a-zA-Z])[Nn][Aa][Mm][Ee]\s*[:\-]\s*([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3})"
)
GENDER_RE = re.compile(r"\b(male|female|transgender)\b", re.IGNORECASE)

EDU_PATTERNS = [
    (r"\bp\.?h\.?d\b|\bm\.?a\b|\bm\.?sc\b|\bm\.?com\b|post[\s-]?graduat|master'?s?\s+degree", "pg"),
    (r"\bb\.?a\b|\bb\.?sc\b|\bb\.?com\b|\bb\.?tech\b|\bb\.?e\b|graduat|bachelor'?s?\s+degree", "grad"),
    (r"\b12\s?th\b|\bhsc\b|higher secondary|\b10\s?th\b|\bssc\b|secondary school", "ten12"),
]


def _fix_digit_lookalikes(s):
    """Within a captured 'number-like' string, fix the handful of characters
    Tesseract most often confuses with digits (O/0, I or l/1). Only ever
    applied to small already-matched groups, never to the whole page, so it
    can't corrupt unrelated words."""
    return (s.replace("O", "0").replace("o", "0")
             .replace("I", "1").replace("l", "1")
             .replace(" ", ""))


def _preprocess_variants(img):
    """Produce a few different cleaned-up versions of the same image.
    Different documents (glossy ID card vs. plain printed certificate)
    respond better to different treatment, so we try more than one and
    let the parser pick whichever version actually yields a usable result."""
    img = ImageOps.exif_transpose(img)  # fix phone-photo rotation
    base = img.convert("L")

    # Upscale small photos -- Tesseract is tuned for ~300dpi scans, and a
    # photo taken from a couple feet away is usually far below that.
    w, h = base.size
    if max(w, h) < 1800:
        scale = 1800 / max(w, h)
        base = base.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    contrast = ImageOps.autocontrast(base, cutoff=1)
    sharp = contrast.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # Simple binarization (pure black/white) -- often the single biggest
    # accuracy win for photographed documents with uneven lighting.
    binarized = sharp.point(lambda p: 255 if p > 145 else 0)

    return [sharp, binarized]


def _ocr_with_confidence(img, psm):
    config = f"--psm {psm}"
    data = pytesseract.image_to_data(img, config=config, output_type=pytesseract.Output.DICT)
    text = " ".join(w for w in data["text"] if w.strip())
    confs = [int(c) for c in data["conf"] if str(c).lstrip("-").isdigit() and int(c) >= 0]
    mean_conf = sum(confs) / len(confs) if confs else 0
    return text, mean_conf


def extract_candidates(file_storage):
    """Run OCR across a few preprocessing/segmentation combinations and
    return every attempt (text + confidence), best first, so callers can
    try parsing each until one actually finds what it's looking for."""
    raw = file_storage.read()
    img = Image.open(io.BytesIO(raw))
    variants = _preprocess_variants(img)

    attempts = []
    for variant in variants:
        for psm in (6, 4, 3):  # 6=uniform block, 4=column, 3=fully automatic
            try:
                text, conf = _ocr_with_confidence(variant, psm)
            except Exception:
                continue
            if text.strip():
                attempts.append((conf, text))
    attempts.sort(key=lambda t: t[0], reverse=True)
    return attempts


def extract_text(file_storage):
    """Back-compat single-string helper (used by tests) -- just the best attempt."""
    attempts = extract_candidates(file_storage)
    return attempts[0][1] if attempts else ""


def _age_from_dob(day, month, year):
    if year < 100:
        year += 2000 if year < 30 else 1900
    try:
        dob = date(year, month, day)
    except ValueError:
        return None
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if 0 < age < 120:
        return age
    return None


def parse_common_dob(text):
    # Prefer a date that's explicitly labelled "DOB"/"Date of Birth" over
    # any random date on the page (issue dates, expiry dates, etc.).
    m = DOB_LABEL_RE.search(text)
    if m:
        parts = re.split(r"[/\-. ]", m.group(1))
    else:
        m2 = DOB_ANY_RE.search(text)
        if not m2:
            return None
        parts = [m2.group(1), m2.group(2), m2.group(3)]
    if len(parts) != 3:
        return None
    try:
        d, mo, y = int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        return None
    return _age_from_dob(d, mo, y)


NAME_LABEL_BLOCKLIST = {
    "dob", "state", "class", "address", "gender", "date", "aadhaar", "pan",
    "income", "board", "certificate", "marksheet", "of", "issue", "govt",
    "government", "india", "annual", "father", "mother", "husband", "wife",
    "son", "daughter", "age", "the", "district", "village", "pin", "code",
    "signature", "photo", "male", "female",
}


def parse_common_name(text):
    m = NAME_LABEL_RE.search(text)
    if not m:
        return None
    name = (m.group(1) or m.group(2) or "").strip()
    if not name:
        return None
    # The reconstructed OCR text has no reliable line breaks, so a greedy
    # multi-word capture can run on into the next field's label (e.g.
    # "Ramesh Kumar DOB"). Trim any trailing words that are actually labels.
    words = name.split()
    while words and words[-1].lower() in NAME_LABEL_BLOCKLIST:
        words.pop()
    if not words:
        return None
    return " ".join(words)


def parse_common_state(text):
    for state in KNOWN_STATES:
        if state.lower() in text.lower():
            return state
    return None


def parse_common_gender(text):
    m = GENDER_RE.search(text)
    if not m:
        return None
    word = m.group(1).lower()
    return "male" if word == "male" else ("female" if word == "female" else "other")


def parse_aadhaar(text):
    out = {}
    m = AADHAAR_NUM_RE.search(text)
    if m and len(_fix_digit_lookalikes(m.group(1))) == 12:
        out["aadhaar_number_found"] = True
    age = parse_common_dob(text)
    if age:
        out["age"] = age
    name = parse_common_name(text)
    if name:
        out["name"] = name
    gender = parse_common_gender(text)
    if gender:
        out["gender"] = gender
    state = parse_common_state(text)
    if state:
        out["state"] = state
    return out


def parse_pan(text):
    out = {}
    m = PAN_RE.search(text.upper())
    if m:
        out["pan_number_found"] = True
    age = parse_common_dob(text)
    if age:
        out["age"] = age
    name = parse_common_name(text)
    if name:
        out["name"] = name
    return out


def parse_income(text):
    out = {}
    m = INCOME_LABEL_RE.search(text) or INCOME_CURRENCY_RE.search(text)
    if m:
        digits = _fix_digit_lookalikes(m.group(1)).replace(",", "")
        try:
            income = int(digits)
            if 1000 < income < 10**8:
                out["income"] = income
        except ValueError:
            pass
    name = parse_common_name(text)
    if name:
        out["name"] = name
    state = parse_common_state(text)
    if state:
        out["state"] = state
    return out


def parse_marksheet(text):
    out = {}
    lower = text.lower()
    for pattern, code in EDU_PATTERNS:
        if re.search(pattern, lower):
            out["education"] = code
            break
    name = parse_common_name(text)
    if name:
        out["name"] = name
    state = parse_common_state(text)
    if state:
        out["state"] = state
    return out


PARSERS = {
    "aadhaar": parse_aadhaar,
    "pan": parse_pan,
    "income": parse_income,
    "marksheet": parse_marksheet,
}


MIN_CONFIDENCE_FOR_FIELDS = 65  # below this, OCR is too unreliable to trust for auto-fill


def process_document(file_storage, doc_type):
    attempts = extract_candidates(file_storage)
    parser = PARSERS.get(doc_type)

    if not attempts:
        return {"fields": {}, "raw_text_preview": "", "low_confidence": True}

    best_text = attempts[0][1]
    best_conf = attempts[0][0]
    fields = {}
    low_confidence = True

    if parser:
        # Try every OCR attempt (best-confidence first), but only ever trust
        # a parsed result if that specific attempt cleared the confidence
        # floor -- a lucky regex match on garbled/noisy text is worse than
        # no match at all, since a wrong auto-filled value looks trustworthy.
        for conf, text in attempts:
            if conf < MIN_CONFIDENCE_FOR_FIELDS:
                continue
            result = parser(text)
            if result:
                fields = result
                best_text = text
                low_confidence = False
                break

    return {
        "fields": fields,
        "raw_text_preview": best_text.strip()[:600],
        "low_confidence": low_confidence,
        "confidence": round(best_conf, 1),
    }

