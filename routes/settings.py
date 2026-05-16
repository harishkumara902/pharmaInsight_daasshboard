import base64
from email.message import EmailMessage
import os
import smtplib
import socket
from datetime import datetime

from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from config import DATABASE_PATH, GEMINI_API_KEY
from generate_data import seed as regenerate_seed_data
from models.database import get_db

settings_bp = Blueprint("settings", __name__)


USER_COLUMNS = {
    "phone": "TEXT",
    "job_title": "TEXT",
    "profile_photo": "TEXT",
    "status": "TEXT DEFAULT 'Active'",
    "last_login": "TEXT",
}

PREFERENCE_DEFAULTS = {
    "theme": "light",
    "accent_color": "#FF85BB",
    "font_size": "medium",
    "layout": "comfortable",
    "sidebar_collapsed": 0,
    "chart_animations": 1,
    "show_data_labels": 1,
    "chart_color_scheme": "navy-pink",
    "default_date_range": "current_quarter",
    "auto_refresh_interval": 0,
    "pdf_paper_size": "A4",
    "pdf_include_charts": 1,
    "pdf_include_insights": 1,
    "ai_model": "gemini-1.5-flash",
    "chatbot_personality": "professional",
    "forecast_horizon": 1,
    "forecast_model": "lstm",
    "confidence_interval": 90,
    "auto_insights": 1,
    "insight_count": 3,
    "anomaly_detection": 1,
    "anomaly_sensitivity": "medium",
    "quota_alert_threshold": 70,
    "notify_quota_alert": 1,
    "notify_anomaly": 1,
    "notify_new_rep": 1,
    "notify_monthly_report": 1,
    "notify_weekly_digest": 1,
    "notify_daily_kpi": 0,
    "notify_rep_underperformance": 1,
    "notification_frequency": "daily",
    "pdf_header_text": "PharmaInsight AI",
    "pdf_logo": "",
    "max_response_words": 180,
    "show_suggested_chips": 1,
    "insight_tone": "executive",
    "detection_method": "iqr",
    "email_smtp_host": "",
    "email_smtp_port": "",
    "email_smtp_user": "",
    "email_smtp_pass": "",
    "email_from_name": "",
    "email_from_email": "",
    "gemini_api_key": "",
    "updated_at": "",
}


