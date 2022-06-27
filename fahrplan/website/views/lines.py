import json
import os
from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import and_
import requests

from website.model.line import LineSection, Trip
from .. import db
from ..model import Section, Line, Route


lines = Blueprint("lines", __name__)


# @admin_required  #TODO custom decorator ??
@lines.route("/lines/", methods=["GET", "POST"])
@login_required
def lines_view():
    """View function: show all lines"""
    lines = Line.query.all()
    lines = sorted(lines, key=lambda l: l.route.id)
    return render_template("lines/lines.html", current_user=current_user, lines=lines)


@lines.route("/lines/<int:line_id>/", methods=["GET", "POST"])
@login_required
def line_detail(line_id):
    """View function: show line details page by id"""
    line = Line.query.get(line_id)
    return render_template(
        "lines/line_detail.html", current_user=current_user, line=line
    )


@lines.route("/lines/create/", methods=["GET", "POST"])
# @lines.route("/lines/<int:line_id>/update", methods=["GET", "POST"])
@login_required
def line_create():
    """View function: page to create a new line"""
    if request.method == "POST":
        route_id = request.form.get("route_id", default=None, type=int)
        descr = request.form.get("descr", default=None, type=str)
        note = request.form.get("note", default=None, type=str)
        # price = request.form.get("price", default=None, type=int)

        first_section = request.form.get("first_section", default=None, type=int)
        last_section = request.form.get("last_section", default=None, type=int)

        confirm = request.form.get("confirm", default=False, type=bool)

        sel_route = Route.query.get(route_id)
        line = None



        # step 2
        if first_section and last_section:
            linesections = []
            arrival = 0
            for s in range(first_section, last_section + 1):
                section = Section.query.get(s)
                arrival += section.duration
                linesections.append(LineSection(arrival=arrival, section=section))

                secprices = [sec.section.fee for sec in linesections]
                price_min = sum(secprices) * 100

            line = Line(
                descr=descr,
                note=note,
                price=price_min,
                route=Route.query.get(route_id),
                sections=linesections,
            )
            print(line)
        # step final
        if confirm:
            db.session.add(line)
            db.session.commit()
            flash("Fahrtstrecke angelegt!", category="success")
            return redirect(url_for("lines.line_detail", line_id=line.id))

        routes = Route.query.all()
        return render_template(
            "lines/line_c.html",
            current_user=current_user,
            routes=routes,
            sel_route=sel_route,
            descr=descr,
            # price=price,
            first_section=first_section,
            last_section=last_section,
            line=line,
        )

    url = os.environ.get("STRECKEN_API_URL")
    try:
        res = requests.get(url).content
        routes = json.loads(res)["routes"]
        for r in routes:
            r = Route.dict_to_obj(r)
            db_route = Route.query.get(r.id)
            print(db_route)
            if not db_route:
                db.session.add(r)
        db.session.commit()
        flash("Streckendaten erfolgreich geladen!", category="success")
    except requests.exceptions.RequestException as e:
        flash(f"Streckendaten laden fehlgeschlagen!", category="error")
        flash(f"- {e}", category="error")

    routes = Route.query.all()
    return render_template(
        "lines/line_c.html",
        current_user=current_user,
        routes=routes,
    )


@lines.route("/lines/<int:line_id>/update/", methods=["GET", "POST"])
@login_required
def line_update(line_id):
    """View function: update page for given line by ID"""
    if request.method == "POST":
        route_id = request.form.get("route_id", default=None, type=int)
        descr = request.form.get("descr", default=None, type=str)
        note = request.form.get("note", default=None, type=str)
        # price = request.form.get("price", default=None, type=int)

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
                secprices = [sec.section.fee for sec in linesections]
                price_min = sum(secprices) * 100

            print(linesections)
            if not linesections:
                flash("Keine Sections!", category="error")
            else:
                line.update(
                    descr=descr,
                    price=price_min,
                    note=note,
                    sections=linesections,
                )
                print(line)

            if confirm:
                db.session.commit()
                flash("Fahrtstrecke bearbeitet!", category="success")
                return redirect(url_for("lines.line_detail", line_id=line.id))

        routes = Route.query.all()
        return render_template(
            "lines/line_u.html",
            current_user=current_user,
            routes=routes,
            sel_route=sel_route,
            descr=descr,
            # price=price,
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
    """View function to delete a given line by ID"""
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


@lines.route("/lines/<int:line_id>/resolved/", methods=["GET", "POST"])
@login_required
def line_detail_trips_resolved(line_id):
    """View function to show line details page with all individual trips"""
    # TODO pages for individual trips
    # /lines/7/?trips=intervals
    # /lines/7/?trips=resolved&recurrence_id=2&items=20&page=1

    # sortby = request.args.get("sortby", default="date")
    # page = request.args.get("page", type=int, default=1)
    # items = request.args.get("items", type=int, default=10)
    # i = (page - 1) * items

    line = Line.query.get(line_id)
    trips = Trip.query.filter(
        and_(
            Trip.line_id == line_id,
            # Trip.departure >= t_dep,
        )
    )
    # .slice(i, i + items)

    resolved = []
    for trip in trips:
        resolved.extend(trip.get_resolved_all_dict())

    resolved = sorted(resolved, key=lambda d: d["date"])
    return render_template(
        "lines/line_detail.html",
        current_user=current_user,
        line=line,
        trips=trips,
        resolved=resolved,
    )
