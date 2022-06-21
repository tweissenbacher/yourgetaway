from db import db

# serves the management of admins (storage of admin email)
class AdminModel (db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))

    def __init__(self, email):
        self.email = email

    # finds admin per email
    @classmethod
    def find_admin(cls, email):
        return cls.query.filter_by(email = email).first()

    # saves admin to db
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()