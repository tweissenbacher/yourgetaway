from dataclasses import fields
from marshmallow_sqlalchemy.fields import Nested
import sqlalchemy
from sqlalchemy.sql import func

from .. import db, ma


class Section(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    start = db.Column(db.String(100))
    end = db.Column(db.String(100))
    duration = db.Column(db.Integer())
    line_id = db.Column(db.Integer(), db.ForeignKey("line.id"))


class SectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Section


section_schema = SectionSchema()
sections_schema = SectionSchema(many=True)


class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    price = db.Column(db.Integer())
    # note = db.Column(db.String(10000))
    # date = db.Column(db.DateTime(timezone=True), default=func.now())
    sections = db.relationship(
        "Section"
    )  # , backref=db.backref("line"))#, lazy="subquery")


class LineSchema(ma.SQLAlchemyAutoSchema):
    sections = Nested(SectionSchema, many=True)

    class Meta:
        model = Line
        ordered = True
        fields = ("id", "description", "price", "note", "sections")


line_schema = LineSchema()
lines_schema = LineSchema(many=True)
