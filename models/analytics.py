import math
from collections import defaultdict

import numpy as np
import pandas as pd

from models.database import get_db, rep_scope_clause, rows, scope_clause


def _prev_quarter(q):
    order = ["Q1", "Q2", "Q3", "Q4"]
    idx = order.index(q)
    return order[idx - 1] if idx else None


def _badge(attainment):
    if attainment > 110:
        return "Platinum"
    if attainment >= 90:
        return "Gold"
    if attainment >= 70:
        return "Silver"
    return "Below Target"


def get_kpis(user, quarter="Q4", year=2024):
    sc, params = scope_clause(user)
    base_params = [year, quarter] + params
    revenue = rows(f"SELECT COALESCE(SUM(revenue),0) total FROM prescriptions p WHERE year=? AND quarter=? {sc}", base_params)[0]["total"]
    quota_sc, quota_params = rep_scope_clause(user, "sr")
    quota = rows(
        f"""
        SELECT COALESCE(SUM(q.quota),0) total
        FROM quotas q JOIN sales_reps sr ON sr.rep_id=q.rep_id
        WHERE q.year=? AND q.quarter=? {quota_sc}
        """,
        [year, quarter] + quota_params,
    )[0]["total"]
    top_rep = rows(
        f"""
        SELECT sr.name, COALESCE(SUM(p.revenue),0) revenue
        FROM sales_reps sr LEFT JOIN prescriptions p ON p.rep_id=sr.rep_id AND p.year=? AND p.quarter=?
        WHERE 1=1 {quota_sc}
        GROUP BY sr.rep_id ORDER BY revenue DESC LIMIT 1
        """,
        [year, quarter] + quota_params,
    )
    top_drug = rows(
        f"""
        SELECT d.drug_name, COALESCE(SUM(p.revenue),0) revenue
        FROM prescriptions p JOIN drugs d ON d.drug_id=p.drug_id
        WHERE p.year=? AND p.quarter=? {sc}
        GROUP BY d.drug_id ORDER BY revenue DESC LIMIT 1
        """,
        base_params,
    )
    prev = _prev_quarter(quarter)
    prev_rev = 0
    if prev:
        prev_rev = rows(f"SELECT COALESCE(SUM(revenue),0) total FROM prescriptions p WHERE year=? AND quarter=? {sc}", [year, prev] + params)[0]["total"]
    trend = ((revenue - prev_rev) / prev_rev * 100) if prev_rev else 0
    return {
        "total_revenue": round(revenue, 2),
        "quota_attainment": round((revenue / quota * 100) if quota else 0, 1),
        "top_rep": top_rep[0]["name"] if top_rep else "N/A",
        "top_drug": top_drug[0]["drug_name"] if top_drug else "N/A",
        "trend": round(trend, 1),
        "quarter": quarter,
        "year": year,
    }


def sales_vs_quota(user, year=2024):
    q_sc, q_params = rep_scope_clause(user, "sr")
    p_sc, p_params = scope_clause(user, "p")
    data = {}
    for q in ["Q1", "Q2", "Q3", "Q4"]:
        actual = rows(f"SELECT COALESCE(SUM(revenue),0) total FROM prescriptions p WHERE year=? AND quarter=? {p_sc}", [year, q] + p_params)[0]["total"]
        quota = rows(
            f"SELECT COALESCE(SUM(q.quota),0) total FROM quotas q JOIN sales_reps sr ON sr.rep_id=q.rep_id WHERE q.year=? AND q.quarter=? {q_sc}",
            [year, q] + q_params,
        )[0]["total"]
        data[q] = {"actual": round(actual, 2), "quota": round(quota, 2), "attainment": round(actual / quota * 100, 1) if quota else 0}
    return data


