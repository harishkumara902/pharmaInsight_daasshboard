import os
from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from config import SECRET_KEY
from models.analytics import detect_anomalies
from models.database import get_user_by_email, get_user_by_id
from routes.chatbot import chatbot_bp
from routes.dashboard import dashboard_bp
from routes.drugs import drugs_bp
from routes.forecast import forecast_bp
from routes.reps import reps_bp
from routes.settings import init_settings_schema, settings_bp, update_last_login
from routes.territories import territories_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", SECRET_KEY)

init_settings_schema()

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@app.context_processor
def inject_user_context():
    anomalies = []
    if current_user.is_authenticated:
        anomalies = detect_anomalies(current_user)[:8]
    return {"anomalies": anomalies, "anomaly_count": len(anomalies)}

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = get_user_by_email(request.form.get("email", ""))
        if user and check_password_hash(user.password_hash, request.form.get("password", "")):
            login_user(user, remember=bool(request.form.get("remember")))
            update_last_login(user.user_id)
            return redirect(request.args.get("next") or url_for("dashboard.dashboard"))
        error = "Invalid email or password."
    return render_template("login.html", error=error, auth_page=True)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

app.register_blueprint(dashboard_bp)
app.register_blueprint(reps_bp)
app.register_blueprint(drugs_bp)
app.register_blueprint(territories_bp)
app.register_blueprint(forecast_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(settings_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
