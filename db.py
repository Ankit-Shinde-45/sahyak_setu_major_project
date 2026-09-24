"""
Tiny data-access layer built on Python's built-in sqlite3 module.
No ORM dependency (SQLAlchemy) needed -- keeps the project lightweight.
"""
import sqlite3
import json
import time
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "sahayak.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('citizen','admin'))
    );

    CREATE TABLE IF NOT EXISTS profiles (
        user_id INTEGER PRIMARY KEY REFERENCES users(id),
        age INTEGER, gender TEXT, occupation TEXT, education TEXT,
        income INTEGER, state TEXT, other_info TEXT, category TEXT,
        updated_at TEXT
    );

    CREATE TABLE IF NOT EXISTS saved_schemes (
        user_id INTEGER REFERENCES users(id),
        scheme_id TEXT,
        PRIMARY KEY (user_id, scheme_id)
    );

    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(id),
        scheme_id TEXT,
        applied_at TEXT
    );

    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        sentiment TEXT,
        comment TEXT,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS custom_schemes (
        id TEXT PRIMARY KEY,
        scope TEXT, state TEXT, name TEXT, tag TEXT, description TEXT,
        benefits TEXT, documents TEXT, steps TEXT, link TEXT, rule TEXT
    );
    """)
    from werkzeug.security import generate_password_hash
    row = conn.execute("SELECT 1 FROM users WHERE role='admin' LIMIT 1").fetchone()
    if not row:
        conn.execute(
            "INSERT INTO users (username, password_hash, name, role) VALUES (?,?,?,?)",
            ("admin", generate_password_hash("Admin@123"), "Administrator", "admin"),
        )
    conn.commit()
    conn.close()


def get_user_by_username(username):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return row


def create_user(username, password_hash, name, role="citizen"):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO users (username, password_hash, name, role) VALUES (?,?,?,?)",
        (username, password_hash, name, role),
    )
    conn.commit()
    uid = cur.lastrowid
    conn.close()
    return uid


def list_citizens():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM users WHERE role='citizen' ORDER BY id").fetchall()
    conn.close()
    return rows


def save_profile(user_id, data):
    conn = get_conn()
    conn.execute("DELETE FROM profiles WHERE user_id=?", (user_id,))
    conn.execute(
        """INSERT INTO profiles (user_id, age, gender, occupation, education, income,
           state, other_info, category, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (user_id, data.get("age"), data.get("gender"), data.get("occupation"),
         data.get("education"), data.get("income"), data.get("state"),
         data.get("other_info"), data.get("category"), str(time.time())),
    )
    conn.commit()
    conn.close()


def get_profile(user_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM profiles WHERE user_id=?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def toggle_saved(user_id, scheme_id):
    conn = get_conn()
    row = conn.execute(
        "SELECT 1 FROM saved_schemes WHERE user_id=? AND scheme_id=?", (user_id, scheme_id)
    ).fetchone()
    if row:
        conn.execute("DELETE FROM saved_schemes WHERE user_id=? AND scheme_id=?", (user_id, scheme_id))
        saved = False
    else:
        conn.execute("INSERT INTO saved_schemes (user_id, scheme_id) VALUES (?,?)", (user_id, scheme_id))
        saved = True
    conn.commit()
    conn.close()
    return saved


def get_saved_ids(user_id):
    conn = get_conn()
    rows = conn.execute("SELECT scheme_id FROM saved_schemes WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    return [r["scheme_id"] for r in rows]


def add_application(user_id, scheme_id):
    conn = get_conn()
    conn.execute(
        "INSERT INTO applications (user_id, scheme_id, applied_at) VALUES (?,?,?)",
        (user_id, scheme_id, str(time.time())),
    )
    conn.commit()
    conn.close()


def get_applied_ids(user_id):
    conn = get_conn()
    rows = conn.execute("SELECT scheme_id FROM applications WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    return [r["scheme_id"] for r in rows]


def all_applications():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM applications").fetchall()
    conn.close()
    return rows


def add_feedback(user_id, sentiment, comment):
    conn = get_conn()
    conn.execute(
        "INSERT INTO feedback (user_id, sentiment, comment, created_at) VALUES (?,?,?,?)",
        (user_id, sentiment, comment, str(time.time())),
    )
    conn.commit()
    conn.close()


def all_feedback():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM feedback").fetchall()
    conn.close()
    return rows


def add_custom_scheme(scheme):
    conn = get_conn()
    conn.execute(
        """INSERT INTO custom_schemes (id, scope, state, name, tag, description,
           benefits, documents, steps, link, rule) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (scheme["id"], scheme["scope"], scheme.get("state"), scheme["name"], scheme["tag"],
         scheme["description"], json.dumps(scheme["benefits"]), json.dumps(scheme["documents"]),
         json.dumps(scheme["steps"]), scheme["link"], json.dumps(scheme["rule"])),
    )
    conn.commit()
    conn.close()


def delete_custom_scheme(scheme_id):
    conn = get_conn()
    conn.execute("DELETE FROM custom_schemes WHERE id=?", (scheme_id,))
    conn.commit()
    conn.close()


def list_custom_schemes():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM custom_schemes").fetchall()
    conn.close()
    out = []
    for r in rows:
        out.append({
            "id": r["id"], "scope": r["scope"], "state": r["state"],
            "rule": json.loads(r["rule"]), "custom": True,
            "t": {"en": {
                "name": r["name"], "tag": r["tag"], "desc": r["description"],
                "benefits": json.loads(r["benefits"]), "documents": json.loads(r["documents"]),
                "steps": json.loads(r["steps"]), "link": r["link"],
            }},
        })
    return out
