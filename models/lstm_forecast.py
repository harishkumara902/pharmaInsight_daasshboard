import math

import numpy as np

from models.database import rows


def _series(drug_id=1, region="South"):
    data = rows(
        """
        SELECT p.quarter, COALESCE(SUM(p.revenue),0) revenue
        FROM prescriptions p
        JOIN sales_reps sr ON sr.rep_id=p.rep_id
        WHERE p.drug_id=? AND sr.region=?
        GROUP BY p.quarter ORDER BY p.quarter
        """,
        (drug_id, region),
    )
    labels = [d["quarter"] for d in data]
    values = [float(d["revenue"]) for d in data]
    return labels, values


def forecast(drug_id=1, region="South"):
    labels, values = _series(drug_id, region)
    if not values:
        values = [0, 0, 0, 0]
        labels = ["Q1", "Q2", "Q3", "Q4"]

    x = np.arange(len(values))
    y = np.array(values, dtype=float)
    if len(values) > 1:
        coef = np.polyfit(x, y, 1)
        pred = float(np.polyval(coef, len(values)))
        fitted = np.polyval(coef, x)
    else:
        pred = y[-1]
        fitted = y
    pred = max(pred, 0)
    mae = float(np.mean(np.abs(y - fitted))) if len(y) else 0
    rmse = float(math.sqrt(np.mean((y - fitted) ** 2))) if len(y) else 0
    ss_res = float(np.sum((y - fitted) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2)) or 1
    r2 = 1 - ss_res / ss_tot
    return {
        "labels": labels + ["Next Q"],
        "actual": [round(v, 2) for v in values] + [None],
        "forecast": [None] * max(0, len(values) - 1) + [round(values[-1], 2), round(pred, 2)],
        "confidence_low": round(pred * 0.85, 2),
        "confidence_high": round(pred * 1.15, 2),
        "metrics": {"mae": round(mae, 2), "rmse": round(rmse, 2), "r2": round(r2, 3)},
    }


def retrain():
    result = forecast()
    result["status"] = "Model refreshed with latest prescription history"
    return result
