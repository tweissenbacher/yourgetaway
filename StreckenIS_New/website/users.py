from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

from . import db
from website.models import User

user = {
    "0": {"email": "someonegmail.com", "first_name": "Thomas", "password": "somePW"},
}

users_put_args = reqparse.RequestParser()
users_put_args.add_argument("email", type=str, help="Email", required=True)
users_put_args.add_argument("first_name", type=str, help="First name", required=True)
users_put_args.add_argument("password", type=str, help="password", required=True)

users_update_args = reqparse.RequestParser()
users_update_args.add_argument("email", type=str, help="update_Email")
users_update_args.add_argument("first_name", type=str, help="update_First name")
users_update_args.add_argument("password", type=str, help="update_password")

users_resource_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'first_name': fields.String,
    'password': fields.String
}


class Users(Resource):
    @marshal_with(users_resource_fields)
    def get(self):
        all_users= User.query.all()
        return all_users


class User(Resource):
    @marshal_with(users_resource_fields)  # to define how to serialize it
    def get(self, user_id):
        result = User.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="Couldnt find ID-Warning")
        return result

    @marshal_with(users_resource_fields)
    def patch(self, user_id):
        args = users_update_args.parse_args()
        result = User.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="Warning doesnt exist, cannot update")

        if args['email']:
            result.users = args['email']
        if args['first_name']:
            result.users = args['first_name']
        if args['password']:
            result.users = args['password']

        db.session.commit()

        return result

    @marshal_with(users_resource_fields)  # to define how to serialize it
    def put(self, user_id):
        # abort_if_station_Exists(user_id)
        args = users_put_args.parse_args()
        result = User.query.filter_by(id=user_id).first()
        if result:
            abort(409, message="Id taken...")
        us = User(id=user_id, email=args['email'], first_name=args['first_name'], password=args['password'])
        db.session.add(us)
        db.session.commit()
        return us, 201
