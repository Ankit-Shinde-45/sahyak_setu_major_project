# Sahayak Setu — AI Government Scheme Assistant (Flask edition)

A rewrite of the original single-file HTML/JS prototype into a proper Python
web application using **Flask**. This version moves eligibility logic, scheme
data, translations, and rendering onto the server; the browser JavaScript is
reduced to voice glue only (speech-to-text, text-to-speech, and a handful of
`fetch()` calls).

## Why this is less code, not just different code

| | Old (single HTML file) | New (Flask) |
|---|---|---|
| Eligibility rules | 27 separate hand-written JS boolean functions | 1 generic rule interpreter (`eligibility.py`, ~45 lines) reading declarative JSON rules |
| Scheme cards | 3 separate JS functions building the same HTML string (results / browse / saved) | 1 Jinja2 macro (`_scheme_card.html`) reused by all 3 pages |
| Citizen form | An 8-branch hand-written chat state machine (`askStep()`) | 1 Python list of field definitions (`fields.py`) looped over by a template |
| Data + translations | ~900 lines of JS object literals mixed into the same file as logic | Pure JSON data files, no code |
| Persistence | Browser artifact key-value storage, simulated client-side | Real SQLite database via Python's built-in `sqlite3` (no extra dependency) |
| Login/session | Hand-rolled JS auth simulation | Flask `session` + `werkzeug.security` password hashing |

Total hand-written code (`.py` + `.html` + `.css` + `.js`, **excluding** the
JSON data files, which are content, not logic) is about **1,300 lines**
across 19 small, single-purpose files, versus one ~1,700-line file that mixed
markup, styling, translations, scheme data, and application logic together.

## Folder structure

```
sahayak-flask/
├── app.py                  Flask routes (auth, citizen pages, admin pages, JSON APIs)
├── db.py                   sqlite3 data-access layer (no ORM needed)
├── eligibility.py          Generic declarative rule engine
├── fields.py                Citizen profile form field definitions
├── requirements.txt
├── data/
│   ├── schemes.json         27 schemes (15 central + 12 state), 4-language content + rule
│   ├── translations.json    UI strings in English/Hindi/Marathi/Tamil
│   ├── states.json
│   └── langs.json
├── templates/               Jinja2 HTML templates
│   ├── base.html            Shared layout, nav, language switch, theme toggle
│   ├── login.html
│   ├── assistant.html       Citizen voice-assisted profile form + results
│   ├── browse.html
│   ├── saved.html
│   ├── admin_schemes.html
│   ├── admin_citizens.html
│   ├── admin_analytics.html
│   └── _scheme_card.html    Shared macro for rendering one scheme card
└── static/
    ├── css/style.css
    └── js/app.js             Voice I/O + AJAX glue only (~200 lines)
```

## How to run it

This app needs both the Python packages **and** the Tesseract OCR program
itself (a separate system install, not something `pip` can provide).

**1. Install Tesseract OCR (system package, one-time):**
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS (Homebrew)
brew install tesseract

