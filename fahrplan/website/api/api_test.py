from datetime import datetime
import json

from flask import Blueprint, Response, jsonify, make_response, redirect, request
from flask_login import current_user, login_required
from sqlalchemy import Time, select
from website.model import (
    Line,
    line_schema,
    lines_schema,
    Section,
    section_schema,
    sections_schema,
    Trip,
    trip_schema,
    User,
    user_schema,
    users_schema,
)

from .. import db

api_test = Blueprint("api_test", __name__)


# https://docs.sqlalchemy.org/en/14/orm/session_basics.html#querying-2-0-style


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


@api_test.route("/lines/<int:id>/trips/create/", methods=["GET"])
def test_api_create_trip(id):
    trip = Trip(
        note="Trip 0",
        departure=datetime.utcnow().time(),
        train_id=0,
        price=1250,
        recurrence_id=0,
        line_id=id,
    )
    db.session.add(trip)
    db.session.commit()
    res = trip_schema.dump(trip)
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
