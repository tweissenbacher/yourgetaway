from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

from . import db
from website.models import RouteModel


route = {
    "0": {"name": "Weststrecke", "start": "Wien Hbf", "end": "Sbg Hbf",
          "route_sections": "[Wien Hbf - St. Pölten Hbf], [St.Pölten Hbf - Linz Hbf], [Linz Hbf - Sbg Hbf]",
          "warnings": "Maintenance work on sections [St. Pölten Hbf - Linz Hbf] between March 2022 and June 2022"},
    "1": {"name": "Weststrecke_return", "start": "Sbg Hbf", "end": "Wien Hbf",
          "route_sections": "[Sbg Hbf - Linz Hbf], [Linz Hbf - St. Pölten Hbf], [St. Pölten Hbf - Wien Hbf]",
          "warnings": "Maintenance work on sections [St. Pölten Hbf - Linz Hbf] between March 2022 and June 2022"},
}


route_put_args = reqparse.RequestParser()
route_put_args.add_argument("name", type=str, help="Name of the Route", required=True)
route_put_args.add_argument("start", type=str, help="Name of the Start", required=True)
route_put_args.add_argument("end", type=str, help="Name of the End", required=True)
route_put_args.add_argument("route_sections", type=str, help="Name of all sections on the route", required=True)
route_put_args.add_argument("warnings", type=str, help="Warnings", required=True)

route_update_args = reqparse.RequestParser()
route_update_args.add_argument("name", type=str, help="update_Name of the Route")
route_update_args.add_argument("start", type=str, help="update_Name of the Start")
route_update_args.add_argument("end", type=str, help="update_Name of the End")
route_update_args.add_argument("route_sections", type=str, help="update_Name of all sections on the route")
route_update_args.add_argument("warnings", type=str, help="update_Warnings")

route_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'start': fields.String,
    'end': fields.String,
    'route_sections': fields.String,
    'warnings': fields.String
}



class Routes(Resource):
    @marshal_with(route_resource_fields)
    def get(self):
        all_routes = RouteModel.query.all()
        return all_routes

class Route(Resource):
    @marshal_with(route_resource_fields)  # to define how to serialize it
    def get(self, route_id):
        result = RouteModel.query.filter_by(id=route_id).first()
        if not result:
            abort(404, message="Couldnt find ID_route")
        return result

    @marshal_with(route_resource_fields)
    def patch(self, route_id):
        args = route_update_args.parse_args()
        result = RouteModel.query.filter_by(id=route_id).first()
        if not result:
            abort(404, message="Route doesnt exist, cannot update")

        if args['name']:
            result.name = args['name']
        if args['start']:
            result.start = args['start']
        if args['end']:
            result.end = args['end']
        if args['route_sections']:
            result.route_sections = args['route_sections']
        if args['warnings']:
            result.warnings = args['warnings']

        db.session.commit()

        return result

    @marshal_with(route_resource_fields)  # to define how to serialize it
    def put(self, route_id):
        # abort_if_station_Exists(route_id)
        args = route_put_args.parse_args()
        result = RouteModel.query.filter_by(id=route_id).first()
        if result:
            abort(409, message="Id taken...")
        route = RouteModel(id=route_id, name=args['name'], start=args['start'], end=args['end'],
                           route_sections=args['route_sections'], warnings=args['warnings'])
        db.session.add(route)
        db.session.commit()
        return route, 201
