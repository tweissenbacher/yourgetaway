from flask import Blueprint, render_template
from flask_login import current_user

from ..model import Line


index = Blueprint("index", __name__)


@index.route("/", methods=["GET"])
def index_view():
    lines = Line.query.all()
    return render_template("index.html", user=current_user, lines=lines)
