from datetime import date, time
import json
from flask_restful import fields, marshal_with, marshal
from flask import Blueprint, Response, jsonify, make_response, redirect, request
from flask_login import current_user, login_required
from sqlalchemy import and_, select
from ..models import (
    User,
    user_schema,
    users_schema,
    TrainstationModel,
    trainstation_schema,
    trainstations_schema,
    SectionModel,
    section_schema,
    sections_schema,
    RouteModel,
    route_schema,
    routes_schema,
    WarningModel,
    warning_section_schema,
    warnings_section_schema
)

from .. import db

api = Blueprint("api", __name__)

warnings_resource_fields = {
    'id': fields.Integer,
    'warning': fields.String
}

@api.route("/api/")
def api_index():
    return jsonify(
        {
            "api": [
                "/trainstations",
                "/trainstations/<int:trainstations_id>",
                "/users",
                "/users/<int:user_id>",
                "/sections",
                "/sections/<int:section_id>",
                "/routes",
                "/routes/<int:route_id>",
                "/warnings",
                "/warnings/<int:warnings_id>",
            ]
        }
    )


@api.route("/api/trainstations/", methods=["GET"])
def api_trainstations_all():
    trainstations = TrainstationModel.query.all()
    res = trainstations_schema.dump(trainstations)
    return jsonify({"trainstations": res})


@api.route("/api/trainstations/<int:trainstations_id>/", methods=["GET"])
def api_trainstations_id(trainstations_id):
    trainstation = TrainstationModel.query.get(trainstations_id)
    res = trainstation_schema.dump(trainstation)
    return jsonify(res)


@api.route("/api/users/", methods=["GET"])
def api_users_all():
    users = User.query.all()
    res = users_schema.dump(users)
    return jsonify({"users": res})


@api.route("/api/users/<int:user_id>", methods=["GET"])
def api_users_id(user_id):
    user = User.query.get(user_id)
    res = user_schema.dump(user)
    return jsonify(res)


@api.route("/api/sections/", methods=["GET"])
def api_sections_all():
    sections = SectionModel.query.all()
    res = sections_schema.dump(sections)
    return jsonify({"sections": res})


@api.route("/api/sections/<int:sections_id>/", methods=["GET"])
def api_sections_id(sections_id):
    section = SectionModel.query.get(sections_id)
    res = section_schema.dump(section)
    return jsonify(res)


@api.route("/api/routes/", methods=["GET"])
def api_routes_all():
    routes = RouteModel.query.all()
    res = routes_schema.dump(routes)
    return jsonify({"routes": res})


@api.route("/api/routes/<int:routes_id>/", methods=["GET"])
def api_routes_id(routes_id):
    route = RouteModel.query.get(routes_id)
    res = route_schema.dump(route)
    return jsonify(res)


@api.route("/api/warnings/", methods=["GET"])
def api_warnings_all():
    warnings = WarningModel.query.all()
    res = warnings_section_schema.dump(warnings)
    return jsonify({"warnings": res})


@api.route("/api/warnings/<int:warnings_id>/", methods=["GET"])
def api_warnings_id(warnings_id):
    warning = WarningModel.query.get(warnings_id)
    res = warning_section_schema.dump(warning)
    return jsonify(res)
