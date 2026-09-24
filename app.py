import json
import os
import functools
import time

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

import db
from eligibility import match_schemes
from fields import FIELDS
from ocr import process_document
import pytesseract

BASE_DIR = os.path.dirname(__file__)
app = Flask(__name__)
app.secret_key = "sahayak-setu-demo-secret-key"  # fine for a demo/college project only
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB per upload

with open(os.path.join(BASE_DIR, "data", "schemes.json"), encoding="utf-8") as f:
    SCHEMES = json.load(f)
with open(os.path.join(BASE_DIR, "data", "translations.json"), encoding="utf-8") as f:
    STR = json.load(f)
with open(os.path.join(BASE_DIR, "data", "states.json"), encoding="utf-8") as f:
    STATES = json.load(f)
with open(os.path.join(BASE_DIR, "data", "langs.json"), encoding="utf-8") as f:
    LANGS = json.load(f)
LANGS_CODES = [l["code"] for l in LANGS]

DYNAMIC = {
    "en": {"resultsFound": "I found {n} scheme{s} you may be eligible for:",
           "stateGovt": "State Government · {s}", "welcomeBack": "Welcome, {n}",
           "gotIt": "Got it — {v}.", "matchedCount": "{n} scheme{s} matched"},
    "hi": {"resultsFound": "मुझे {n} योजना{s} मिलीं जिनके आप पात्र हो सकते हैं:",
           "stateGovt": "राज्य सरकार · {s}", "welcomeBack": "स्वागत है, {n}",
           "gotIt": "समझ गया — {v}.", "matchedCount": "{n} योजना{s} मेल खाईं"},
    "mr": {"resultsFound": "मला तुमच्यासाठी {n} योजना सापडल्या ज्यासाठी तुम्ही पात्र असू शकता:",
           "stateGovt": "राज्य सरकार · {s}", "welcomeBack": "स्वागत आहे, {n}",
           "gotIt": "समजले — {v}.", "matchedCount": "{n} योजना जुळल्या"},
    "ta": {"resultsFound": "உங்களுக்கு தகுதி இருக்கக்கூடிய {n} திட்டங்களை கண்டறிந்தேன்:",
           "stateGovt": "மாநில அரசு · {s}", "welcomeBack": "வணக்கம், {n}",
           "gotIt": "புரிந்தது — {v}.", "matchedCount": "{n} திட்டங்கள் பொருந்தின"},
}


def t(key, **kw):
    lang = session.get("lang", "en")
    val = STR.get(lang, STR["en"]).get(key) or STR["en"].get(key, key)
    return val.format(**kw) if kw else val


def d(key, **kw):
    lang = session.get("lang", "en")
    tmpl = DYNAMIC.get(lang, DYNAMIC["en"])[key]
    return tmpl.format(**kw)


app.jinja_env.globals.update(t=t, d=d)


def all_schemes():
    return SCHEMES + db.list_custom_schemes()


def scheme_text(scheme):
    lang = session.get("lang", "en")
    return scheme["t"].get(lang) or scheme["t"]["en"]


def login_required(role=None):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*a, **kw):
            if "user_id" not in session:
                return redirect(url_for("login"))
            if role and session.get("role") != role:
                return redirect(url_for("login"))
            return fn(*a, **kw)
        return wrapper
    return deco


@app.route("/set_language/<lang>")
def set_language(lang):
    if lang in LANGS_CODES:
        session["lang"] = lang
    return redirect(request.referrer or url_for("login"))


@app.route("/", methods=["GET"])
def login():
    if "user_id" in session:
        return redirect(url_for("admin_dashboard") if session["role"] == "admin" else url_for("assistant"))
    session.setdefault("lang", "en")
    signup = request.args.get("signup") == "1"
    role = request.args.get("role", "citizen")
    return render_template("login.html", langs=LANGS, states=STATES, signup=signup, role=role)


@app.route("/login", methods=["POST"])
def do_login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    role = request.form.get("role", "citizen")
    user = db.get_user_by_username(username)
    if not user or user["role"] != role or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", langs=LANGS, states=STATES, error=t("invalidLogin"), role=role)
    session["user_id"] = user["id"]
    session["name"] = user["name"]
    session["role"] = user["role"]
    session["fresh_login"] = True
    return redirect(url_for("admin_dashboard") if role == "admin" else url_for("assistant"))


