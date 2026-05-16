from flask import Blueprint, render_template
from flask_login import login_required

territories_bp = Blueprint("territories", __name__)


@territories_bp.route("/territories")
@login_required
def territories():
    return render_template("territories.html", active="territories")
