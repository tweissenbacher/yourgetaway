import json
import os
from time import time
from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from datetime import date, time, datetime

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


# @trips.route("/lines/<int:line_id>/create_trip/", methods=["GET", "POST"])
# @login_required
# def trip_create(line_id):
#     line = Line.query.get(line_id)
#     if not line:
#         flash(f"Fahrtstrecke ID {line_id} nicht vorhanden!", category="error")
#         return redirect(request.referrer)

#     all_trains = [
#         (0, "0 - Rex3364"),
#         (1, "0 - WB200"),
#         (2, "0 - R38722"),
#         (3, "0 - RJ302"),
#     ]

#     step = 1

#     new_trip = Trip()
#     form = TripCreateForm(obj=new_trip)

#     form.train.choices = all_trains
#     form.personell.choices = [
#         (user.id, f"{user.last_name} {user.first_name}")
#         for user in User.query.filter(User.admin == 0).all()
#     ]

#     if request.method == "POST":
#         form.populate_obj(new_trip)

#         print(new_trip)

#     return render_template(
#         "trips/trip_c.html",
#         current_user=current_user,
#         line=line,
#         form=form,
#         new_trip=new_trip,
#         step=step,
#     )

#     request.form.get("departure")
#     request.form.get("price")
#     request.form.get("note")
#     request.form.get("train")
#     request.form.get("departure")


# @trips.route("/lines/<int:line_id>/create_trip/", methods=["GET", "POST"])
# @login_required
# def trip_create(line_id):
#     line = Line.query.get(line_id)
#     if not line:
#         flash(f"Fahrtstrecke ID {line_id} nicht vorhanden!", category="error")
#         return redirect(request.referrer)

#     all_trains = [
#         (0, "0 - Rex3364"),
#         (1, "1 - WB200"),
#         (2, "2 - R38722"),
#         (3, "3 - RJ302"),
#     ]

#     # form.trip.object_data=new_trip
#     # form.trip.personell.query = User.query.filter(User.admin==0).order_by(User.last_name)

#     # form.personell.choices = [
#     #     (user.id, f"{user.last_name} {user.first_name}")
#     #     for user in User.query.filter(User.admin == 0).all()
#     # ]

#     form = CompleteTripCreateForm()
#     if not form.proceed1.data:
#         print(0000)
#         step = 1
#         new_recurrence = Recurrence()
#         new_trip = Trip(line_id=line_id)

#     # new_recurrence = Recurrence()
#     # new_trip = Trip()
#     if form.proceed1.data and form.recurrence.validate_on_submit():
#         print(222222)

#         # form.recurrence.populate_obj(new_recurrence, "data")
#         form.recurrence.populate_obj(new_trip, "recurrence")
#         form.trip.train_id.choices = all_trains
#         print(new_trip.recurrence)
#         print("..........")
#         # form.recurrence.render_kw={"disabled":""}
#         step = 2

#     if form.proceed2.data and form.trip.train_id:
#         print(33333)
#         form.trip.populate_obj(new_trip, "trip")
#         # new_trip.train_id = form.trip.train_id.data
#         # new_trip.price = form.trip.price.data
#         form.trip.personell.choices = [
#             (f"{user.id} - {user.first_name} {user.last_name}")
#             for user in User.query.all()
#             # if not user.is_blocked(
#             #     departure=new_trip.departure,
#             #     dt_start=new_recurrence.date_start,
#             #     dt_end=new_recurrence.date_end,
#             # )

#         ]

#         print(new_trip)
#         step = 3


#     if form.proceed3.data:
#         print(new_recurrence.date_end)
#         # print(avail_users)

#         # form.trip.personell.query = User.query.filter(
#         #     User.is_blocked(
#         #         departure=new_trip.departure,
#         #         dt_start=new_recurrence.date_start,
#         #         dt_end=new_recurrence.date_end,
#         #     )
#         #     == False
#         # ).order_by(User.last_name)
#         # form.trip.personell.query = User.query.filter(User.admin==0).order_by(User.last_name)

