import csv
import io

from flask import Blueprint, Response, jsonify, render_template, request, send_file
from flask_login import current_user, login_required
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from models.analytics import (
    ai_context,
    detect_anomalies,
    drug_performance,
    get_kpis,
    rep_leaderboard,
    sales_vs_quota,
    table_csv,
    territory_performance,
)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", active="dashboard")


@dashboard_bp.route("/api/data")
@login_required
def api_data():
    quarter = request.args.get("quarter", "Q4")
    year = int(request.args.get("year", 2024))
    return jsonify(
        {
            "kpis": get_kpis(current_user, quarter, year),
            "sales_vs_quota": sales_vs_quota(current_user, year),
            "reps": rep_leaderboard(current_user, quarter, year),
            "drugs": drug_performance(current_user, quarter, year),
            "territories": territory_performance(current_user, quarter, year),
            "anomalies": detect_anomalies(current_user),
        }
    )


@dashboard_bp.route("/api/kpis")
@login_required
def api_kpis():
    return jsonify(get_kpis(current_user, request.args.get("quarter", "Q4"), int(request.args.get("year", 2024))))


@dashboard_bp.route("/api/reps")
@login_required
def api_reps():
    return jsonify(rep_leaderboard(current_user, request.args.get("quarter", "Q4"), int(request.args.get("year", 2024))))


@dashboard_bp.route("/api/drugs")
@login_required
def api_drugs():
    return jsonify(drug_performance(current_user, request.args.get("quarter", "Q4"), int(request.args.get("year", 2024))))


@dashboard_bp.route("/api/territories")
@login_required
def api_territories():
    return jsonify(territory_performance(current_user, request.args.get("quarter", "Q4"), int(request.args.get("year", 2024))))


@dashboard_bp.route("/api/anomalies")
@login_required
def api_anomalies():
    return jsonify(detect_anomalies(current_user))


@dashboard_bp.route("/export/csv")
@login_required
def export_csv():
    table = request.args.get("table", "reps")
    quarter = request.args.get("quarter", "Q4")
    csv_data = table_csv(table, current_user, quarter, int(request.args.get("year", 2024)))
    return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition": f"attachment; filename={table}_{quarter}.csv"})


@dashboard_bp.route("/export/pdf")
@login_required
def export_pdf():
    quarter = request.args.get("quarter", "Q4")
    year = int(request.args.get("year", 2024))
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, title="PharmaInsight AI Report")
    styles = getSampleStyleSheet()
    story = []
    ctx = ai_context(current_user, quarter, year)
    navy = colors.HexColor("#021A54")
    pink = colors.HexColor("#FF85BB")
    story.append(Paragraph("PharmaInsight AI Sales Performance Report", styles["Title"]))
    story.append(Paragraph(f"{quarter} {year} | {current_user.name} ({current_user.role})", styles["Normal"]))
    story.append(Spacer(1, 16))
    k = ctx["kpis"]
    story.append(Table([["Total Revenue", "Quota Attainment", "Top Rep", "Top Drug"], [f"INR {k['total_revenue']:,.0f}", f"{k['quota_attainment']}%", k["top_rep"], k["top_drug"]]], style=[("BACKGROUND", (0, 0), (-1, 0), navy), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, pink)]))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Charts Summary", styles["Heading1"]))
    for q, item in ctx["sales_vs_quota"].items():
        story.append(Paragraph(f"{q}: Actual INR {item['actual']:,.0f} vs Quota INR {item['quota']:,.0f} ({item['attainment']}%)", styles["Normal"]))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Rep Leaderboard", styles["Heading1"]))
    reps = [["Rank", "Rep", "Region", "Revenue", "Quota %", "Badge"]] + [[r["rank"], r["name"], r["region"], f"INR {r['revenue']:,.0f}", r["quota_pct"], r["badge"]] for r in ctx["top_reps"]]
    story.append(Table(reps, repeatRows=1, style=[("BACKGROUND", (0, 0), (-1, 0), navy), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.35, colors.lightgrey)]))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Drug Performance", styles["Heading1"]))
    drugs = [["Drug", "Category", "Revenue", "Share"]] + [[d["drug_name"], d["category"], f"INR {d['revenue']:,.0f}", f"{d['share']}%"] for d in ctx["top_drugs"]]
    story.append(Table(drugs, repeatRows=1, style=[("BACKGROUND", (0, 0), (-1, 0), navy), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.35, colors.lightgrey)]))
    story.append(Spacer(1, 30))
    story.append(Paragraph("AI-Generated Insights Summary", styles["Heading1"]))
    story.append(Paragraph(f"Revenue trend is {k['trend']}%. {ctx['anomaly_count']} anomalies need review. Top growth focus: {k['top_drug']}.", styles["Normal"]))
    doc.build(story)
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name=f"pharmainsight_{quarter}_{year}.pdf", mimetype="application/pdf")
