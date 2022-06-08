from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

from . import db
from .models import WarningModel

warnings = {
    "0": {"warnings": "Maintenance work on sections [St. Pölten Hbf - Linz Hbf] between March 2022 and June 2022"},
    "1": {"warnings": "Maintenance work on sections [...] between March 2022 and June 2022"},
}

warnings_put_args = reqparse.RequestParser()
warnings_put_args.add_argument("warning", type=str, help="warning", required=True)

warnings_update_args = reqparse.RequestParser()
warnings_update_args.add_argument("warning", type=str, help="update_warning")


warnings_resource_fields = {
    'id': fields.Integer,
    'warning': fields.String
}


class Warnings(Resource):
    @marshal_with(warnings_resource_fields)
    def get(self):
        all_warnings = WarningModel.query.all()
        return all_warnings


class Warning(Resource):
    @marshal_with(warnings_resource_fields)  # to define how to serialize it
    def get(self, warning_id):
        result = WarningModel.query.filter_by(id=warning_id).first()
        if not result:
            abort(404, message="Couldnt find ID-Warning")
        return result

    @marshal_with(warnings_resource_fields)
    def patch(self, warning_id):
        args = warnings_update_args.parse_args()
        result = WarningModel.query.filter_by(id=warning_id).first()
        if not result:
            abort(404, message="Warning doesnt exist, cannot update")

        if args['warnings']:
            result.warnings = args['warnings']

        db.session.commit()

        return result

    @marshal_with(warnings_resource_fields)  # to define how to serialize it
    def put(self, warning_id):
        # abort_if_station_Exists(route_id)
        args = warnings_put_args.parse_args()
        result = WarningModel.query.filter_by(id=warning_id).first()
        if result:
            abort(409, message="Id taken...")
        war = WarningModel(id=warning_id, warning=args['warnings'])
        db.session.add(war)
        db.session.commit()
        return war, 201
