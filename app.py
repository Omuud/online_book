from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any

from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from passlib.hash import pbkdf2_sha256

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length


DATABASE_PATH = Path(__file__).parent / "app.db"


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-change-me"  # In production, load from env
    app.config["DATABASE"] = str(DATABASE_PATH)

    @app.before_request
    def open_db_connection() -> None:
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])  # type: ignore[attr-defined]
            g.db.row_factory = sqlite3.Row  # type: ignore[attr-defined]

    @app.teardown_appcontext
    def close_db_connection(exception: Optional[BaseException]) -> None:
        db = g.pop("db", None)
        if db is not None:
            db.close()

    with app.app_context():
        initialize_database()
        seed_demo_users()

    register_routes(app)
    return app


@dataclass
class User:
    id: int
    student_id: str
    password_hash: str
    full_name: str


@dataclass
class Registration:
    id: int
    user_id: int
    semester: str
    program: str
    year_level: str
    courses_csv: str
    notes: str
    status: str  # draft, submitted


class LoginForm(FlaskForm):
    student_id = StringField("Student ID", validators=[DataRequired(), Length(min=3, max=32)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=128)])
    submit = SubmitField("Sign in")


class RegistrationForm(FlaskForm):
    semester = SelectField(
        "Semester",
        choices=[
            ("Fall 2025", "Fall 2025"),
            ("Spring 2026", "Spring 2026"),
            ("Summer 2026", "Summer 2026"),
        ],
        validators=[DataRequired()],
    )
    program = SelectField(
        "Program",
        choices=[
            ("BSc Computer Science", "BSc Computer Science"),
            ("BEng Software Engineering", "BEng Software Engineering"),
            ("BA Mathematics", "BA Mathematics"),
        ],
        validators=[DataRequired()],
    )
    year_level = SelectField(
        "Year Level",
        choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4")],
        validators=[DataRequired()],
    )
    courses_csv = StringField(
        "Courses (comma separated course codes)", validators=[DataRequired(), Length(min=3, max=256)]
    )
    notes = TextAreaField("Notes (optional)")
    submit = SubmitField("Review")


# Database helpers

def get_db() -> sqlite3.Connection:
    return g.db  # type: ignore[attr-defined]


