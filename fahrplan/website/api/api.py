import json

from flask import Blueprint, Response, jsonify, make_response, redirect, request
from flask_login import current_user, login_required
from sqlalchemy import select
from website.model import (
    User,
    user_schema,
    users_schema,
    Line,
    line_schema,
    lines_schema,
)

from .. import db

api = Blueprint("api", __name__)


# https://docs.sqlalchemy.org/en/14/orm/session_basics.html#querying-2-0-style


@api.route("/api/")
def api_index():
    return jsonify(
        {
            "api": [
                "/lines",
                "/lines/<int:line_id>",
                "/users",
                "/users/<int:user_id>",
            ]
        }
    )


@api.route("/api/lines/", methods=["GET"])
def api_lines_all():
    lines = Line.query.all()
    res = lines_schema.dump(lines)
    return jsonify({"lines": res})


@api.route("/api/lines/<int:line_id>", methods=["GET"])
def api_lines_id(line_id):
    line = Line.query.get(line_id)
    res = line_schema.dump(line)
    # return jsonify({"lines": res})
    return jsonify(res)


@api.route("/api/users/", methods=["GET"])
def api_users_all():
    users = User.query.all()
    res = users_schema.dump(users)
    return jsonify(res)


@api.route("/api/users/<int:user_id>", methods=["GET"])
def api_users_id(user_id):
    user = User.query.get(user_id)
    res = user_schema.dump(user)
    return jsonify(res)