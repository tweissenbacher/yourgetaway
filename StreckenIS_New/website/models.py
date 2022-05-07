from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')


class TrainstationModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Trainstations(name {self.name}, address {self.address})"

    # @classmethod
    # def find_all(cls):
    #   return cls.query.all();


#sections = db.table('secondTable',
                    #db.Column('section_id', db.Integer, db.ForeignKey('section_model.id'), primary_key=True),
                    #db.Column('route_id', db.Integer, db.ForeignKey('route_model.id'), primary_key=True)
                    #)


class SectionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(100), nullable=False)
    end = db.Column(db.String(100), nullable=False)
    track = db.Column(db.String(100), nullable=False)
    fee = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Sections(start {self.start}, end {self.end}, track {self.track}, fee {self.fee}, time {self.time})"


class RouteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start = db.Column(db.String(100), nullable=False)
    end = db.Column(db.String(100), nullable=False)
    #route_sections = db.relationship('SectionModel', secondary=sections, lazy='subquery',
                                     #backref=db.backref('routes', lazy=True))
    route_sections = db.Column(db.String(100), nullable=False)
    warnings = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Routes(name {self.name}, start {self.start}, end {self.end}" \
               f", route_sections {self.route_sections}, warnings {self.warnings}) "
