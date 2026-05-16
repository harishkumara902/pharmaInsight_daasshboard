import json

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from config import GEMINI_API_KEY
from models.analytics import ai_context

chatbot_bp = Blueprint("chatbot", __name__)

try:
    import google.generativeai as genai

    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
except Exception:
    gemini_model = None

SYSTEM_PROMPT = (
    "You are PharmaInsight AI. You have access to pharma sales data. "
    "Answer questions about reps, drugs, territories, forecasts. Be concise and data-driven."
)


def fallback_answer(message, ctx):
    text = message.lower()
    k = ctx["kpis"]
    if "top rep" in text:
        return f"Top rep is {k['top_rep']} for {k['quarter']} {k['year']}."
    if "best drug" in text or "top drug" in text:
        return f"Top drug is {k['top_drug']} with current total revenue of INR {k['total_revenue']:,.0f}."
    if "worst territory" in text:
        worst = sorted(ctx.get("top_reps", []), key=lambda r: r["quota_pct"])[0]
        return f"The weakest visible territory is {worst['region']} via {worst['name']} at {worst['quota_pct']}% quota."
    if "forecast" in text:
        return "Forecast is available on the Forecast page. Current trend suggests checking the drug-region forecast line for next-quarter revenue."
    return f"Current revenue is INR {k['total_revenue']:,.0f}, quota attainment is {k['quota_attainment']}%, top rep is {k['top_rep']}, and anomalies flagged: {ctx['anomaly_count']}."


@chatbot_bp.route("/api/chat", methods=["POST"])
@login_required
def chat():
    payload = request.get_json(force=True)
    message = payload.get("message", "")
    history = payload.get("history", [])
    ctx = ai_context(current_user, payload.get("quarter", "Q4"), int(payload.get("year", 2024)))
    if gemini_model and GEMINI_API_KEY != "your-key-here":
        prompt = f"{SYSTEM_PROMPT}\nContext JSON:\n{json.dumps(ctx, default=str)}\nHistory:\n{history}\nQuestion: {message}"
        try:
            return jsonify({"answer": gemini_model.generate_content(prompt).text})
        except Exception as exc:
            return jsonify({"answer": fallback_answer(message, ctx), "warning": str(exc)})
    return jsonify({"answer": fallback_answer(message, ctx)})


@chatbot_bp.route("/api/insights/generate", methods=["POST"])
@login_required
def insights():
    payload = request.get_json(silent=True) or {}
    ctx = ai_context(current_user, payload.get("quarter", "Q4"), int(payload.get("year", 2024)))
    k = ctx["kpis"]
    bullets = [
        f"Revenue is INR {k['total_revenue']:,.0f} with {k['quota_attainment']}% quota attainment.",
        f"{k['top_rep']} leads the visible sales cohort; prioritize playbook sharing this quarter.",
        f"{ctx['anomaly_count']} anomaly signals need review before executive reporting.",
    ]
    if gemini_model and GEMINI_API_KEY != "your-key-here":
        try:
            prompt = f"{SYSTEM_PROMPT}\nGenerate exactly 3 concise bullet insights from this JSON:\n{json.dumps(ctx, default=str)}"
            text = gemini_model.generate_content(prompt).text
            bullets = [line.strip("-• ").strip() for line in text.splitlines() if line.strip()][:3] or bullets
        except Exception:
            pass
    return jsonify({"insights": bullets})
