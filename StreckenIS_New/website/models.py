from marshmallow_sqlalchemy.fields import Nested
from marshmallow import fields

from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db, ma



class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    birthday = db.Column(db.Date, default=func.now())
    admin = db.Column(db.Boolean, default=False)


class TrainstationModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Trainstations(name {self.name}, address {self.address})"

class TrainstationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrainstationModel
        ordered = True
        fields = (
            "id",
            "name",
            "address"
        )


trainstation_schema = TrainstationSchema()
trainstations_schema = TrainstationSchema(many=True)


class SectionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.relationship('TrainstationModel', foreign_keys='SectionModel.start_id')
    start_id = db.Column(db.Integer, db.ForeignKey('trainstation_model.id'))
    end = db.relationship('TrainstationModel', foreign_keys='SectionModel.end_id')
    end_id = db.Column(db.Integer, db.ForeignKey('trainstation_model.id'))
    track = db.Column(db.String(100), nullable=False)
    fee = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Sections(start {self.start}, end {self.end}, track {self.track}, fee {self.fee}, time {self.time}"

class SectionSchema(ma.SQLAlchemyAutoSchema):
    start = Nested(TrainstationSchema, many=True)
    end = Nested(TrainstationSchema, many=True)
    class Meta:
        model = SectionModel
        ordered = True
        fields = (
            "id",
            "start",
            "start_id",
            "end",
            "end_id",
            "track",
            "fee",
            "time"
        )


section_schema = SectionSchema()
sections_schema = SectionSchema(many=True)

sections = db.Table('sections',
                    db.Column('section_model_id', db.Integer, db.ForeignKey('section_model.id'), primary_key=True),
                    db.Column('route_model_id', db.Integer, db.ForeignKey('route_model.id'), primary_key=True)
                    )


class RouteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start = db.relationship('TrainstationModel', foreign_keys='RouteModel.start_id')
    start_id = db.Column(db.Integer, db.ForeignKey('trainstation_model.id'))
    end = db.relationship('TrainstationModel', foreign_keys='RouteModel.end_id')
    end_id = db.Column(db.Integer, db.ForeignKey('trainstation_model.id'))
    route_sections = db.relationship('SectionModel', secondary=sections, lazy='dynamic',
                                     backref=db.backref('routes', lazy=True))
    v_max = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return {"id": self.id,
                "name": self.name,
                "start": self.start,
                "end": self.end,
                "route_sections": self.route_sections,
                "v_max": self.v_max
                }

class RouteSchema(ma.SQLAlchemyAutoSchema):
    start = Nested(TrainstationSchema, many=True)
    end = Nested(TrainstationSchema, many=True)
    route_sections = Nested(SectionSchema, many=True)
    class Meta:
        model = RouteModel
        ordered = True
        fields = (
            "id",
            "name",
            "start",
            "start_id",
            "end",
            "end_id",
            "route_sections",
            "v_max"
        )


route_schema = RouteSchema()
routes_schema = RouteSchema(many=True)

class WarningModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warnings = db.Column(db.String(1000), nullable=False)
    sections = db.relationship('SectionModel', foreign_keys='WarningModel.sections_id')
    sections_id = db.Column(db.Integer, db.ForeignKey('section_model.id'))

    def __repr__(self):
        return {"id": self.id,
                "warnings": self.warnings,
                "sections": self.sections,
                "sections_id": self.sections_id
                }

class WarningSchema(ma.SQLAlchemyAutoSchema):
    sections = Nested(SectionSchema, many=True)
    class Meta:
        model = WarningModel
        ordered = True
        fields = (
            "id",
            "warnings",
            "sections",
            "sections_id"
        )


warning_schema = WarningSchema()
warnings_schema = WarningSchema(many=True)