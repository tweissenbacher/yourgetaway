import json
import os
from time import time
from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from datetime import date, time, datetime, timedelta

from website.model.line import LineSection, Recurrence
from website.model.user import User
from .. import db
from ..model import Section, Line, Trip, Route
from .forms import CompleteTripCreateForm, TripCreateForm


trips = Blueprint("trips", __name__)


@trips.route("/trips/", methods=["GET", "POST"])
@login_required
def trips_view():
    trips = Trip.query.all()
    return render_template("trips/trips.html", user=current_user, trips=trips)


@trips.route("/lines/<int:line_id>/create_trip/", methods=["GET", "POST"])
@login_required
def trip_create(line_id):
    line = Line.query.get(line_id)
    if not line:
        flash(f"Fahrtstrecke ID {line_id} nicht vorhanden!", category="error")
        return redirect(request.referrer)
    users = None
    trip = Trip(line_parent=Line.query.get(line_id))

    # trains DUMMY data
    trains = [
        {
            "id": 0,
            "bezeichnung": "REX 3920",
            "spurweite": "normal",
            "wagen": [
                {
                    "id": 0,
                    "bez": "Triebwagen",
                    "gewicht": 30000,
                    "sitze": 0
                },
                {
                    "id": 1,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 52
                },
                {
                    "id": 2,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 52
                },
                {
                    "id": 103,
                    "bez": "Speisewagen",
                    "gewicht": 19000,
                    "sitze": 52
                }
            ]
        },
        {
            "id": 1,
            "bezeichnung": "RJ 301",
            "spurweite": "normal",
            "wagen": [
                {
                    "id": 6,
                    "bez": "Triebwagen",
                    "gewicht": 30000,
                    "sitze": 0
                },
                {
                    "id": 8,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 52
                },
                {
                    "id": 15,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 52
                },
                {
                    "id": 102,
                    "bez": "Speisewagen",
                    "gewicht": 19000,
                    "sitze": 52
                }
            ]
        },
        {
            "id": 32,
            "bezeichnung": "IC 902",
            "spurweite": "normal",
            "wagen": [
                {
                    "id": 6,
                    "bez": "Triebwagen",
                    "gewicht": 30000,
                    "sitze": 0
                },
                {
                    "id": 8,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 52
                },
                {
                    "id": 15,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 52
                },
                {
                    "id": 102,
                    "bez": "Speisewagen",
                    "gewicht": 19000,
                    "sitze": 52
                }
            ]
        },
        {
            "id": 143,
            "bezeichnung": "Museumsbahn",
            "spurweite": "schmalspur",
            "wagen": [
                {
                    "id": 102,
                    "bez": "298.102 Steyrtalbahn Lok Nr. 2",
                    "gewicht": 30000,
                    "sitze": 0
                },
                {
                    "id": 103,
                    "bez": "Kohlewagen",
                    "gewicht": 19000,
                    "sitze": 0
                },
                {
                    "id": 233,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 24
                },
                {
                    "id": 234,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 24
                },
                {
                    "id": 235,
                    "bez": "Speisewagen",
                    "gewicht": 19000,
                    "sitze": 12
                }
            ]
        }
    ]

    # trains = filter(lambda t: t["spurweite"] == line.route.sections[0].track, trains)
    secprices = [sec.section.fee for sec in line.sections]
    price_min = sum(secprices) * 100
    # print(price_min)
    trip.price = price_min

    if request.method == "POST":
        note = request.form.get("note", default="", type=str)
        departure = request.form.get("departure", default="00:00", type=str)
        price = request.form.get("price", default=0, type=int)
        recurring = request.form.get("recurring", default=None, type=int)
        date_single = request.form.get("date", default=None, type=str)
        date_start = request.form.get("date_start", default=None, type=str)
        date_end = request.form.get("date_end", default=None, type=str)

        mon = request.form.get("mon", default=0, type=int)
        tue = request.form.get("tue", default=0, type=int)
        wed = request.form.get("wed", default=0, type=int)
        thu = request.form.get("thu", default=0, type=int)
        fri = request.form.get("fri", default=0, type=int)
        sat = request.form.get("sat", default=0, type=int)
        sun = request.form.get("sun", default=0, type=int)

        train_id = request.form.get("train_id", default=None, type=int)
        personell = request.form.getlist("personell")
        confirm = request.form.get("confirm", default=False, type=bool)

        trip.note = note

        if len(departure) < 2:
            departure = f"0{departure}"
        trip.departure = time.fromisoformat(departure)

        trip.price = max(price_min, price * 100)

        recurrence = Recurrence(
            mon=1,
            tue=1,
            wed=1,
            thu=1,
            fri=1,
            sat=1,
            sun=1,
        )

        if recurring == 0 and date_single is not None:
            date_single = date.fromisoformat(date_single)
            recurrence.date_start = date_single
            recurrence.date_end = date_single
        elif date_start and date_end is not None:
            date_start = date.fromisoformat(date_start)
            date_end = date.fromisoformat(date_end)
            recurrence.date_start = date_start
            recurrence.date_end = date_end
            recurrence.mon = mon
            recurrence.tue = tue
            recurrence.wed = wed
            recurrence.thu = thu
            recurrence.fri = fri
            recurrence.sat = sat
            recurrence.sun = sun
        trip.recurrence = recurrence

        # trains = filter(lambda t: not trip.is_train_in_use(t["id"]), trains)


        if train_id:
            trip.train_id = train_id
            with db.session.no_autoflush:
                users = User.query.all()

        resolved = []
        if personell:
            print(f"personell: {personell}")
            with db.session.no_autoflush:
                # trip.personell = [(user for user_id in personell for user in User.query.get(user_id))]
                for user_id in personell:
                    user = User.query.get(user_id)
                    if user:
                        trip.personell.append(user)
            # db.session.flush()

            resolved = trip.get_resolved_all_dict()

            resolved = sorted(resolved, key=lambda d: d["date"])
            db.session.flush()
        if confirm:
            db.session.add(trip)
            db.session.commit()
            flash("Durchführung angelegt!", category="success")
            return redirect(url_for("lines.line_detail", line_id=line.id))

        return render_template(
            "trips/trip_c3.html",
            current_user=current_user,
            line=line,
            recurring=recurring,
            trip=trip,
            resolved=resolved,
            recurrence=recurrence,
            trains=trains,
            users=users
            # step=step,
        )

    recurring = None
    step = 1
    return render_template(
        "trips/trip_c3.html", current_user=current_user, trip=trip, line=line
    )


@trips.route("/trip/<int:trip_id>/update/", methods=["GET", "POST"])
@login_required
def trip_update(trip_id):
    trip = Trip.query.get(trip_id)
    return render_template(
        "trips/trip_c3.html",
        current_user=current_user,
        trip=trip,
        line=trip.line_parent,
    )


@trips.route("/trip/<int:trip_id>/delete/", methods=["GET", "POST"])
@login_required
def trip_delete(trip_id):
    trip = Trip.query.get(trip_id)
    if trip:
        db.session.delete(trip)
        db.session.commit()
        flash(f"Durchführungen gelöscht!", category="success")
        return redirect(request.referrer)
    flash(f"Durchführungen gelöscht!", category="success")
    return redirect(request.referrer)
