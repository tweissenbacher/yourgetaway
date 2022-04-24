from db import db

from models.adminModel import AdminModel

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(100))
    password = db.Column(db.String(100))
    ist_admin = db.Column(db.Boolean)

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.check_if_admin();

    def json(self):
        return {"email": self.email, "password": self.password, "ist_admin": self.ist_admin}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def check_if_admin(self):
        if AdminModel.find_admin(self.email):
            self.ist_admin = True
        else:
            self.ist_admin = False

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email= email).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id = user_id).first()