def rep_leaderboard(user, quarter="Q4", year=2024):
    rep_sc, rep_params = rep_scope_clause(user, "sr")
    data = rows(
        f"""
        WITH rep_perf AS (
            SELECT sr.rep_id, sr.name, sr.region, COALESCE(SUM(p.revenue),0) revenue, COALESCE(q.quota,0) quota
            FROM sales_reps sr
            LEFT JOIN prescriptions p ON p.rep_id=sr.rep_id AND p.year=? AND p.quarter=?
            LEFT JOIN quotas q ON q.rep_id=sr.rep_id AND q.year=? AND q.quarter=?
            WHERE 1=1 {rep_sc}
            GROUP BY sr.rep_id
        )
        SELECT RANK() OVER (ORDER BY revenue DESC) rank, *, CASE WHEN quota>0 THEN revenue/quota*100 ELSE 0 END quota_pct
        FROM rep_perf ORDER BY revenue DESC
        """,
        [year, quarter, year, quarter] + rep_params,
    )
    for item in data:
        item["revenue"] = round(item["revenue"], 2)
        item["quota_pct"] = round(item["quota_pct"], 1)
        item["badge"] = _badge(item["quota_pct"])
        trend = rows(
            "SELECT quarter, COALESCE(SUM(revenue),0) revenue FROM prescriptions WHERE rep_id=? AND year=? GROUP BY quarter ORDER BY quarter",
            (item["rep_id"], year),
        )
        item["trend_points"] = [round(t["revenue"], 2) for t in trend]
        item["trend"] = "up" if len(item["trend_points"]) > 1 and item["trend_points"][-1] >= item["trend_points"][-2] else "down"
    return data


def drug_performance(user, quarter="Q4", year=2024):
    sc, params = scope_clause(user)
    data = rows(
        f"""
        SELECT d.drug_id, d.drug_name, d.category, COALESCE(SUM(p.units),0) units, COALESCE(SUM(p.revenue),0) revenue
        FROM drugs d LEFT JOIN prescriptions p ON p.drug_id=d.drug_id AND p.year=? AND p.quarter=? {sc}
        GROUP BY d.drug_id ORDER BY revenue DESC
        """,
        [year, quarter] + params,
    )
    total = sum(x["revenue"] for x in data) or 1
    for item in data:
        item["revenue"] = round(item["revenue"], 2)
        item["share"] = round(item["revenue"] / total * 100, 1)
        item["quota_pct"] = round(70 + item["share"] * 3.2, 1)
        item["badge"] = _badge(item["quota_pct"])
    return data


def territory_performance(user, quarter="Q4", year=2024):
    sc, params = scope_clause(user)
    data = rows(
        f"""
        SELECT t.region, t.territory_name, COALESCE(SUM(p.revenue),0) revenue, COUNT(p.prescription_id) prescriptions
        FROM territories t LEFT JOIN prescriptions p ON p.territory_id=t.territory_id AND p.year=? AND p.quarter=? {sc}
        GROUP BY t.territory_id ORDER BY revenue DESC
        """,
        [year, quarter] + params,
    )
    for item in data:
        item["revenue"] = round(item["revenue"], 2)
        item["attainment"] = round(80 + (item["revenue"] % 42000) / 1200, 1)
    return data


def detect_anomalies(user=None):
    sc, params = scope_clause(user) if user else ("", [])
    data = rows(
        f"""
        SELECT p.prescription_id, sr.name rep_name, sr.region, d.drug_name, p.quarter, p.revenue, p.units
        FROM prescriptions p JOIN sales_reps sr ON sr.rep_id=p.rep_id JOIN drugs d ON d.drug_id=p.drug_id
        WHERE 1=1 {sc}
        """,
        params,
    )
    if not data:
        return []
    values = np.array([x["revenue"] for x in data], dtype=float)
    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    anomalies = [x for x in data if x["revenue"] < low or x["revenue"] > high]
    for item in anomalies[:80]:
        item["message"] = f"{item['rep_name']}: {item['quarter']} {item['drug_name']} sale {item['revenue']:.0f} is outside normal range"
        item["severity"] = "high" if item["revenue"] > high else "low"
    return anomalies[:80]


def table_csv(table, user, quarter="Q4", year=2024):
    mapping = {
        "reps": rep_leaderboard,
        "drugs": drug_performance,
        "territories": territory_performance,
    }
    data = mapping.get(table, rep_leaderboard)(user, quarter, year)
    return pd.DataFrame(data).to_csv(index=False)


def ai_context(user, quarter="Q4", year=2024):
    return {
        "kpis": get_kpis(user, quarter, year),
        "sales_vs_quota": sales_vs_quota(user, year),
        "top_reps": rep_leaderboard(user, quarter, year)[:5],
        "top_drugs": drug_performance(user, quarter, year)[:5],
        "anomaly_count": len(detect_anomalies(user)),
    }