# Windows: download the installer from
# https://github.com/UB-Mannheim/tesseract/wiki and add it to your PATH
```

**"tesseract is not installed or it's not in your PATH"?**
The app now **searches your whole computer automatically** for Tesseract on
startup — you don't need to touch any code or edit PATH yourself. The only
thing that has to be true is that Tesseract is actually installed somewhere.
If you haven't installed it yet:
1. Go to https://github.com/UB-Mannheim/tesseract/wiki
2. Download the latest `tesseract-ocr-w64-setup-*.exe`
3. Run it and click through with the default options (no custom install
   location needed)
4. Restart the server: `python3 app.py`

The terminal will print one of these on startup, so you know immediately
whether it worked, without needing to test the upload feature first:
```
[ocr] Tesseract found (version 5.3.4) at: C:\Program Files\Tesseract-OCR\tesseract.exe
```
or
```
[ocr] WARNING: Tesseract OCR was NOT found anywhere on this computer.
```
If you see the warning after installing, the most likely cause is that the
install genuinely didn't finish — reopen the installer and run it again.

**2. Install Python dependencies and run:**
```bash
cd sahayak-flask
pip install -r requirements.txt
python3 app.py
```

Then open **http://localhost:5000** in **Google Chrome** (voice features need
the Web Speech API, which Chrome supports best).

If you don't want to install Tesseract, the app still runs fine — the
document-photo upload boxes just won't be able to read anything; everything
else (manual typing, voice fill, the By Documents checklist) works
independently of OCR.

The SQLite database (`sahayak.db`) is created automatically on first run,
seeded with a default admin account.

## Demo login

| Role    | Username | Password  |
|---------|----------|-----------|
| Admin   | admin    | Admin@123 |
| Citizen | *(sign up a new account from the login screen)* | |

## What changed in the user experience

The original version was a turn-by-turn voice **chat** (one question at a
time, spoken and typed). This version is a **single voice-assisted form**:
all questions are shown at once, each with its own 🎤 button, plus a
"Fill by voice" button that walks through every field automatically
(speaks the label, listens, fills it in, moves on, then submits the form
for you). This is a deliberate trade-off to make the server-side code
simpler and more maintainable — the Python side no longer needs to track
"which step is the user on," which was the single biggest source of
complexity in the old JavaScript version.

The **"Hey Sahayak" wake-word mode** still works the same way: say the wake
phrase, get a spoken "Yes? I'm listening," then either say a navigation
command ("browse schemes", "saved schemes", "log out") or just start
answering — it will run the same voice-fill walkthrough.

## "By Documents" — eligibility without knowing your category

A lot of people don't know which official category (BPL, income slab, etc.)
they fall into, but they *do* know what papers they're holding. The
**By Documents** tab lists every distinct document mentioned across all 27
schemes as a checkbox (Aadhaar card, ration card, land records, etc.) —
no photo or file upload, just names. Tick what you have, and the app shows
every scheme whose full document requirement is a subset of what you
ticked. It's a rough proxy (it ignores age/income/state), but it's a fast
way for someone unsure of their eligibility to see what's realistically
within reach.

## Clicking a scheme

Clicking a scheme's name (in results, Browse, Saved, or By Documents) opens
`/scheme/<id>`, which shows the full scheme card plus the **official
government page embedded directly on that screen** in an iframe, with an
"Open in a new tab" button right above it as a fallback. Many government
sites send security headers (`X-Frame-Options` / `Content-Security-Policy`)
that block being embedded this way — when that happens the box will appear
blank, which is expected browser security behavior, not a bug. The
new-tab button is the reliable option for those cases.

## Auto-fill from document photos (OCR)

On the assistant page, above the form, there's an optional "Auto-fill from
document photos" section with four upload boxes: Aadhaar card, PAN card,
income certificate, and marksheet/education certificate. Uploading a photo
sends it to `/api/ocr`, which runs it through **Tesseract OCR** (via
`pytesseract`) and applies regex heuristics per document type:

- **Income certificate** → looks for "annual/total/gross income" followed by
  a number, or any `₹`/`Rs`/`INR` amount, and fills the income field; also
  looks for the applicant's name (label-anchored) and a state name.
- **Marksheet** → looks for keywords ("12th"/"HSC", "Bachelor"/"B.A"/"B.Sc",
  "Master"/"post-graduate") and fills the education dropdown; also looks for
  name and state.
- **Aadhaar / PAN** → looks for a date-of-birth pattern and a
  12-digit Aadhaar number / 10-character PAN pattern, computes age from the
  DOB, and fills the age field. Also looks for a labelled name, gender
  ("Male"/"Female"), and any of the 12 known state names, filling the
  gender and state dropdowns directly. **Name has no matching profile
  field** (this app doesn't collect a name — only age/gender/etc.), so it's
  shown as a confirmation note next to the upload box instead ("name
  recognized as ...") rather than silently used anywhere.

This was tested with synthetically generated document images (clean,
printed text) and correctly extracted income, education, age, gender,
state, and name in every test — including at a "realistic phone photo"
difficulty level (rotated, blurred, slightly noisy). Name extraction only
trusts text that follows an explicit "Name:" (or "Name of ___:") label,
and trims off anything that looks like the next field's label if the OCR
engine ran two lines together (a real failure mode that showed up during
testing and was fixed before shipping) — deliberately conservative, since
guessing a name from unlabelled capitalized text is exactly the kind of
heuristic that produces confident-looking wrong answers.

### How extraction accuracy was improved

The first version just grayscaled the image and ran OCR once. That worked
on clean, computer-generated test images but **failed on anything resembling
a real phone photo** (slight rotation, blur, uneven lighting, image noise).
This was verified directly, not assumed: a set of synthetic "phone photo"
test images (rotated, blurred, low-res, noisy) was run through both the old
and new pipeline before and after this change.

What changed:
- **Multiple preprocessing passes** — each upload is tried as both a
  sharpened/contrast-boosted grayscale version and a binarized (pure
  black/white) version, since different document types respond better to
  different treatment.
- **Automatic upscaling** — small/low-res photos are scaled up before OCR,
  since Tesseract is tuned for ~300dpi and a photo taken from arm's length
  is usually far below that.
- **Multiple segmentation modes** — each preprocessed version is also tried
  with a few different Tesseract page-segmentation settings, since ID cards
  and printed certificates lay out text differently.
- **OCR-confusion-tolerant regex** — patterns for Aadhaar/PAN numbers now
  tolerate the handful of characters Tesseract most commonly confuses with
  digits (O/0, I or l/1) inside number-shaped matches specifically, without
  touching the rest of the text.
- **A confidence floor, and honesty about it** — every OCR attempt now
  reports Tesseract's own per-word confidence score. If nothing clears a
  minimum bar (~65%), the app **does not guess** — it tells the user the
  photo was too unclear to read reliably and asks them to retake it or type
  the field manually, rather than silently filling in something that might
  be wrong. This was a deliberate fix after testing showed the more
  aggressive extraction could otherwise produce a plausible-looking but
  *incorrect* number on a badly degraded image, which is worse than
  returning nothing.

Verified results across three difficulty levels (clean / realistic phone
photo / very degraded):

| Test image | Old pipeline | New pipeline |
|---|---|---|
| Clean, computer-generated | ✅ correct | ✅ correct |
| Realistic phone photo (rotated, blurred, noisy) | ❌ failed on all 3 documents | ✅ correct on all 3 |
| Badly degraded (heavy blur/noise/low-res) | ❌ empty (safe) | ✅ empty + explicit low-confidence flag (safe, no wrong guess) |


**Read this before demoing it on a real ID photo:**
- This is genuine OCR, not a fake/simulated feature — but it's also **not** a
  KYC or document-verification system. It does not check that a document is
  authentic, unaltered, or even the correct document type.
- Accuracy on real phone photos of ID cards will be noticeably worse than on
  clean printed text — lighting, glare, skew, low resolution, and the
  security-pattern backgrounds many Aadhaar/PAN cards have all hurt Tesseract's
  accuracy. Expect it to work best on decently lit, straight-on, high-resolution
  photos or scans.
- Every extracted value lands in a normal, still-editable form field — the
  citizen can and should check it before submitting. Nothing is auto-submitted
  from OCR alone.
- Uploaded images are processed in memory and **never saved to disk** —
  intentional, since Aadhaar/PAN photos are sensitive personal data and this
  is a demo, not a production KYC pipeline with the security/compliance work
  that would require.
- Requires the system package `tesseract-ocr` to be installed separately from
  the Python packages (see "How to run it" below) — `pip install` alone is
  not enough.

## Known limitations (worth mentioning in a report/viva)

- Flask's built-in development server (`app.run()`) is **not** meant for
  production. Deploying for real would use Gunicorn/uWSGI behind Nginx, or a
  platform like Render/Railway/PythonAnywhere.
- The Web Speech API is still browser-only and cloud-backed by Google —
  Python has no involvement in speech recognition/synthesis itself; it only
  receives the *already-transcribed* text via form submission or AJAX.
- Dark mode is intentionally **not persisted** across page loads in this
  version (kept in-memory only) to avoid adding cookies/localStorage code —
  a small, deliberate simplification versus the old version.
- `app.secret_key` is a hardcoded string — fine for a demo, but a real
  deployment should load it from an environment variable.
- SQLite is great for a single-user demo/project; a multi-user production
  deployment would move to PostgreSQL/MySQL.
