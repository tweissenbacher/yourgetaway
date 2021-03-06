from flask_login import UserMixin
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.sql import func

from . import db, ma


##########
# Models #
##########


# Additional Model to create Notes for Users (not implemented)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    birthday = db.Column(db.Date, default=func.now())
    admin = db.Column(db.Boolean, default=False)


# Trainstation Model
class TrainstationModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Trainstations(name {self.name}, address {self.address})"


# Section Model
class SectionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.relationship('TrainstationModel', foreign_keys='SectionModel.start_id')
    start_id = db.Column(db.Integer, db.ForeignKey('trainstation_model.id'))
    end = db.relationship('TrainstationModel', foreign_keys='SectionModel.end_id')
    end_id = db.Column(db.Integer, db.ForeignKey('trainstation_model.id'))
    track = db.Column(db.String(100), nullable=False)
    fee = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    section_warnings = db.relationship('WarningModel',
                                       lazy='joined',
                                       backref=db.backref('section', lazy='joined'))

    def __repr__(self):
        return f"Sections(start {self.start}, end {self.end}, track {self.track}, " \
               f"fee {self.fee}, time {self.time}, section_warnings {self.section_warnings}"


# Association between Section and Route (Many-to-Many Relationship)
sections = db.Table('sections',
                    db.Column('section_model_id', db.Integer, db.ForeignKey('section_model.id'), primary_key=True),
                    db.Column('route_model_id', db.Integer, db.ForeignKey('route_model.id'), primary_key=True)
                    )


# Route Model
class RouteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start = db.relationship('TrainstationModel', foreign_keys='RouteModel.start_id')
    start_id = db.Column(db.Integer, db.ForeignKey('trainstation_model.id'))
    end = db.relationship('TrainstationModel', foreign_keys='RouteModel.end_id')
    end_id = db.Column(db.Integer, db.ForeignKey('trainstation_model.id'))
    route_sections = db.relationship('SectionModel',
                                     secondary=sections,
                                     lazy='dynamic',
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


# Warning Model
class WarningModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warnings = db.Column(db.String(1000), nullable=False)
    warning_section = db.relationship('SectionModel', foreign_keys='WarningModel.section_id')
    section_id = db.Column(db.Integer, db.ForeignKey('section_model.id'))

    def __repr__(self):
        return {"id": self.id,
                "warnings": self.warnings,
                "warning_section": self.warning_section,
                "section_id": self.section_id
                }


#########################
# Schemas (Marshmallow) #
#########################

# User Schema for API
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        ordered = True
        fields = (
            "id",
            "email",
            "first_name",
            "last_name"
        )


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Trainstation Schema for API
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


# Warning Schema for API
class WarningSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WarningModel
        ordered = True
        fields = (
            "id",
            "warnings"
        )


warning_schema = WarningSchema()
warnings_schema = WarningSchema(many=True)


# Section Schema for API
class SectionSchema(ma.SQLAlchemyAutoSchema):
    start = Nested(TrainstationSchema)
    end = Nested(TrainstationSchema)
    section_warnings = Nested(WarningSchema, many=True)

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
            "time",
            "section_warnings"
        )


section_schema = SectionSchema()
sections_schema = SectionSchema(many=True)


# Route Schema for API
class RouteSchema(ma.SQLAlchemyAutoSchema):
    start = Nested(TrainstationSchema)
    end = Nested(TrainstationSchema)
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
            "v_max",
            "route_sections"
        )


route_schema = RouteSchema()
routes_schema = RouteSchema(many=True)


# Additional Warning Schema
# This workaround is necessary because WarningSchema
# is needed before in the SectionSchema and
# WarningSchemaSection has a nested SectionSchema
class WarningSchemaSection(ma.SQLAlchemyAutoSchema):
    section = Nested(SectionSchema)

    class Meta:
        model = WarningModel
        ordered = True
        fields = (
            "id",
            "warnings",
            "section_id",
            "section"
        )


warning_section_schema = WarningSchemaSection()
warnings_section_schema = WarningSchemaSection(many=True)
