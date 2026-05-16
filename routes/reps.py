from flask import Blueprint, render_template
from flask_login import login_required

reps_bp = Blueprint("reps", __name__)


@reps_bp.route("/reps")
@login_required
def reps():
    return render_template("reps.html", active="reps")
