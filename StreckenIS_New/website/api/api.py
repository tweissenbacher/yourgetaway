from flask import Blueprint, jsonify

# Import models and Schemas
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

#Prefix
api = Blueprint("api", __name__)

@api.route("/api/")
def api_index():
    return jsonify(
        {
            "api": [
                "/trainstations",
                "/trainstations/<int:trainstations_id>",
                "/users",
                "/users/<int:users_id>",
                "/sections",
                "/sections/<int:sections_id>",
                "/routes",
                "/routes/<int:routes_id>",
                "/warnings",
                "/warnings/<int:warnings_id>",
            ]
        }
    )

# All Trainstations
@api.route("/api/trainstations/", methods=["GET"])
def api_trainstations_all():
    trainstations = TrainstationModel.query.all()
    res = trainstations_schema.dump(trainstations)
    return jsonify({"trainstations": res})

# Trainstations by Id
@api.route("/api/trainstations/<int:trainstations_id>/", methods=["GET"])
def api_trainstations_id(trainstations_id):
    trainstation = TrainstationModel.query.get(trainstations_id)
    res = trainstation_schema.dump(trainstation)
    return jsonify(res)

# All Users
@api.route("/api/users/", methods=["GET"])
def api_users_all():
    users = User.query.all()
    res = users_schema.dump(users)
    return jsonify({"users": res})

# Users by Id
@api.route("/api/users/<int:user_id>", methods=["GET"])
def api_users_id(user_id):
    user = User.query.get(user_id)
    res = user_schema.dump(user)
    return jsonify(res)

# All Sections
@api.route("/api/sections/", methods=["GET"])
def api_sections_all():
    sections = SectionModel.query.all()
    res = sections_schema.dump(sections)
    return jsonify({"sections": res})

# Sections by Id
@api.route("/api/sections/<int:sections_id>/", methods=["GET"])
def api_sections_id(sections_id):
    section = SectionModel.query.get(sections_id)
    res = section_schema.dump(section)
    return jsonify(res)

# All Routes
@api.route("/api/routes/", methods=["GET"])
def api_routes_all():
    routes = RouteModel.query.all()
    res = routes_schema.dump(routes)
    return jsonify({"routes": res})

# Routes by Id
@api.route("/api/routes/<int:routes_id>/", methods=["GET"])
def api_routes_id(routes_id):
    route = RouteModel.query.get(routes_id)
    res = route_schema.dump(route)
    return jsonify(res)

# All Warnings
@api.route("/api/warnings/", methods=["GET"])
def api_warnings_all():
    warnings = WarningModel.query.all()
    res = warnings_section_schema.dump(warnings)
    return jsonify({"warnings": res})

# Warnings by Id
@api.route("/api/warnings/<int:warnings_id>/", methods=["GET"])
def api_warnings_id(warnings_id):
    warning = WarningModel.query.get(warnings_id)
    res = warning_section_schema.dump(warning)
    return jsonify(res)
