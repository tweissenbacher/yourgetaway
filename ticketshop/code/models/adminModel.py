from db import db

class AdminModel (db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))

    def __init__(self, email):
        self.email = email

    @classmethod
    def find_admin(cls, email):
        return cls.query.filter_by(email = email).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()