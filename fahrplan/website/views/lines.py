import json
import os
from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
import requests

from website.model.line import LineSection
from .. import db
from ..model import Section, Line, User, Route


lines = Blueprint("lines", __name__)


# @admin_required  #?? custom decorator ??
@lines.route("/lines/", methods=["GET", "POST"])
@login_required
def lines_view():
    lines = Line.query.all()
    return render_template("lines.html", user=current_user, lines=lines)


@lines.route("/lines/<int:id>/", methods=["GET", "POST"])
@login_required
def lines_detail(id):
    line = Line.query.get(id)
    return render_template("line_detail.html", user=current_user, line=line)

@lines.route("/lines/<int:id>/update/", methods=["GET", "POST"])
@login_required
def lines_update(id):
    line = Line.query.get(id)
    return render_template("line_detail.html", user=current_user, line=line, update=True)

@lines.route("/lines/<int:id>/delete/", methods=["GET", "POST"])
@login_required
def lines_delete(id):
    # TODO
    line = Line.query.get(id)
    if line:
        db.session.delete(line)
        db.session.commit()
        flash("Fahrtstrecke entfernt!", category="success")
        return redirect(url_for("lines.lines_view"))

    return render_template("line_detail.html", user=current_user, line=line, update=True)


@lines.route("/lines/create/", methods=["GET", "POST"])
# @lines.route("/lines/<int:line_id>/update", methods=["GET", "POST"])
@login_required
def lines_create():
    if request.method == "POST":
        route_id = request.form.get("route_id", default=None, type=int)
        descr = request.form.get("descr", default=None, type=str)
        price = request.form.get("price", default=None, type=int)

        first_section = request.form.get("first_section", default=None, type=int)
        last_section = request.form.get("last_section", default=None, type=int)
        
        confirm = request.form.get('confirm', default=False, type=bool)

        sel_route = Route.query.get(route_id)
        line = None
        # line = Line.query.get(line_id)
        if first_section and last_section:
            linesections = []
            arrival = 0
            for s in range(first_section, last_section+1):
                section=Section.query.get(s)
                arrival += section.duration
                linesections.append(LineSection(arrival=arrival, section=section))

            line = Line(
                descr=descr, price=price, route=Route.query.get(route_id), sections=linesections
            )
            print(line)
        
        if confirm:
            db.session.add(line)
            db.session.commit()
            flash("Fahrtstrecke angelegt!", category="success")
            return redirect(url_for("lines.lines_detail", id=line.id))
        
        routes = Route.query.all()
        return render_template(
            "lines_c.html",
            user=current_user,
            routes=routes,
            sel_route=sel_route,
            descr=descr,
            price=price,
            first_section=first_section,
            last_section=last_section,
            line=line
        )
        
    routes = Route.query.all()
    return render_template(
        "lines_c.html",
        user=current_user,
        routes=routes,
    )


@lines.route("/lines/<int:id>/trips/", methods=["GET", "POST"])
@login_required
def lines_trips(id):
    line = Line.query.get(id)
    return render_template("trips.html", user=current_user, line=line)

