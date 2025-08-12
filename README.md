# Student Semester Registration App

A simple Flask web app that allows students to log in with their student ID and password, fill out a semester registration form, review a summary, and confirm their registration.

## Features
- Login with student ID and password
- Session-based auth with CSRF protection
- Registration form with validation (credit limits, required fields)
- Summary page to review and confirm
- Stores confirmed registrations in `data/registrations.json`

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The app runs at `http://127.0.0.1:8000`.

## Demo Credentials
- Student ID: `1001`  Password: `Passw0rd!`
- Student ID: `1002`  Password: `Test1234`

## Project Structure
```
app.py
requirements.txt
README.md
static/
  styles.css
templates/
  layout.html
  login.html
  register.html
  summary.html
data/
  courses.json
  registrations.json
```

## Notes
- This app is for demonstration and learning purposes.
- Secrets are hard-coded for ease of local running—replace with environment vars in production.
- CSRF protection is custom and minimal; in production use Flask-WTF.
