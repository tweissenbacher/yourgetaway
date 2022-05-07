from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

from . import db
from website.models import TrainstationModel

trainstations = {
    "0": {"name": "Wien Hbf", "address": "Am Hbf 1, 1100 Wien"},
    "1": {"name": "St. Pölten Hbf", "address": "Bahnhofplatz 1, 3100 St. Pölten"},
    "2": {"name": "Linz Hbf", "address": "Bahnhofplatz 3-6, 4020 Linz"},
    "3": {"name": "Graz Hbf", "address": "Europastraße 4, 8020 Graz"},
    "4": {"name": "Sbg Hbf", "address": "Suedtirolerplatz 1, 5020 Salzburg"}
}

trainstations_put_args = reqparse.RequestParser()
trainstations_put_args.add_argument("name", type=str, help="Name of the Trainstation", required=True)
trainstations_put_args.add_argument("address", type=str, help="Address of the Trainstation", required=True)

trainstations_update_args = reqparse.RequestParser()
trainstations_update_args.add_argument("name", type=str, help="update_Name of the Trainstation")
trainstations_update_args.add_argument("address", type=str, help="update_Address of the Trainstation")

trainstation_put_args = reqparse.RequestParser()
trainstation_put_args.add_argument("name", type=str, help="Name of the Trainstation", required=True)
trainstation_put_args.add_argument("address", type=str, help="Address of the Trainstation", required=True)

trainstation_update_args = reqparse.RequestParser()
trainstation_update_args.add_argument("name", type=str, help="update_Name of the Trainstation")
trainstation_update_args.add_argument("address", type=str, help="update_Address of the Trainstation")

trainstation_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'address': fields.String,
}

trainstations_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'address': fields.String,
}



def abort_if_id_notExists(trainstations_id):
    if trainstations_id not in trainstations:
        abort(404, message="Couldnt find ID")


def abort_if_station_Exists(trainstations_id):
    if trainstations_id in trainstations:
        abort(409, message="Station already exists")


class Trainstations(Resource):
    @marshal_with(trainstations_resource_fields)
    def get(self):
        result = TrainstationModel.query.all()

        return result


class Trainstation(Resource):
    @marshal_with(trainstation_resource_fields)  # to define how to serialize it
    def get(self, trainstations_id):
        if trainstations_id:
            result = TrainstationModel.query.filter_by(id=trainstations_id).first()
        if not result:
            abort(404, message="Couldnt find ID")
        return result

    @marshal_with(trainstation_resource_fields)
    def patch(self, trainstations_id):
        args = trainstation_update_args.parse_args()
        result = TrainstationModel.query.filter_by(id=trainstations_id).first()
        if not result:
            abort(404, message="Trainstation doesnt exist, cannot update")

        if args['name']:
            result.name = args['name']
        if args['address']:
            result.address = args['address']

        db.session.commit()

        return result

    @marshal_with(trainstation_resource_fields)  # to define how to serialize it
    def put(self, trainstations_id):
        # abort_if_station_Exists(trainstations_id)
        args = trainstation_put_args.parse_args()
        result = TrainstationModel.query.filter_by(id=trainstations_id).first()
        if result:
            abort(409, message="Id taken...")
        trainstations = TrainstationModel(id=trainstations_id, name=args['name'], address=args['address'])
        db.session.add(trainstations)
        db.session.commit()
        return trainstations, 201

    def delete(self, trainstations_id):
        abort_if_id_notExists(trainstations_id)
        trainstation = TrainstationModel(id=trainstations_id, name=args['name'], address=args['address'])

        db.session.delete(trainstation)
        db.session.commit()
        return '', 204