def init_settings_schema():
    with get_db() as conn:
        existing = {row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
        for name, ddl in USER_COLUMNS.items():
            if name not in existing:
                conn.execute(f"ALTER TABLE users ADD COLUMN {name} {ddl}")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id INTEGER PRIMARY KEY,
                theme TEXT DEFAULT 'light',
                accent_color TEXT DEFAULT '#FF85BB',
                font_size TEXT DEFAULT 'medium',
                layout TEXT DEFAULT 'comfortable',
                sidebar_collapsed INTEGER DEFAULT 0,
                chart_animations INTEGER DEFAULT 1,
                show_data_labels INTEGER DEFAULT 1,
                chart_color_scheme TEXT DEFAULT 'navy-pink',
                default_date_range TEXT DEFAULT 'current_quarter',
                auto_refresh_interval INTEGER DEFAULT 0,
                pdf_paper_size TEXT DEFAULT 'A4',
                pdf_include_charts INTEGER DEFAULT 1,
                pdf_include_insights INTEGER DEFAULT 1,
                ai_model TEXT DEFAULT 'gemini-1.5-flash',
                chatbot_personality TEXT DEFAULT 'professional',
                forecast_horizon INTEGER DEFAULT 1,
                forecast_model TEXT DEFAULT 'lstm',
                confidence_interval INTEGER DEFAULT 90,
                auto_insights INTEGER DEFAULT 1,
                insight_count INTEGER DEFAULT 3,
                anomaly_detection INTEGER DEFAULT 1,
                anomaly_sensitivity TEXT DEFAULT 'medium',
                quota_alert_threshold INTEGER DEFAULT 70,
                notify_quota_alert INTEGER DEFAULT 1,
                notify_anomaly INTEGER DEFAULT 1,
                notify_new_rep INTEGER DEFAULT 1,
                notify_monthly_report INTEGER DEFAULT 1,
                notify_weekly_digest INTEGER DEFAULT 1,
                notify_daily_kpi INTEGER DEFAULT 0,
                notify_rep_underperformance INTEGER DEFAULT 1,
                notification_frequency TEXT DEFAULT 'daily',
                pdf_header_text TEXT DEFAULT 'PharmaInsight AI',
                pdf_logo TEXT,
                max_response_words INTEGER DEFAULT 180,
                show_suggested_chips INTEGER DEFAULT 1,
                insight_tone TEXT DEFAULT 'executive',
                detection_method TEXT DEFAULT 'iqr',
                email_smtp_host TEXT,
                email_smtp_port INTEGER,
                email_smtp_user TEXT,
                email_smtp_pass TEXT,
                email_from_name TEXT,
                email_from_email TEXT,
                gemini_api_key TEXT,
                updated_at TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
            """
        )
        # Add any columns missing from older local runs.
        existing_pref = {row["name"] for row in conn.execute("PRAGMA table_info(user_preferences)").fetchall()}
        for key, value in PREFERENCE_DEFAULTS.items():
            if key not in existing_pref and key != "updated_at":
                kind = "INTEGER" if isinstance(value, int) else "TEXT"
                conn.execute(f"ALTER TABLE user_preferences ADD COLUMN {key} {kind}")
        conn.commit()


def ensure_preferences(user_id):
    init_settings_schema()
    with get_db() as conn:
        pref = conn.execute("SELECT * FROM user_preferences WHERE user_id=?", (user_id,)).fetchone()
        if not pref:
            conn.execute(
                "INSERT INTO user_preferences(user_id, updated_at) VALUES (?, ?)",
                (user_id, datetime.utcnow().isoformat(timespec="seconds")),
            )
            conn.commit()
            pref = conn.execute("SELECT * FROM user_preferences WHERE user_id=?", (user_id,)).fetchone()
        return dict(pref)


def update_last_login(user_id):
    init_settings_schema()
    with get_db() as conn:
        conn.execute("UPDATE users SET last_login=? WHERE user_id=?", (datetime.utcnow().isoformat(timespec="seconds"), user_id))
        conn.commit()


def current_user_record():
    with get_db() as conn:
        return dict(conn.execute("SELECT * FROM users WHERE user_id=?", (current_user.user_id,)).fetchone())


def file_to_base64(file):
    if not file or not file.filename:
        return None
    encoded = base64.b64encode(file.read()).decode("ascii")
    return f"data:{file.mimetype};base64,{encoded}"


def save_preferences(payload):
    prefs = ensure_preferences(current_user.user_id)
    allowed = [key for key in PREFERENCE_DEFAULTS if key != "updated_at"]
    updates = {key: payload[key] for key in allowed if key in payload}
    if not updates:
        return prefs
    updates["updated_at"] = datetime.utcnow().isoformat(timespec="seconds")
    sets = ", ".join(f"{key}=?" for key in updates)
    with get_db() as conn:
        conn.execute(f"UPDATE user_preferences SET {sets} WHERE user_id=?", [*updates.values(), current_user.user_id])
        conn.commit()
    return ensure_preferences(current_user.user_id)


@settings_bp.route("/settings")
@login_required
def settings():
    init_settings_schema()
    prefs = ensure_preferences(current_user.user_id)
    with get_db() as conn:
        user = dict(conn.execute("SELECT * FROM users WHERE user_id=?", (current_user.user_id,)).fetchone())
        users = [dict(row) for row in conn.execute("SELECT user_id, name, email, role, region, status, profile_photo FROM users ORDER BY user_id").fetchall()]
        total_records = conn.execute("SELECT COUNT(*) c FROM prescriptions").fetchone()["c"]
    db_size = round(os.path.getsize(DATABASE_PATH) / (1024 * 1024), 2) if os.path.exists(DATABASE_PATH) else 0
    return render_template(
        "settings.html",
        active="settings",
        prefs=prefs,
        settings_user=user,
        users=users,
        total_records=total_records,
        db_size=db_size,
        last_generated=datetime.fromtimestamp(os.path.getmtime(DATABASE_PATH)).strftime("%d %b %Y, %I:%M %p") if os.path.exists(DATABASE_PATH) else "N/A",
    )


@settings_bp.route("/settings/profile", methods=["POST"])
@login_required
def profile():
    init_settings_schema()
    form = request.form
    email = current_user.email if current_user.role == "rep" else form.get("email", current_user.email)
    photo = file_to_base64(request.files.get("profile_photo"))
    with get_db() as conn:
        if photo:
            conn.execute(
                "UPDATE users SET name=?, email=?, phone=?, job_title=?, region=?, profile_photo=? WHERE user_id=?",
                (form.get("name"), email, form.get("phone"), form.get("job_title"), form.get("region"), photo, current_user.user_id),
            )
        else:
            conn.execute(
                "UPDATE users SET name=?, email=?, phone=?, job_title=?, region=? WHERE user_id=?",
                (form.get("name"), email, form.get("phone"), form.get("job_title"), form.get("region"), current_user.user_id),
            )
        conn.commit()
    return jsonify({"ok": True, "message": "Profile updated successfully"})


@settings_bp.route("/settings/password", methods=["POST"])
@login_required
def password():
    payload = request.get_json(force=True)
    user = current_user_record()
    new_password = payload.get("new_password", "")
    if not check_password_hash(user["password_hash"], payload.get("current_password", "")):
        return jsonify({"ok": False, "message": "Current password is incorrect"}), 400
    if len(new_password) < 8 or not any(c.isupper() for c in new_password) or not any(c.isdigit() for c in new_password):
        return jsonify({"ok": False, "message": "Password must be 8+ chars with 1 uppercase and 1 number"}), 400
    if new_password != payload.get("confirm_password"):
        return jsonify({"ok": False, "message": "Passwords do not match"}), 400
    with get_db() as conn:
        conn.execute("UPDATE users SET password_hash=? WHERE user_id=?", (generate_password_hash(new_password), current_user.user_id))
        conn.commit()
    return jsonify({"ok": True, "message": "Password updated successfully"})


@settings_bp.route("/settings/notifications", methods=["POST"])
@login_required
def notifications():
    return jsonify({"ok": True, "message": "Notification preferences saved", "preferences": save_preferences(request.get_json(force=True))})


@settings_bp.route("/settings/appearance", methods=["POST"])
@login_required
def appearance():
    return jsonify({"ok": True, "message": "Appearance preferences saved", "preferences": save_preferences(request.get_json(force=True))})


@settings_bp.route("/settings/charts", methods=["POST"])
@login_required
def charts():
    return jsonify({"ok": True, "message": "Chart preferences saved", "preferences": save_preferences(request.get_json(force=True))})


@settings_bp.route("/settings/export-config", methods=["POST"])
@login_required
def export_config():
    payload = dict(request.form) if request.form else request.get_json(force=True)
    logo = file_to_base64(request.files.get("pdf_logo")) if request.files else None
    if logo:
        payload["pdf_logo"] = logo
    return jsonify({"ok": True, "message": "Export settings saved", "preferences": save_preferences(payload)})


@settings_bp.route("/settings/ai-config", methods=["POST"])
@login_required
def ai_config():
    return jsonify({"ok": True, "message": "AI and ML settings saved", "preferences": save_preferences(request.get_json(force=True))})


@settings_bp.route("/settings/add-user", methods=["POST"])
@login_required
def add_user():
    if current_user.role != "admin":
        return jsonify({"ok": False, "message": "Admin access required"}), 403
    payload = request.get_json(force=True)
    with get_db() as conn:
        conn.execute(
            "INSERT INTO users(name, email, password_hash, role, region, status) VALUES (?, ?, ?, ?, ?, 'Active')",
            (payload["name"], payload["email"], generate_password_hash(payload["password"]), payload["role"], payload["region"]),
        )
        conn.commit()
    return jsonify({"ok": True, "message": "User added successfully"})


@settings_bp.route("/settings/remove-user", methods=["POST"])
@login_required
def remove_user():
    if current_user.role != "admin":
        return jsonify({"ok": False, "message": "Admin access required"}), 403
    user_id = int(request.get_json(force=True).get("user_id"))
    if user_id == current_user.user_id:
        return jsonify({"ok": False, "message": "You cannot remove your own account"}), 400
    with get_db() as conn:
        conn.execute("DELETE FROM user_preferences WHERE user_id=?", (user_id,))
        conn.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        conn.commit()
    return jsonify({"ok": True, "message": "User removed"})


@settings_bp.route("/settings/regenerate-data", methods=["POST"])
@login_required
def regenerate_data():
    if current_user.role != "admin":
        return jsonify({"ok": False, "message": "Admin access required"}), 403
    regenerate_seed_data()
    init_settings_schema()
    return jsonify({"ok": True, "message": "Synthetic data regenerated successfully"})


@settings_bp.route("/settings/test-gemini", methods=["GET", "POST"])
@login_required
def test_gemini():
    prefs = ensure_preferences(current_user.user_id)
    payload = request.get_json(silent=True) or {}
    key = payload.get("gemini_api_key") or prefs.get("gemini_api_key") or GEMINI_API_KEY
    model_name = payload.get("ai_model") or prefs.get("ai_model") or "gemini-1.5-flash"
    if not key or key == "your-key-here":
        return jsonify({"ok": False, "message": "Not Connected - add a Gemini API key"})
    try:
        import google.generativeai as genai

        genai.configure(api_key=key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Reply with exactly: connected")
        if "connected" not in (response.text or "").lower():
            return jsonify({"ok": False, "message": "Gemini responded unexpectedly"})
    except Exception as exc:
        return jsonify({"ok": False, "message": f"Not Connected - {str(exc)[:140]}"})
    return jsonify({"ok": True, "message": f"Connected - {model_name}"})


@settings_bp.route("/settings/test-smtp", methods=["POST"])
@login_required
def test_smtp():
    payload = request.get_json(force=True)
    required = ["email_smtp_host", "email_smtp_port", "email_smtp_user", "email_smtp_pass", "email_from_email"]
    missing = [field for field in required if not payload.get(field)]
    if missing:
        return jsonify({"ok": False, "message": f"Missing SMTP fields: {', '.join(missing)}"}), 400

    message = EmailMessage()
    message["Subject"] = "PharmaInsight AI SMTP Test"
    message["From"] = payload.get("email_from_email")
    message["To"] = current_user.email
    message.set_content("SMTP integration is connected for PharmaInsight AI.")

    try:
        port = int(payload.get("email_smtp_port"))
        with smtplib.SMTP(payload.get("email_smtp_host"), port, timeout=12) as smtp:
            smtp.ehlo()
            if port in (587, 25):
                smtp.starttls()
                smtp.ehlo()
            smtp.login(payload.get("email_smtp_user"), payload.get("email_smtp_pass"))
            smtp.send_message(message)
    except (OSError, smtplib.SMTPException, ValueError, socket.timeout) as exc:
        return jsonify({"ok": False, "message": f"SMTP test failed - {str(exc)[:140]}"})
    return jsonify({"ok": True, "message": f"SMTP connected - test email sent to {current_user.email}"})
