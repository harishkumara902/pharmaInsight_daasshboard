from flask import Blueprint, render_template
from flask_login import login_required

drugs_bp = Blueprint("drugs", __name__)


@drugs_bp.route("/drugs")
@login_required
def drugs():
    return render_template("drugs.html", active="drugs")
