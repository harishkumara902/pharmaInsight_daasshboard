from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required

from models import lstm_forecast
from models.analytics import rep_leaderboard
from flask_login import current_user

forecast_bp = Blueprint("forecast", __name__)


@forecast_bp.route("/forecast")
@login_required
def forecast_page():
    return render_template("forecast.html", active="forecast")


@forecast_bp.route("/simulator")
@login_required
def simulator():
    return render_template("simulator.html", active="simulator")


@forecast_bp.route("/api/forecast")
@login_required
def api_forecast():
    return jsonify(lstm_forecast.forecast(int(request.args.get("drug_id", 1)), request.args.get("region", "South")))


@forecast_bp.route("/forecast/retrain", methods=["POST"])
@login_required
def retrain():
    return jsonify(lstm_forecast.retrain())


@forecast_bp.route("/api/simulator")
@login_required
def api_simulator():
    quota_adjustment = float(request.args.get("quota", 0))
    marketing = float(request.args.get("marketing", 0))
    reps = rep_leaderboard(current_user, request.args.get("quarter", "Q4"), 2024)
    before = [r["quota_pct"] for r in reps]
    after = [max(0, pct * (1 + marketing / 100 * 0.35) / (1 + quota_adjustment / 100)) for pct in before]
    return jsonify({"before": round(sum(before) / len(before), 1) if before else 0, "after": round(sum(after) / len(after), 1) if after else 0, "hit_target": sum(1 for x in after if x >= 100)})
