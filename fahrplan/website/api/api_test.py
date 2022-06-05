from datetime import date, datetime, time
import json

from flask import (
    Blueprint,
    Response,
    jsonify,
    make_response,
    redirect,
    request,
    session,
)
from flask_login import current_user, login_required
from sqlalchemy import Time, and_, select
from website.model import (
    Line,
    line_schema,
    lines_schema,
    Section,
    section_schema,
    sections_schema,
    Trip,
    trip_schema,
    trips_schema,
    User,
    user_schema,
    users_schema,
)
from website.model.line import Recurrence

from .. import db

api_test = Blueprint("api_test", __name__)


# https://docs.sqlalchemy.org/en/14/orm/session_basics.html#querying-2-0-style


@api_test.route("/test/", methods=["GET"])
@api_test.route("/test/<another>", methods=["GET"])
def test_api_multiple(another):
    if another:
        return jsonify(another)
    return jsonify(res)


@api_test.route("/lines/", methods=["GET"])
def test_api_lines():
    # lines = db.session.execute(
    #     select(
    #         Line.description,
    #         # Line.note,
    #         Line.price,
    #         Line.sections  #)  # bool is not iterable, #??
    #     )#.select_from(Section).join(Section.line_id)
    #     .order_by(Line.id.desc())
    #     # .limit(2)
    # )
    lines = Line.query.all()
    # lines = []
    print(lines)
    res = lines_schema.dump(lines)
    # return jsonify({"lines": res})
    return jsonify(res)


@api_test.route("/lines/<int:id>/", methods=["GET"])
def test_api_line_by_id(id):
    line = Line.query.get(id)
    print(line)
    res = line_schema.dump(line)
    return jsonify(res)


# api-test/lines/7/trips/create?note=notiz&price=1360&t_dep=12:00&dt_start=2022-04-02&dt_end=2022-08-02&
@api_test.route("/lines/<int:line_id>/trips/create/", methods=["GET"])
def test_api_create_trip(line_id):
    note = request.args.get("note", type=str)
    price = request.args.get("price", type=int)

    t_dep = request.args.get("t_dep", type=str)
    dt_start = request.args.get("dt_start", type=str)
    dt_end = request.args.get("dt_end", type=str)

    dt_start = date.fromisoformat(dt_start)
    dt_end = date.fromisoformat(dt_end)
    t_dep = time.fromisoformat(t_dep)

    rec = Recurrence(dt_start, dt_end, 1, 1, 1, 1, 1, 0, 0)

    trip = Trip(
        note=note,
        departure=t_dep,
        train_id=0,
        price=price,
        recurrence=rec,
        line_id=line_id,
    )
    db.session.add(trip)
    db.session.commit()
    res = trip_schema.dump(trip)
    print(res)
    return jsonify(res)


# api-test/lines/7/trips/?note=notiz&price=1360&t_dep=12:00&dt_start=2022-04-02&dt_end=2022-08-02&items=10&page=1
@api_test.route("/lines/<int:line_id>/trips/", methods=["GET"])
def test_api_trips_filtered(line_id):
    # note = request.args.get("note", type=str)
    # price = request.args.get("price", type=int)

    t_dep = request.args.get("t_dep", type=str)
    dt_start = request.args.get("dt_start", type=str)  # , default=datetime.now())

    t_dep = time.fromisoformat(t_dep)
    dt_start = date.fromisoformat(dt_start)

    page = request.args.get("page", type=int, default=1)
    items = request.args.get("items", type=int, default=10)

    i = (page - 1) * items

    trips = Trip.query.filter(
        and_(
            Trip.line_id == line_id,
            Trip.departure >= t_dep,
            Trip.recurrence.has(Recurrence.date_start <= dt_start),
            Trip.recurrence.has(Recurrence.date_end >= dt_start),
        )
    ).slice(i, i + items)

    # filters = {'t_dep':t_dep, 'dt_start':dt_start}
    # query = session.query(Trip)
    # for filt, val in filters.iteritems():
    #     query = query.filter(getattr(Trip, attr))

    res = trips_schema.dump(trips)
    print(res)
    return jsonify(res)


####
####
####
####


@api_test.route("/<int:n>", methods=["GET"])
def test_url_jsonify1(n):
    return jsonify({"n": n})


@api_test.route("/<x>", methods=["GET"])
def test_url_jsonify(x):
    if x == "a":
        return jsonify({"1": "aaaa"})
    if x == "b":
        return jsonify({"1": "bbbb"})
    else:
        return jsonify({"1": "invalid"})


@api_test.route("api/delete-fs", methods=["POST"])
@login_required
def delete_fs():
    """
    delete method for javascript evt listener
    """
    data = json.loads(request.data)
    fs_id = data["fs_id"]
    fs = Fahrtstrecke.query.get(fs_id)
    if fs:
        db.session.delete(fs)
        db.session.commit()
        return f"{fs_id} deleted", 200
    else:
        return "", 404


@api_test.route("api/fs/delete/<fs_id>", methods=["POST"])
@login_required
def api_fs_delete(fs_id):
    """
    delete method for html form button no-js
    """
    fs = Fahrtstrecke.query.get(fs_id)
    if fs:
        db.session.delete(fs)
        db.session.commit()
    # return jsonify({})
    return redirect(
        request.referrer
    )  # , "200" # returns 302 found, or 200 and redirect hangs


@api_test.route("/durchfuehrung", methods=["GET"])
def api_durchf_urlparam():

    # request.args.getlist(),
    req_args = request.args
    from_st = request.args.get("from_st")
    to_st = request.args.get("to_st")
    dtfrom = request.args.get("dtfrom")
    n = request.args.get("n")  # anzahl
    p = request.args.get("p")  # page

    with open("website\durchf.json", encoding="utf-8") as f:
        durchfuehrungen = json.load(f)

    return jsonify(
        {
            "request": {
                "args": req_args,
                "from_st": from_st,
                "to_st": to_st,
                "dtfrom": dtfrom,
                "n": n,
                "p": p,
            },
            "response": {"durchfuehrungen": durchfuehrungen},
        }
    )


@api_test.route("/durchfuehrung/<from_st>/<to_st>", methods=["GET"])
def api_durchf_slash(from_st, to_st):
    req_args = request.args
    dtfrom = request.args.get("dtfrom")
    n = request.args.get("n")  # anzahl
    p = request.args.get("p")  # page

    with open("website\durchf.json", encoding="utf-8") as f:
        durchfuehrungen = json.load(f)

    return jsonify(
        {
            "request": {
                "args": req_args,
                "from_st": from_st,
                "to_st": to_st,
                "dtfrom": dtfrom,
                "n": n,
                "p": p,
            },
            "response": {"durchfuehrungen": durchfuehrungen},
        }
    )
