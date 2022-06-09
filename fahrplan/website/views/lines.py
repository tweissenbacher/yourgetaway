import datetime
import json
import os
from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import and_, select
from werkzeug.security import generate_password_hash, check_password_hash
import requests

from website.model.line import LineSection, Trip
from .. import db
from ..model import Section, Line, User, Route


lines = Blueprint("lines", __name__)


# @admin_required  #?? custom decorator ??
@lines.route("/lines/", methods=["GET", "POST"])
@login_required
def lines_view():
    lines = Line.query.all()
    lines = sorted(lines, key=lambda l: l.route.id)

    return render_template("lines/lines.html", current_user=current_user, lines=lines)


@lines.route("/lines/<int:line_id>/", methods=["GET", "POST"])
@login_required
def line_detail(line_id):
    line = Line.query.get(line_id)
    return render_template(
        "lines/line_detail.html", current_user=current_user, line=line
    )


@lines.route("/lines/create/", methods=["GET", "POST"])
# @lines.route("/lines/<int:line_id>/update", methods=["GET", "POST"])
@login_required
def line_create():
    if request.method == "POST":
        route_id = request.form.get("route_id", default=None, type=int)
        descr = request.form.get("descr", default=None, type=str)
        price = request.form.get("price", default=None, type=int)

        first_section = request.form.get("first_section", default=None, type=int)
        last_section = request.form.get("last_section", default=None, type=int)

        confirm = request.form.get("confirm", default=False, type=bool)

        sel_route = Route.query.get(route_id)
        line = None
        # line = Line.query.get(line_id)
        if first_section and last_section:
            linesections = []
            arrival = 0
            for s in range(first_section, last_section + 1):
                section = Section.query.get(s)
                arrival += section.duration
                linesections.append(LineSection(arrival=arrival, section=section))

            line = Line(
                descr=descr,
                price=price,
                route=Route.query.get(route_id),
                sections=linesections,
            )
            print(line)

        if confirm:
            db.session.add(line)
            db.session.commit()
            flash("Fahrtstrecke angelegt!", category="success")
            return redirect(url_for("lines.lines_detail", id=line.id))

        routes = Route.query.all()
        return render_template(
            "lines/line_c.html",
            current_user=current_user,
            routes=routes,
            sel_route=sel_route,
            descr=descr,
            price=price,
            first_section=first_section,
            last_section=last_section,
            line=line,
        )

    routes = Route.query.all()
    return render_template(
        "lines/line_c.html",
        current_user=current_user,
        routes=routes,
    )


@lines.route("/lines/<int:line_id>/update/", methods=["GET", "POST"])
@login_required
def line_update(line_id):

    if request.method == "POST":
        route_id = request.form.get("route_id", default=None, type=int)
        descr = request.form.get("descr", default=None, type=str)
        note = request.form.get("note", default=None, type=str)
        price = request.form.get("price", default=None, type=int)

        first_section = request.form.get("first_section", default=None, type=int)
        last_section = request.form.get("last_section", default=None, type=int)

        confirm = request.form.get("confirm", default=False, type=bool)

        sel_route = Route.query.get(route_id)
        line = Line.query.get(line_id)

        if first_section == last_section + 1:
            flash("Start und Endbahnhof dürfen nicht gleich sein!", category="error")
        elif first_section > last_section + 1:
            flash(
                "Startbahnhof darf nicht vor dem Endbahnhof liegen!", category="error"
            )
        elif first_section and last_section:
            linesections = []
            arrival = 0
            for s in range(first_section, last_section + 1):
                section = Section.query.get(s)
                arrival += section.duration
                linesections.append(LineSection(arrival=arrival, section=section))

            print(linesections)
            if not linesections:
                flash("Keine Sections!", category="error")
            else:
                line.update(
                    descr=descr,
                    price=price,
                    note=note,
                    sections=linesections,
                )
                print(line)

            if confirm:
                db.session.commit()
                flash("Fahrtstrecke bearbeitet!", category="success")
                return redirect(url_for("lines.lines_detail", id=line.id))

        routes = Route.query.all()
        return render_template(
            "lines/line_u.html",
            current_user=current_user,
            routes=routes,
            sel_route=sel_route,
            descr=descr,
            price=price,
            first_section=first_section,
            last_section=last_section,
            line=line,
        )

    line = Line.query.get(line_id)
    return render_template(
        "lines/line_u.html", current_user=current_user, line=line, update=True
    )


@lines.route("/lines/<int:line_id>/delete/", methods=["GET", "POST"])
@login_required
def line_delete(line_id):
    # TODO
    line = Line.query.get(line_id)
    if line:
        db.session.delete(line)
        db.session.commit()
        flash("Fahrtstrecke entfernt!", category="success")
        return redirect(url_for("lines.lines_view"))

    return render_template(
        "lines/line_detail.html", current_user=current_user, line=line, update=True
    )


#
# TRIPS


# @lines.route("/lines/<int:line_id>/trips/", methods=["GET", "POST"])
# @login_required
# def lines_trips(line_id):
#     line = Line.query.get(line_id)
#     return render_template("trips.html", current_user=current_user, line=line)


# /lines/7/?trips=intervals
# /lines/7/?trips=resolved&recurrence_id=2&items=20&page=1
@lines.route("/lines/<int:line_id>/resolved/", methods=["GET", "POST"])
@login_required
def line_detail_trips_resolved(line_id):

    # t_dep = request.args.get("t_dep", type=str, default='')
    # t_dep = time.fromisoformat(t_dep)
    sortby = request.args.get("sortby", default="date")
    page = request.args.get("page", type=int, default=1)
    items = request.args.get("items", type=int, default=10)
    i = (page - 1) * items

    line = Line.query.get(line_id)
    trips = Trip.query.filter(
        and_(
            Trip.line_id == line_id,
            # Trip.departure >= t_dep,
        )
    ).slice(i, i + items)

    resolved = []
    for trip in trips:
        start_date = trip.recurrence.date_start
        end_date = trip.recurrence.date_end
        current_date = start_date
        i = 0
        while current_date <= end_date:
            resolved.append(
                {
                    "rec_id": trip.recurrence.id,
                    "date": current_date,
                    "line": trip.line_parent,
                    "departure": trip.departure,
                    "arrival": datetime.time(
                        hour=trip.departure.hour,
                        minute=trip.departure.minute
                        + trip.line_parent.sections[-1].arrival,
                    ),
                    "personell": trip.personell,
                    "train_id": trip.train_id,
                }
            )
            current_date += datetime.timedelta(days=1)

    resolved = sorted(resolved, key=lambda d: d["date"])
    return render_template(
        "lines/line_detail.html",
        current_user=current_user,
        line=line,
        trips=trips,
        resolved=resolved,
    )
