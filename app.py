import json
import os
import re
import secrets
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
COURSES_FILE = DATA_DIR / "courses.json"
REGISTRATIONS_FILE = DATA_DIR / "registrations.json"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Initialize registration file if missing
if not REGISTRATIONS_FILE.exists():
    REGISTRATIONS_FILE.write_text(json.dumps({}, indent=2))

# Seed demo courses if missing
if not COURSES_FILE.exists():
    demo_courses = [
        {"id": "CS101", "title": "Intro to Computer Science", "credits": 3},
        {"id": "MATH201", "title": "Calculus II", "credits": 4},
        {"id": "ENG150", "title": "Academic Writing", "credits": 3},
        {"id": "HIST210", "title": "Modern World History", "credits": 3},
        {"id": "PHYS110", "title": "General Physics I", "credits": 4},
        {"id": "BIO120", "title": "Biology Basics", "credits": 3}
    ]
    COURSES_FILE.write_text(json.dumps(demo_courses, indent=2))


def load_courses():
    with open(COURSES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_registrations():
    with open(REGISTRATIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_registrations(registrations):
    with open(REGISTRATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(registrations, f, indent=2)


app = Flask(__name__)
# In production, set via environment variable
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-me")

# Demo user store with password hashes
RAW_USERS = {
    "1001": {"name": "Alex Johnson", "password": "Passw0rd!"},
    "1002": {"name": "Samira Patel", "password": "Test1234"},
}
USERS = {sid: {"name": u["name"], "password_hash": generate_password_hash(u["password"]) } for sid, u in RAW_USERS.items()}

# Simple CSRF
CSRF_SESSION_KEY = "csrf_token"


def ensure_csrf_token():
    if CSRF_SESSION_KEY not in session:
        session[CSRF_SESSION_KEY] = secrets.token_hex(16)
    return session[CSRF_SESSION_KEY]


def validate_csrf():
    token = session.get(CSRF_SESSION_KEY)
    form_token = request.form.get("csrf_token")
    if not token or not form_token or token != form_token:
        abort(400, description="Invalid CSRF token")


# Auth helpers

def login_required(view_func):
    from functools import wraps

    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("student_id"):
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped


def get_current_user():
    student_id = session.get("student_id")
    if not student_id:
        return None
    user = USERS.get(student_id)
    if not user:
        return None
    return {"student_id": student_id, "name": user["name"]}


@app.context_processor
def inject_globals():
    return {
        "current_user": get_current_user(),
        "csrf_token": ensure_csrf_token(),
    }


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        validate_csrf()
        student_id = request.form.get("student_id", "").strip()
        password = request.form.get("password", "")

        user = USERS.get(student_id)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid student ID or password.", "danger")
            return render_template("login.html", student_id=student_id), 401

        session.clear()
        session["student_id"] = student_id
        ensure_csrf_token()
        flash("Welcome back!", "success")
        return redirect(url_for("register"))

    return render_template("login.html")


@app.route("/logout", methods=["POST"]) 
def logout():
    validate_csrf()
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    courses = load_courses()

    # Load existing confirmed registration (for edit) or pending
    student_id = session["student_id"]
    registrations = load_registrations()
    confirmed = registrations.get(student_id)
    pending = session.get("pending_registration")

    if request.method == "POST":
        validate_csrf()
        # Gather form inputs
        full_name = request.form.get("full_name", "").strip()
        semester = request.form.get("semester", "").strip()
        program = request.form.get("program", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        schedule_pref = request.form.get("schedule_pref", "").strip()
        comments = request.form.get("comments", "").strip()
        selected_courses = request.form.getlist("courses")

        # Basic validation
        errors = []
        if not full_name:
            errors.append("Full name is required.")
        if not semester:
            errors.append("Semester is required.")
        if not program:
            errors.append("Program is required.")
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if email and not re.match(email_pattern, email):
            errors.append("Email format looks invalid.")
        phone_pattern = r"^[0-9+\-()\s]{7,}$"
        if phone and not re.match(phone_pattern, phone):
            errors.append("Phone format looks invalid.")
        if not selected_courses:
            errors.append("Select at least one course.")

        # Compute credits
        course_map = {c["id"]: c for c in courses}
        total_credits = sum(course_map[cid]["credits"] for cid in selected_courses if cid in course_map)
        if total_credits < 12:
            errors.append("Minimum credit load is 12.")
        if total_credits > 21:
            errors.append("Maximum credit load is 21.")

        if errors:
            for e in errors:
                flash(e, "danger")
            # Re-render with user's inputs
            form_values = {
                "full_name": full_name,
                "semester": semester,
                "program": program,
                "email": email,
                "phone": phone,
                "schedule_pref": schedule_pref,
                "comments": comments,
                "courses": selected_courses,
            }
            return render_template("register.html", courses=courses, form=form_values, confirmed=confirmed, total_credits=total_credits), 400

        # Save to session for summary step
        pending_registration = {
            "student_id": student_id,
            "full_name": full_name,
            "semester": semester,
            "program": program,
            "email": email,
            "phone": phone,
            "schedule_pref": schedule_pref,
            "comments": comments,
            "courses": selected_courses,
            "total_credits": total_credits,
            "updated_at": datetime.utcnow().isoformat() + "Z",
        }
        session["pending_registration"] = pending_registration
        return redirect(url_for("summary"))

    # GET: Pre-fill form values
    user = get_current_user()
    default_name = user["name"] if user else ""
    # Prioritize pending > confirmed > defaults
    form_values = {
        "full_name": pending.get("full_name") if pending else (confirmed.get("full_name") if confirmed else default_name),
        "semester": pending.get("semester") if pending else (confirmed.get("semester") if confirmed else ""),
        "program": pending.get("program") if pending else (confirmed.get("program") if confirmed else ""),
        "email": pending.get("email") if pending else (confirmed.get("email") if confirmed else ""),
        "phone": pending.get("phone") if pending else (confirmed.get("phone") if confirmed else ""),
        "schedule_pref": pending.get("schedule_pref") if pending else (confirmed.get("schedule_pref") if confirmed else ""),
        "comments": pending.get("comments") if pending else (confirmed.get("comments") if confirmed else ""),
        "courses": pending.get("courses") if pending else (confirmed.get("courses") if confirmed else []),
    }

    course_map = {c["id"]: c for c in courses}
    total_credits = sum(course_map[cid]["credits"] for cid in form_values["courses"] if cid in course_map)

    return render_template("register.html", courses=courses, form=form_values, confirmed=confirmed, total_credits=total_credits)


@app.route("/summary", methods=["GET", "POST"])
@login_required
def summary():
    pending = session.get("pending_registration")
    if not pending:
        flash("No registration in progress.", "warning")
        return redirect(url_for("register"))

    if request.method == "POST":
        validate_csrf()
        action = request.form.get("action")
        if action == "confirm":
            # Persist to file
            registrations = load_registrations()
            registrations[pending["student_id"]] = {
                **pending,
                "confirmed_at": datetime.utcnow().isoformat() + "Z",
            }
            save_registrations(registrations)
            session.pop("pending_registration", None)
            flash("Registration confirmed.", "success")
            return redirect(url_for("register"))
        elif action == "edit":
            flash("You can edit your registration.", "info")
            return redirect(url_for("register"))
        else:
            abort(400)

    # GET
    courses = load_courses()
    course_map = {c["id"]: c for c in courses}
    selected = [course_map[cid] for cid in pending["courses"] if cid in course_map]
    return render_template("summary.html", pending=pending, selected_courses=selected)


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def handle_errors(error):
    try:
        code = getattr(error, 'code', 500)
        message = getattr(error, 'description', str(error))
    except Exception:
        code = 500
        message = "An unexpected error occurred."
    return render_template("error.html", code=code, message=message), code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)