from flask import Blueprint, jsonify
from flask_login import login_required
from website.model import (
    User,
    user_with_trips_schema,
    users_with_trips_schema,
    Line,
    line_schema,
    lines_schema,
)


api = Blueprint("api", __name__)


@api.route("/api/")
def api_index():
    """view function

    Returns:
        json: available API URLs
    """    
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
    """view function

    Returns:
        json: all lines (Fahrtstrecken)
    """    
    lines = Line.query.all()
    res = lines_schema.dump(lines)
    return jsonify({"lines": res})


@api.route("/api/lines/<int:line_id>/", methods=["GET"])
def api_lines_id(line_id):
    """view function

    Returns:
        json: line by id (Fahrtstrecke)
    """    
    line = Line.query.get(line_id)
    res = line_schema.dump(line)
    # return jsonify({"lines": res})
    return jsonify(res)


#
# USERS
#
@api.route("/api/users/", methods=["GET"])
@login_required
def api_users_all():
    """view function

    Returns:
        json: all users (Personal)
    """
    users = User.query.all()
    res = users_with_trips_schema.dump(users)
    return jsonify(res)


@api.route("/api/users/<int:user_id>", methods=["GET"])
def api_users_id(user_id):
    """view function

    Returns:
        json: user by id (Personal)
    """
    user = User.query.get(user_id)
    res = user_with_trips_schema.dump(user)
    return jsonify(res)
