import os
import random
import sqlite3
from datetime import date, timedelta

import numpy as np
from faker import Faker
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "pharmainsight.db")

fake = Faker("en_IN")
random.seed(42)
np.random.seed(42)

REGIONS = ["North", "South", "East", "West", "Central"]
DRUGS = [
    ("Cardiomax", "Cardiology", 210.0),
    ("Neurocil", "Neurology", 180.0),
    ("Oncora", "Oncology", 320.0),
    ("Glucozen", "Diabetes", 150.0),
    ("Respira", "Respiratory", 135.0),
    ("Dermasol", "Dermatology", 95.0),
    ("Immunex", "Immunology", 285.0),
    ("Painex", "Analgesic", 75.0),
    ("Renova", "Nephrology", 240.0),
    ("Gastrofit", "Gastroenterology", 125.0),
]
QUARTERS = {
    "Q1": (date(2024, 1, 1), date(2024, 3, 31), 0.92),
    "Q2": (date(2024, 4, 1), date(2024, 6, 30), 1.05),
    "Q3": (date(2024, 7, 1), date(2024, 9, 30), 0.98),
    "Q4": (date(2024, 10, 1), date(2024, 12, 31), 1.18),
}


def connect():
    return sqlite3.connect(DB_PATH)


def reset_schema(cur):
    cur.executescript(
        """
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS prescriptions;
        DROP TABLE IF EXISTS quotas;
        DROP TABLE IF EXISTS doctors;
        DROP TABLE IF EXISTS drugs;
        DROP TABLE IF EXISTS sales_reps;
        DROP TABLE IF EXISTS territories;

        CREATE TABLE territories (
            territory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT NOT NULL,
            territory_name TEXT NOT NULL,
            market_potential REAL NOT NULL
        );

        CREATE TABLE sales_reps (
            rep_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            region TEXT NOT NULL,
            territory_id INTEGER NOT NULL,
            hire_date TEXT NOT NULL,
            FOREIGN KEY (territory_id) REFERENCES territories(territory_id)
        );

        CREATE TABLE drugs (
            drug_id INTEGER PRIMARY KEY AUTOINCREMENT,
            drug_name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit_price REAL NOT NULL
        );

        CREATE TABLE doctors (
            doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            region TEXT NOT NULL,
            potential_score REAL NOT NULL
        );

        CREATE TABLE prescriptions (
            prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            rep_id INTEGER NOT NULL,
            drug_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            territory_id INTEGER NOT NULL,
            prescription_date TEXT NOT NULL,
            year INTEGER NOT NULL,
            quarter TEXT NOT NULL,
            units INTEGER NOT NULL,
            revenue REAL NOT NULL,
            FOREIGN KEY (rep_id) REFERENCES sales_reps(rep_id),
            FOREIGN KEY (drug_id) REFERENCES drugs(drug_id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
            FOREIGN KEY (territory_id) REFERENCES territories(territory_id)
        );

        CREATE TABLE quotas (
            quota_id INTEGER PRIMARY KEY AUTOINCREMENT,
            rep_id INTEGER NOT NULL,
            year INTEGER NOT NULL,
            quarter TEXT NOT NULL,
            quota REAL NOT NULL,
            FOREIGN KEY (rep_id) REFERENCES sales_reps(rep_id)
        );

        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin','manager','rep')),
            rep_id INTEGER,
            region TEXT,
            FOREIGN KEY (rep_id) REFERENCES sales_reps(rep_id)
        );
        """
    )


def random_day(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


def seed():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = connect()
    cur = conn.cursor()
    reset_schema(cur)

    territory_ids = {}
    for region in REGIONS:
        cur.execute(
            "INSERT INTO territories(region, territory_name, market_potential) VALUES (?, ?, ?)",
            (region, f"{region} Metro", round(float(np.random.uniform(0.82, 1.28)), 2)),
        )
        territory_ids[region] = cur.lastrowid

    for name, category, price in DRUGS:
        cur.execute(
            "INSERT INTO drugs(drug_name, category, unit_price) VALUES (?, ?, ?)",
            (name, category, price),
        )

    specialties = [d[1] for d in DRUGS]
    for _ in range(160):
        region = random.choice(REGIONS)
        cur.execute(
            "INSERT INTO doctors(name, specialty, region, potential_score) VALUES (?, ?, ?, ?)",
            (f"Dr. {fake.name()}", random.choice(specialties), region, round(float(np.random.uniform(0.65, 1.45)), 2)),
        )

    rep_ids = []
    for idx in range(20):
        region = REGIONS[idx % len(REGIONS)]
        name = fake.name()
        cur.execute(
            "INSERT INTO sales_reps(name, email, region, territory_id, hire_date) VALUES (?, ?, ?, ?, ?)",
            (name, f"rep{idx + 1}@pharma.com", region, territory_ids[region], fake.date_between(start_date="-6y", end_date="-6m").isoformat()),
        )
        rep_ids.append((cur.lastrowid, region))

    # Quotas vary by rep, quarter, and regional market potential.
    for rep_id, region in rep_ids:
        rep_factor = float(np.random.uniform(0.86, 1.2))
        for q, (_, _, season) in QUARTERS.items():
            quota = 62000 * season * rep_factor * float(np.random.uniform(0.92, 1.1))
            cur.execute(
                "INSERT INTO quotas(rep_id, year, quarter, quota) VALUES (?, 2024, ?, ?)",
                (rep_id, q, round(quota, 2)),
            )

    cur.execute("SELECT doctor_id, region, potential_score FROM doctors")
    doctors = cur.fetchall()
    cur.execute("SELECT drug_id, unit_price FROM drugs")
    drugs = cur.fetchall()

    rows = []
    for q, (start, end, season) in QUARTERS.items():
        for _ in range(560):
            rep_id, rep_region = random.choice(rep_ids)
            regional_doctors = [d for d in doctors if d[1] == rep_region]
            doctor_id, _, potential = random.choice(regional_doctors)
            drug_id, price = random.choice(drugs)
            demand = np.random.poisson(lam=18 * season * potential)
            units = int(max(2, demand + np.random.randint(-4, 7)))
            if random.random() < 0.016:
                units = int(units * random.choice([0.25, 2.8]))
            revenue = round(units * price * float(np.random.uniform(0.92, 1.08)), 2)
            rows.append((rep_id, drug_id, doctor_id, territory_ids[rep_region], random_day(start, end).isoformat(), 2024, q, units, revenue))

    cur.executemany(
        """
        INSERT INTO prescriptions(rep_id, drug_id, doctor_id, territory_id, prescription_date, year, quarter, units, revenue)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )

    first_rep_id = rep_ids[0][0]
    users = [
        ("Admin User", "admin@pharma.com", "Admin@123", "admin", None, None),
        ("South Manager", "manager@pharma.com", "Manager@123", "manager", None, "South"),
        ("Demo Rep", "rep@pharma.com", "Rep@123", "rep", first_rep_id, rep_ids[0][1]),
    ]
    for name, email, password, role, rep_id, region in users:
        cur.execute(
            "INSERT INTO users(name, email, password_hash, role, rep_id, region) VALUES (?, ?, ?, ?, ?, ?)",
            (name, email, generate_password_hash(password), role, rep_id, region),
        )

    conn.commit()
    conn.close()
    print(f"Created {DB_PATH}")
    print("Tables: sales_reps=20, drugs=10, territories=5, prescriptions=%d, quotas=80, users=3" % len(rows))


if __name__ == "__main__":
    seed()
