from datetime import date, time
import json

from flask import Blueprint, Response, jsonify, make_response, redirect, request
from flask_login import current_user, login_required
from sqlalchemy import and_, select
from ..models import (
    User,
    user_schema,
    users_schema,
    TrainstationModel,
    trainstation_schema,
    trainstations_schema
)

from .. import db

api = Blueprint("api", __name__)


@api.route("/api/")
def api_index():
    return jsonify(
        {
            "api": [
                "/trainstations",
                "/trainstations/<int:line_id>",
                "/users",
                "/users/<int:user_id>",
            ]
        }
    )


@api.route("/api/trainstations/", methods=["GET"])
def api_trainstations_all():
    trainstations = TrainstationModel.query.all()
    res = trainstations_schema.dump(trainstations)
    return jsonify({"trainstations": res})


@api.route("/api/trainstations/<int:line_id>/", methods=["GET"])
def api_trainstations_id(trainstation_id):
    trainstation = TrainstationModel.query.get(trainstation_id)
    res = trainstation_schema.dump(trainstation)
    # return jsonify({"trainstations": res})
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