#         # new_trip.personell=form.trip.personell.data

#     if step == 4:
#         new_trip.recurrence = new_recurrence
#         # print(form.proceed)
#         form.trip.populate_obj(new_trip, "data")
#         # print(form.trip.data)
#         # print(new_trip)

#     return render_template(
#         "trips/trip_c.html",
#         current_user=current_user,
#         line=line,
#         form=form,
#         new_trip=new_trip,
#         step=step,
#     )


@trips.route("/lines/<int:line_id>/create_trip/", methods=["GET", "POST"])
@login_required
def trip_create(line_id):
    line = Line.query.get(line_id)
    if not line:
        flash(f"Fahrtstrecke ID {line_id} nicht vorhanden!", category="error")
        return redirect(request.referrer)
    users = None
    trip = Trip(line_parent=Line.query.get(line_id))

    if request.method == "POST":
        departure = request.form.get("departure", default="11:11", type=str)
        price = request.form.get("price", default=0, type=int)
        note = request.form.get("note", default="", type=str)
        recurring = request.form.get("recurring", default=None, type=int)
        date_single = request.form.get("date", default=None, type=str)
        date_start = request.form.get("date_start", default=None, type=str)
        date_end = request.form.get("date_end", default=None, type=str)
        print(date_start, date_end, date_single)
        # daily = request.form.get("daily", default=0, type=int)
        mon = request.form.get(
            "mon",
            default=0,
        )
        tue = request.form.get("tue", default=0, type=int)
        wed = request.form.get("wed", default=0, type=int)
        thu = request.form.get("thu", default=0, type=int)
        fri = request.form.get("fri", default=0, type=int)
        sat = request.form.get("sat", default=0, type=int)
        sun = request.form.get("sun", default=0, type=int)
        train_id = request.form.get("train_id", default=None, type=int)
        personell = request.form.get("personell", default=None, type=list)
        confirm = request.form.get("confirm", default=False, type=bool)

        print(mon)
        trains = None
        trip.note = note
        trip.departure = time.fromisoformat(departure)
        trip.price = price
        recurrence = Recurrence()

        if recurring == 0 and date_single is not None:
            # flash("date", category="error")
            # return redirect(request.referrer)

            date_single = date.fromisoformat(date_single)
            recurrence = Recurrence(
                date_start=date_single,
                date_end=date_single,
                mon=mon,
                tue=tue,
                wed=wed,
                thu=thu,
                fri=fri,
                sat=sat,
                sun=sun,
            )
            trip.recurrence = recurrence

        elif date_start and date_end is not None:
            # flash("date", category="error")
            # return redirect(request.referrer)

            date_start = date.fromisoformat(date_start)
            date_end = date.fromisoformat(date_end)
            recurrence = Recurrence(
                date_start=date_start,
                date_end=date_end,
                mon=mon,
                tue=tue,
                wed=wed,
                thu=thu,
                fri=fri,
                sat=sat,
                sun=sun,
            )
            trip.recurrence = recurrence
            # trains.
        # recurrence.date_start = date_start
        # recurrence.date_end = date_end
        trains = [
            (0, "0 - Rex3364"),
            (1, "1 - WB200"),
            (2, "2 - R38722"),
            (3, "3 - RJ302"),
        ]
        if train_id:
            trip.train_id = train_id
            with db.session.no_autoflush:
                users = User.query.all()
        if personell:
            print(personell)
            with db.session.no_autoflush:
                for user_id in personell:
                    trip.personell.append(User.query.get(user_id))
                    # db.session.flush()
                # trip.personell = [(user for user_id in personell for user in User.query.get(user_id))]

        if confirm:
            db.session.add(trip)
            db.session.commit()

        return render_template(
            "trips/trip_c3.html",
            current_user=current_user,
            line=line,
            recurring=recurring,
            trip=trip,
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