def initialize_database() -> None:
    db = sqlite3.connect(str(DATABASE_PATH))
    cur = db.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            semester TEXT NOT NULL,
            program TEXT NOT NULL,
            year_level TEXT NOT NULL,
            courses_csv TEXT NOT NULL,
            notes TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'draft',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """
    )
    db.commit()
    db.close()


def seed_demo_users() -> None:
    db = sqlite3.connect(str(DATABASE_PATH))
    cur = db.cursor()
    # Only seed if table is empty
    cur.execute("SELECT COUNT(*) FROM users")
    (count,) = cur.fetchone() or (0,)
    if count == 0:
        demo_users = [
            ("S1001", pbkdf2_sha256.hash("password123"), "Alex Johnson"),
            ("S1002", pbkdf2_sha256.hash("secret456"), "Priya Singh"),
        ]
        cur.executemany(
            "INSERT INTO users (student_id, password_hash, full_name) VALUES (?, ?, ?)", demo_users
        )
        db.commit()
    db.close()


# Auth helpers

def authenticate(student_id: str, password: str) -> Optional[User]:
    db = get_db()
    cur = db.execute("SELECT id, student_id, password_hash, full_name FROM users WHERE student_id = ?", (student_id,))
    row = cur.fetchone()
    if row and pbkdf2_sha256.verify(password, row["password_hash"]):
        return User(id=row["id"], student_id=row["student_id"], password_hash=row["password_hash"], full_name=row["full_name"])  # type: ignore[index]
    return None


# Routes

def login_required(view_func):
    from functools import wraps

    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please sign in to continue.", "warning")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped


def register_routes(app: Flask) -> None:
    @app.route("/", methods=["GET", "POST"])
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if session.get("user_id"):
            return redirect(url_for("register"))

        form = LoginForm()
        if form.validate_on_submit():
            user = authenticate(form.student_id.data.strip(), form.password.data)
            if user:
                session["user_id"] = user.id
                session["student_id"] = user.student_id
                session["full_name"] = user.full_name
                flash(f"Welcome, {user.full_name.split()[0]}!", "success")
                return redirect(url_for("register"))
            flash("Invalid student ID or password.", "danger")
        return render_template("login.html", form=form)

    @app.route("/register", methods=["GET", "POST"])
    @login_required
    def register():
        form = RegistrationForm()
        # Preload existing draft if present
        existing = fetch_latest_registration(session["user_id"], status="draft")
        if request.method == "GET" and existing:
            form.semester.data = existing["semester"]
            form.program.data = existing["program"]
            form.year_level.data = existing["year_level"]
            form.courses_csv.data = existing["courses_csv"]
            form.notes.data = existing["notes"]

        if form.validate_on_submit():
            # store in session temporarily for summary view
            session["reg_form"] = {
                "semester": form.semester.data,
                "program": form.program.data,
                "year_level": form.year_level.data,
                "courses_csv": form.courses_csv.data,
                "notes": form.notes.data or "",
            }
            return redirect(url_for("summary"))

        return render_template("register.html", form=form)

    @app.route("/summary", methods=["GET", "POST"])
    @login_required
    def summary():
        form_data: Optional[Dict[str, Any]] = session.get("reg_form")
        if not form_data:
            flash("No registration details to review.", "warning")
            return redirect(url_for("register"))

        if request.method == "POST":
            if request.form.get("action") == "edit":
                flash("You can now edit your registration.", "info")
                return redirect(url_for("register"))

            # Save as submitted
            save_registration(
                user_id=session["user_id"],
                semester=form_data["semester"],
                program=form_data["program"],
                year_level=form_data["year_level"],
                courses_csv=form_data["courses_csv"],
                notes=form_data.get("notes", ""),
                status="submitted",
            )
            session.pop("reg_form", None)
            flash("Registration submitted successfully!", "success")
            return redirect(url_for("dashboard"))

        return render_template("summary.html", form=form_data)

    @app.route("/dashboard")
    @login_required
    def dashboard():
        user_id = session["user_id"]
        recent = fetch_recent_registrations(user_id)
        return render_template("dashboard.html", recent=recent)

    @app.route("/logout")
    def logout():
        session.clear()
        flash("You have been signed out.", "info")
        return redirect(url_for("login"))


# Data operations

def save_registration(
    user_id: int,
    semester: str,
    program: str,
    year_level: str,
    courses_csv: str,
    notes: str,
    status: str = "draft",
) -> int:
    db = get_db()
    db.execute(
        """
        INSERT INTO registrations (user_id, semester, program, year_level, courses_csv, notes, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, semester, program, year_level, courses_csv.strip(), notes.strip(), status),
    )
    db.commit()
    cur = db.execute("SELECT last_insert_rowid()")
    (new_id,) = cur.fetchone()
    return int(new_id)


def fetch_latest_registration(user_id: int, status: Optional[str] = None) -> Optional[sqlite3.Row]:
    db = get_db()
    if status:
        cur = db.execute(
            """
            SELECT * FROM registrations
            WHERE user_id = ? AND status = ?
            ORDER BY updated_at DESC, id DESC LIMIT 1
            """,
            (user_id, status),
        )
    else:
        cur = db.execute(
            "SELECT * FROM registrations WHERE user_id = ? ORDER BY updated_at DESC, id DESC LIMIT 1",
            (user_id,),
        )
    row = cur.fetchone()
    return row


def fetch_recent_registrations(user_id: int, limit: int = 5) -> list[sqlite3.Row]:
    db = get_db()
    cur = db.execute(
        "SELECT * FROM registrations WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit),
    )
    return cur.fetchall()


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)