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

    def update(self, email, first_name, last_name, admin, password1=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        # self.birthday=birthday
        if admin == "on":
            self.admin = 1
        else:
            self.admin = 0
        if password1 is not None:
            self.password = password1

    # def update(self, email, first_name, last_name, admin):
    #     self.email=email
    #     self.first_name=first_name
    #     self.last_name=last_name
    #     # self.birthday=birthday
    #     if admin == "on":
    #         self.admin=1
    #     else:
    #         self.admin=0


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        # include_fk = True
        ordered = True
        fields = ("email", "first_name", "last_name", "birthday")


user_schema = UserSchema()
users_schema = UserSchema(many=True)