@app.route("/signup", methods=["POST"])
def do_signup():
    name = request.form.get("name", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    password2 = request.form.get("password2", "")
    if not (name and username and password):
        return render_template("login.html", langs=LANGS, states=STATES, error=t("fillAll"), signup=True)
    if password != password2:
        return render_template("login.html", langs=LANGS, states=STATES, error=t("passwordMismatch"), signup=True)
    if db.get_user_by_username(username):
        return render_template("login.html", langs=LANGS, states=STATES, error=t("userExists"), signup=True)
    uid = db.create_user(username, generate_password_hash(password), name, "citizen")
    session["user_id"] = uid
    session["name"] = name
    session["role"] = "citizen"
    session["fresh_login"] = True
    return redirect(url_for("assistant"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/assistant", methods=["GET"])
@login_required(role="citizen")
def assistant():
    profile = db.get_profile(session["user_id"])
    fresh = session.pop("fresh_login", False)
    matches = []
    if profile:
        matches = match_schemes(all_schemes(), profile)
    return render_template(
        "assistant.html", fields=FIELDS, states=STATES, langs=LANGS,
        profile=profile, matches=matches, scheme_text=scheme_text,
        saved_ids=db.get_saved_ids(session["user_id"]),
        applied_ids=db.get_applied_ids(session["user_id"]),
        fresh_login=fresh,
    )


@app.route("/assistant", methods=["POST"])
@login_required(role="citizen")
def submit_assistant():
    profile = {
        "age": int(request.form.get("age") or 0),
        "gender": request.form.get("gender"),
        "occupation": request.form.get("occupation"),
        "education": request.form.get("education"),
        "income": int(request.form.get("income") or 10**9),
        "state": request.form.get("state"),
        "other_info": request.form.get("other_info", ""),
        "category": request.form.get("category"),
    }
    db.save_profile(session["user_id"], profile)
    return redirect(url_for("assistant"))


def all_documents_for_lang(lang):
    """Every distinct document phrase used across all schemes, in the given language."""
    docs = set()
    for sc in all_schemes():
        txt = sc["t"].get(lang) or sc["t"]["en"]
        docs.update(txt["documents"])
    return sorted(docs)


@app.route("/documents", methods=["GET", "POST"])
@login_required(role="citizen")
def documents():
    lang = session.get("lang", "en")
    doc_list = all_documents_for_lang(lang)
    selected = []
    matches = None
    if request.method == "POST":
        selected = request.form.getlist("docs")
        selected_set = set(selected)
        matches = []
        for sc in all_schemes():
            txt = scheme_text(sc)
            required = set(txt["documents"])
            if required and required.issubset(selected_set):
                matches.append(sc)
    return render_template(
        "documents.html", doc_list=doc_list, selected=selected, matches=matches,
        scheme_text=scheme_text,
        saved_ids=db.get_saved_ids(session["user_id"]),
        applied_ids=db.get_applied_ids(session["user_id"]),
    )


@app.route("/scheme/<scheme_id>")
@login_required(role="citizen")
def scheme_detail(scheme_id):
    sc = next((s for s in all_schemes() if s["id"] == scheme_id), None)
    if not sc:
        return redirect(url_for("assistant"))
    return render_template(
        "scheme_detail.html", sc=sc, scheme_text=scheme_text,
        saved_ids=db.get_saved_ids(session["user_id"]),
        applied_ids=db.get_applied_ids(session["user_id"]),
    )


@app.route("/browse")
@login_required(role="citizen")
def browse():
    q = request.args.get("q", "").strip().lower()
    scope = request.args.get("scope", "all")
    state = request.args.get("state", "all")
    results = []
    for sc in all_schemes():
        if scope != "all" and sc["scope"] != scope:
            continue
        if state != "all" and sc.get("state") != state:
            continue
        txt = scheme_text(sc)
        if q and q not in (txt["name"] + " " + txt["tag"] + " " + txt["desc"]).lower():
            continue
        results.append(sc)
    return render_template(
        "browse.html", results=results, states=STATES, scheme_text=scheme_text,
        q=q, scope=scope, state=state,
        saved_ids=db.get_saved_ids(session["user_id"]), applied_ids=db.get_applied_ids(session["user_id"]),
    )


@app.route("/saved")
@login_required(role="citizen")
def saved():
    ids = db.get_saved_ids(session["user_id"])
    results = [sc for sc in all_schemes() if sc["id"] in ids]
    return render_template(
        "saved.html", results=results, scheme_text=scheme_text,
        saved_ids=ids, applied_ids=db.get_applied_ids(session["user_id"]),
    )


@app.route("/api/ocr", methods=["POST"])
@login_required(role="citizen")
def api_ocr():
    doc_type = request.form.get("doc_type", "")
    file = request.files.get("image")
    if not file or not file.filename:
        return jsonify({"error": "No image received."}), 400
    try:
        result = process_document(file, doc_type)
    except pytesseract.TesseractNotFoundError:
        return jsonify({
            "error": "Tesseract OCR isn't installed on this computer. Install it from "
                     "github.com/UB-Mannheim/tesseract/wiki (default options are fine), "
                     "then restart the server -- it will be found automatically, no other "
                     "setup needed."
        }), 400
    except Exception as e:
        return jsonify({"error": "Could not read that image: " + str(e)}), 400
    return jsonify(result)


@app.route("/api/toggle_save/<scheme_id>", methods=["POST"])
@login_required(role="citizen")
def api_toggle_save(scheme_id):
    is_saved = db.toggle_saved(session["user_id"], scheme_id)
    return jsonify({"saved": is_saved})


@app.route("/api/apply/<scheme_id>", methods=["POST"])
@login_required(role="citizen")
def api_apply(scheme_id):
    if scheme_id not in db.get_applied_ids(session["user_id"]):
        db.add_application(session["user_id"], scheme_id)
    return jsonify({"applied": True, "message": t("notifSent")})


@app.route("/api/feedback", methods=["POST"])
@login_required(role="citizen")
def api_feedback():
    data = request.get_json(force=True)
    db.add_feedback(session["user_id"], data.get("sentiment"), data.get("comment", ""))
    return jsonify({"ok": True})


@app.route("/admin")
@login_required(role="admin")
def admin_dashboard():
    return redirect(url_for("admin_schemes"))


@app.route("/admin/schemes")
@login_required(role="admin")
def admin_schemes():
    return render_template("admin_schemes.html", schemes=SCHEMES, custom=db.list_custom_schemes(), states=STATES)


@app.route("/admin/schemes/add", methods=["POST"])
@login_required(role="admin")
def admin_add_scheme():
    rule = {}
    if request.form.get("min_age"):
        rule["age_min"] = int(request.form["min_age"])
    if request.form.get("max_age"):
        rule["age_max"] = int(request.form["max_age"])
    if request.form.get("gender") and request.form["gender"] != "any":
        rule["gender"] = request.form["gender"]
    if request.form.get("max_income"):
        rule["income_max"] = int(request.form["max_income"])
    if request.form.get("occupation") and request.form["occupation"] != "any":
        rule["occupation"] = request.form["occupation"]
    if request.form.get("category") and request.form["category"] != "any":
        rule["category_in"] = [request.form["category"]]
    scope = request.form.get("scope", "central")
    if scope == "state" and request.form.get("state"):
        rule["state"] = request.form["state"]

    scheme = {
        "id": "custom_" + str(int(time.time() * 1000)),
        "scope": scope,
        "state": request.form.get("state") if scope == "state" else None,
        "name": request.form.get("name", "").strip(),
        "tag": request.form.get("tag", "").strip() or "General",
        "description": request.form.get("description", "").strip(),
        "benefits": [x.strip() for x in request.form.get("benefits", "").splitlines() if x.strip()],
        "documents": [x.strip() for x in request.form.get("documents", "").splitlines() if x.strip()],
        "steps": [x.strip() for x in request.form.get("steps", "").splitlines() if x.strip()],
        "link": request.form.get("link", "").strip() or "#",
        "rule": rule,
    }
    db.add_custom_scheme(scheme)
    return redirect(url_for("admin_schemes"))


@app.route("/admin/schemes/delete/<scheme_id>", methods=["POST"])
@login_required(role="admin")
def admin_delete_scheme(scheme_id):
    db.delete_custom_scheme(scheme_id)
    return redirect(url_for("admin_schemes"))


@app.route("/admin/citizens")
@login_required(role="admin")
def admin_citizens():
    citizens = db.list_citizens()
    rows = []
    for c in citizens:
        profile = db.get_profile(c["id"])
        matches = match_schemes(all_schemes(), profile) if profile else []
        rows.append({"user": c, "profile": profile, "match_count": len(matches)})
    return render_template("admin_citizens.html", rows=rows)


@app.route("/admin/analytics")
@login_required(role="admin")
def admin_analytics():
    citizens = db.list_citizens()
    apps = db.all_applications()
    fb = db.all_feedback()

    counts = {}
    for a in apps:
        counts[a["scheme_id"]] = counts.get(a["scheme_id"], 0) + 1
    top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:5]
    scheme_lookup = {s["id"]: scheme_text(s)["name"] for s in all_schemes()}
    top_rows = [(scheme_lookup.get(sid, sid), n) for sid, n in top]
    max_count = top_rows[0][1] if top_rows else 1

    positive = len([f for f in fb if f["sentiment"] == "up"])
    positive_pct = round(100 * positive / len(fb)) if fb else 0

    central_count = len([s for s in all_schemes() if s["scope"] == "central"])
    state_count = len([s for s in all_schemes() if s["scope"] == "state"])

    return render_template(
        "admin_analytics.html", total_citizens=len(citizens), total_apps=len(apps),
        total_feedback=len(fb), positive_pct=positive_pct, top_rows=top_rows,
        max_count=max_count, central_count=central_count, state_count=state_count,
        scope_max=max(central_count, state_count, 1),
    )


if __name__ == "__main__":
    db.init_db()
    app.run(debug=False, use_reloader=False, host="0.0.0.0", port=5000)
