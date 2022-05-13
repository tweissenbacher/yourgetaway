from dataclasses import fields
from marshmallow_sqlalchemy.fields import Nested
import sqlalchemy
from sqlalchemy.sql import func

from .. import db, ma


class Section(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    from_station_id = db.Column(db.Integer())
    to_station_id = db.Column(db.Integer())
    duration = db.Column(db.Integer())
    line_id = db.Column(db.Integer(), db.ForeignKey("line.id"))

    def __init__(self, id, from_station, to_station, duration):
        self.id = id
        self.from_station = from_station
        self.to_station = to_station
        self.duration = duration


class SectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Section
        ordered = True


section_schema = SectionSchema()
sections_schema = SectionSchema(many=True)


class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    price = db.Column(db.Integer())
    # note = db.Column(db.String(10000))
    # date = db.Column(db.DateTime(timezone=True), default=func.now())
    sections = db.relationship(
        "Section", backref=db.backref("linep"), lazy="dynamic"
    )  # ??


class LineSchema(ma.SQLAlchemyAutoSchema):
    sections = Nested(SectionSchema, many=True)

    class Meta:
        model = Line
        ordered = True
        fields = ("id", "description", "price", "note", "sections")


line_schema = LineSchema()
lines_schema = LineSchema(many=True)
