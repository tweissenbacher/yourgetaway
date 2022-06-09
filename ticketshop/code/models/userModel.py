from db import db

from models.adminModel import AdminModel
from werkzeug.security import generate_password_hash

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(100))
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    image_url = db.Column(db.String(100))
    birthday = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean)
    tickets = db.relationship("TicketModel")

    def __init__(self, email, password, firstname, lastname, image_url, birthday):
        self.email = email
        hashed_password = generate_password_hash(password)
        self.password = hashed_password
        self.firstname = firstname
        self.lastname = lastname
        self.image_url = image_url
        self.birthday = birthday
        self.check_if_admin();

    def json(self):
        return {"email": self.email, "password": self.password,
                "firstname": self.firstname, "lastname": self.lastname, "birthday": self.birthday, "is_admin": self.is_admin}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def check_if_admin(self):
        user = AdminModel.find_admin(self.email)
        if user:
            self.is_admin = True
        else:
            self.is_admin = False

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email= email).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id = user_id).first()


