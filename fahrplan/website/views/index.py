from functools import partial
import json
import os

from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from marshmallow import ValidationError
import requests

from .. import db
from ..model import Section, Line, User, Route, routes_schema


index = Blueprint("index", __name__)


@index.route("/", methods=["GET"])
def index_view():
    lines = Line.query.all()
    return render_template("index.html", user=current_user, lines=lines)


@index.route("/json", methods=["GET"])
def serve_routes():
    dat = [
        {
            "end": {"address": "Am Hbf 1, 1100 Wien", "id": 5, "name": "Wien Hbf"},
            "end_id": 5,
            "id": 1,
            "name": "Weststrecke",
            "route_sections": [
                {
                    "end": {
                        "address": "Bahnhofstra\u00dfe 31, 4600 Wels",
                        "id": 2,
                        "name": "Wels Hbf",
                    },
                    "end_id": 2,
                    "fee": 10,
                    "id": 1,
                    "section_warnings": [
                        {
                            "id": 1,
                            "warnings": "Baustelle bei Neumarkt a. W. - Verz\u00f6gerungen von ca 15 min.",
                        }
                    ],
                    "start": {
                        "address": "Suedtirolerplatz 1, 5020 Salzburg",
                        "id": 1,
                        "name": "Salzburg Hbf",
                    },
                    "start_id": 1,
                    "time": 60,
                    "track": "normal",
                },
                {
                    "end": {
                        "address": "Bahnhofplatz 3-6, 4020 Linz",
                        "id": 3,
                        "name": "Linz Hbf",
                    },
                    "end_id": 3,
                    "fee": 8,
                    "id": 2,
                    "section_warnings": [],
                    "start": {
                        "address": "Bahnhofstra\u00dfe 31, 4600 Wels",
                        "id": 2,
                        "name": "Wels Hbf",
                    },
                    "start_id": 2,
                    "time": 30,
                    "track": "normal",
                },
                {
                    "end": {
                        "address": "Bahnhofplatz 1, 3100 St. P\u00f6lten",
                        "id": 4,
                        "name": "St. P\u00f6lten Hbf",
                    },
                    "end_id": 4,
                    "fee": 12,
                    "id": 3,
                    "section_warnings": [],
                    "start": {
                        "address": "Bahnhofplatz 3-6, 4020 Linz",
                        "id": 3,
                        "name": "Linz Hbf",
                    },
                    "start_id": 3,
                    "time": 80,
                    "track": "normal",
                },
                {
                    "end": {
                        "address": "Am Hbf 1, 1100 Wien",
                        "id": 5,
                        "name": "Wien Hbf",
                    },
                    "end_id": 5,
                    "fee": 10,
                    "id": 4,
                    "section_warnings": [
                        {"id": 3, "warnings": "Maskenpflicht bei WIEN bis --.--.----"}
                    ],
                    "start": {
                        "address": "Bahnhofplatz 1, 3100 St. P\u00f6lten",
                        "id": 4,
                        "name": "St. P\u00f6lten Hbf",
                    },
                    "start_id": 4,
                    "time": 60,
                    "track": "normal",
                },
            ],
            "start": {
                "address": "Suedtirolerplatz 1, 5020 Salzburg",
                "id": 1,
                "name": "Salzburg Hbf",
            },
            "start_id": 1,
            "v_max": 230,
        },
        {
            "end": {
                "address": "Fritz-Mayer-Platz 1, 6900 Bregenz",
                "id": 8,
                "name": "Bregenz Hbf",
            },
            "end_id": 8,
            "id": 2,
            "name": "Suedstrecke",
            "route_sections": [
                {
                    "end": {
                        "address": "Europaplatz 4, 8020 Graz",
                        "id": 6,
                        "name": "Graz Hbf",
                    },
                    "end_id": 6,
                    "fee": 15,
                    "id": 6,
                    "section_warnings": [
                        {"id": 2, "warnings": "Maskenpflicht bei WIEN bis --.--.----"}
                    ],
                    "start": {
                        "address": "Am Hbf 1, 1100 Wien",
                        "id": 5,
                        "name": "Wien Hbf",
                    },
                    "start_id": 5,
                    "time": 120,
                    "track": "normal",
                },
                {
                    "end": {
                        "address": "Walther-von-der-Vogelweideplatz 1, 9020 Klagenfurt a.W.",
                        "id": 7,
                        "name": "Klagenfurt Hbf",
                    },
                    "end_id": 7,
                    "fee": 12,
                    "id": 7,
                    "section_warnings": [],
                    "start": {
                        "address": "Europaplatz 4, 8020 Graz",
                        "id": 6,
                        "name": "Graz Hbf",
                    },
                    "start_id": 6,
                    "time": 80,
                    "track": "normal",
                },
                {
                    "end": {
                        "address": "Fritz-Mayer-Platz 1, 6900 Bregenz",
                        "id": 8,
                        "name": "Bregenz Hbf",
                    },
                    "end_id": 8,
                    "fee": 30,
                    "id": 8,
                    "section_warnings": [],
                    "start": {
                        "address": "Walther-von-der-Vogelweideplatz 1, 9020 Klagenfurt a.W.",
                        "id": 7,
                        "name": "Klagenfurt Hbf",
                    },
                    "start_id": 7,
                    "time": 200,
                    "track": "normal",
                },
            ],
            "start": {"address": "Am Hbf 1, 1100 Wien", "id": 5, "name": "Wien Hbf"},
            "start_id": 5,
            "v_max": 200,
        },
    ]

    return jsonify({"routes": dat})


@index.route("/load", methods=["GET"])
def load_routes():
    res = requests.get("http://127.0.0.1:5000/json").content
    routes = json.loads(res)["routes"]
    for r in routes:
        db.session.add(Route.dict_to_obj(r))
    db.session.commit()
    r = Route.query.all()
    return jsonify(routes_schema.dump(r))


# load routes json with marshmallow - Nested (Invalid type error)
@index.route("/load2", methods=["GET"])
def load_routes2():
    res = requests.get("http://127.0.0.1:5000/json").content
    # section = Section(id=0)
    # print(res)
    schema = TestSchema(many=True)
    data = []
    try:
        # data = schema.load({"data": 200, "name": "test4"}, session=db.session)
        data = schema.load(
            res,
            session=db.session,
        )
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data
        print(errors)
        print(valid_data)
    # print(data)
    for d in data:
        print(d)
        db.session.add(d)
    db.session.commit()
    return jsonify(schema.dump(data))
