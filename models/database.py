import sqlite3
from typing import Iterable, Optional

from flask_login import UserMixin

from config import DATABASE_PATH


def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def rows(query: str, params: Iterable = ()):
    with get_db() as conn:
        return [dict(r) for r in conn.execute(query, params).fetchall()]


def row(query: str, params: Iterable = ()):
    with get_db() as conn:
        result = conn.execute(query, params).fetchone()
        return dict(result) if result else None


class User(UserMixin):
    def __init__(self, data):
        self.user_id = data["user_id"]
        self.id = str(data["user_id"])
        self.name = data["name"]
        self.email = data["email"]
        self.password_hash = data["password_hash"]
        self.role = data["role"]
        self.rep_id = data["rep_id"]
        self.region = data["region"]

    @property
    def initials(self):
        return "".join(part[0] for part in self.name.split()[:2]).upper()


def get_user_by_id(user_id: str) -> Optional[User]:
    data = row("SELECT * FROM users WHERE user_id = ?", (user_id,))
    return User(data) if data else None


def get_user_by_email(email: str) -> Optional[User]:
    data = row("SELECT * FROM users WHERE lower(email) = lower(?)", (email,))
    return User(data) if data else None


def scope_clause(user, prefix="p"):
    if not user or user.role == "admin":
        return "", []
    if user.role == "manager":
        return f" AND {prefix}.rep_id IN (SELECT rep_id FROM sales_reps WHERE region = ?)", [user.region]
    return f" AND {prefix}.rep_id = ?", [user.rep_id]


def rep_scope_clause(user, prefix="sr"):
    if not user or user.role == "admin":
        return "", []
    if user.role == "manager":
        return f" AND {prefix}.region = ?", [user.region]
    return f" AND {prefix}.rep_id = ?", [user.rep_id]
