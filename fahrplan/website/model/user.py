from flask_login import UserMixin
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.sql import func
from .. import db, ma


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    birthday = db.Column(db.Date, default=func.now())
    admin = db.Column(db.Integer, default=0)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        # include_fk = True
        ordered = True
        fields = ("email", "first_name", "last_name", "birthday")


user_schema = UserSchema()
users_schema = UserSchema(many=True)
