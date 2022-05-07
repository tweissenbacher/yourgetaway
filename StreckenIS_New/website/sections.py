from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

from . import db
from website.models import SectionModel



sections = {
    "0": {"start": "Wien Hbf", "end": "Graz Hbf", "track": "normal", "fee": 10, "time": 100},
    "1": {"start": "Wien Hbf", "end": "Linz Hbf", "track": "normal", "fee": 15, "time": 150},
    "2": {"start": "Linz Hbf", "end": "Sbg Hbf", "track": "normal", "fee": 8, "time": 80},
    "3": {"start": "Wien Hbf", "end": "St. Pölten Hbf", "track": "normal", "fee": 6, "time": 60},
    "4": {"start": "St. Pölten Hbf", "end": "Linz Hbf", "track": "normal", "fee": 10, "time": 10}
}

sections_resource_fields = {
    'id': fields.Integer,
    'start': fields.String,
    'end': fields.String,
    'track': fields.String,
    'fee': fields.Integer,
    'time': fields.Integer
}

sections_put_args = reqparse.RequestParser()
sections_put_args.add_argument("start", type=str, help="Name of the Start", required=True)
sections_put_args.add_argument("end", type=str, help="Name of the End", required=True)
sections_put_args.add_argument("track", type=str, help="Name of the Tracktype", required=True)
sections_put_args.add_argument("fee", type=int, help="Amount of the fee", required=True)
sections_put_args.add_argument("time", type=int, help="Amount of the time", required=True)

sections_update_args = reqparse.RequestParser()
sections_update_args.add_argument("start", type=str, help="update_Name of the Start")
sections_update_args.add_argument("end", type=str, help="update_Name of the End")
sections_update_args.add_argument("track", type=str, help="update_Name of the Tracktype")
sections_update_args.add_argument("fee", type=int, help="update_Amount of the fee")
sections_update_args.add_argument("time", type=int, help="update_Amount of the time")


class Sections(Resource):
    @marshal_with(sections_resource_fields)
    def get(self):
        all_sections = SectionModel.query.all()

        return all_sections


class Section(Resource):
    @marshal_with(sections_resource_fields)  # to define how to serialize it
    def get(self, sections_id):
        result = SectionModel.query.filter_by(id=sections_id).first()
        if not result:
            abort(404, message="Couldnt find ID_section")
        return result

    @marshal_with(sections_resource_fields)
    def patch(self, sections_id):
        args = sections_update_args.parse_args()
        result = SectionModel.query.filter_by(id=sections_id).first()
        if not result:
            abort(404, message="Section doesnt exist, cannot update")

        if args['start']:
            result.start = args['start']
        if args['end']:
            result.end = args['end']
        if args['track']:
            result.track = args['track']
        if args['fee']:
            result.fee = args['fee']
        if args['time']:
            result.time = args['time']

        db.session.commit()

        return result

    @marshal_with(sections_resource_fields)  # to define how to serialize it
    def put(self, sections_id):
        # abort_if_station_Exists(sections_id)
        args = sections_put_args.parse_args()
        result = SectionModel.query.filter_by(id=sections_id).first()
        if result:
            abort(409, message="Id taken...")
        sections = SectionModel(id=sections_id, start=args['start'], end=args['end'], track=args['track'],
                                fee=args['fee'], time=args['time'])
        db.session.add(sections)
        db.session.commit()
        return sections, 201
