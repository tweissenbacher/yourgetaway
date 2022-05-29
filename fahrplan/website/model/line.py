# from dataclasses import fields
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import fields

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from .. import db, ma


# *
# * Abschnitt
class Section(db.Model):
    id = Column(Integer(), primary_key=True)
    from_station = Column(Integer())
    to_station = Column(Integer())
    from_station_name = Column(String(100))
    to_station_name = Column(String(100))
    duration = Column(Integer())
    # line_id = Column(Integer(), ForeignKey("line.id"))
    route_id = Column(Integer(), ForeignKey("route.id"))  # ? del

    def __init__(self, id, from_station, to_station, duration):
        self.id = id
        self.from_station = from_station
        self.to_station = to_station
        self.duration = duration

    def __repr__(self) -> str:
        return f"Section {self.id}: {self.from_station_name} to {self.to_station_name}"


class SectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Section
        ordered = True
        fields = (
            "id",
            "from_station",
            "to_station",
            "from_station_name",
            "to_station_name",
            "duration",
        )


section_schema = SectionSchema()
sections_schema = SectionSchema(many=True)


# *
# * Strecke (Westbahn,..)
class Route(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    sections = relationship("Section", backref=backref("route"), lazy="joined")  # ??
    # https://www.reddit.com/r/flask/comments/97p7gc/help_jinja_template_error_with_sqlalchemy/


class RouteSchema(ma.SQLAlchemyAutoSchema):
    sections = Nested(SectionSchema, many=True)

    class Meta:
        model = Route
        ordered = True
        fields = ("id", "name", "sections")


route_schema = RouteSchema()
routes_schema = RouteSchema(many=True)


# *
# * Durchführungintervall
    # ?? stundenintervall?? time_start, time_end, interval (h)
class Recurrence(db.Model):
    id = Column(Integer(), primary_key=True)  # ? PK: keine ID stattdessen kombi aus daten (redundanz reduzieren)
    date_start = Column(Date())
    date_end = Column(Date())
    mon = Column(Integer())
    tue = Column(Integer())
    wed = Column(Integer())
    thu = Column(Integer())
    fri = Column(Integer())
    sat = Column(Integer())
    sun = Column(Integer())

    def __init__(self, date_start, date_end, mon, tue, wed, thu, fri, sat, sun):
        self.date_start = date_start
        self.date_end = date_end
        self.mon = mon
        self.tue = tue
        self.wed = wed
        self.thu = thu
        self.fri = fri
        self.sat = sat
        self.sun = sun


class RecurrenceSchema(ma.SQLAlchemyAutoSchema):

    daily = fields.Method("is_daily")
    workdays = fields.Method("is_workdays")
    weekend = fields.Method("is_weekend")

    def is_daily(self, obj):
        if (
            obj.mon
            and obj.tue
            and obj.wed
            and obj.thu
            and obj.fri
            and obj.sat
            and obj.sun == 1
        ):
            return "true"
        else:
            return "false"

    def is_workdays(self, obj):
        if obj.mon and obj.tue and obj.wed and obj.thu and obj.fri == 1:
            return "true"
        else:
            return "false"

    def is_weekend(self, obj):
        if obj.sat and obj.sun == 1:
            return "true"
        else:
            return "false"

    class Meta:
        model = Recurrence
        ordered = True
        fields = (
            "date_start",
            "date_end",
            "daily",
            "workdays",
            "weekend",
            "mon",
            "tue",
            "wed",
            "thu",
            "fri",
            "sat",
            "sun",
        )


recurrence_schema = RecurrenceSchema(many=False)
# intervals_schema = IntervalSchema(many=True)


class Trip(db.Model):
    id = Column(Integer(), primary_key=True)
    note = Column(String(100))
    departure = Column(Time())  # ? auslagern in recurence? stundenintervall?
    train_id = Column(Integer())
    # train_name =
    price = Column(Integer())
    recurrence_id = Column(Integer(), ForeignKey("recurrence.id"))
    recurrence = relationship("Recurrence", uselist=False)
    # recurrence_date_start = Column(Date(), ForeignKey("recurrence.date_start"))  #? for trips order_by date_start ?
    line_id = Column(Integer(), ForeignKey("line.id"))


class TripSchema(ma.SQLAlchemyAutoSchema):
    recurrence = Nested(RecurrenceSchema)  # many=False)

    class Meta:
        model = Trip
        ordered = True
        fields = (
            "line_parent.descr",
            "note",
            "departure",
            "train_id",
            "price",
            "recurrence",
        )


trip_schema = TripSchema()
trips_schema = TripSchema(many=True)


# *
# * association: line with selected sections and arrival time (=sum of prev durations)
class LineSection(db.Model):
    line_id = Column(Integer(), ForeignKey("line.id"), primary_key=True)
    section_id = Column(Integer(), ForeignKey("section.id"), primary_key=True)
    arrival = Column(Integer())
    # line = relationship("Line", back_populates="")
    section = relationship("Section")

    # order = Column(Integer()) # ordered by arrival


class LineSectionSchema(ma.SQLAlchemyAutoSchema):

    section = Nested(SectionSchema)

    class Meta:
        model = LineSection
        ordered = True
        fields = (
            "line_id",
            "section_id",
            "section",
            "arrival",
            "line_parent.price",
        )


line_section_schema = LineSectionSchema()
line_sections_schema = LineSectionSchema(many=True)


# *
# * Fahrtstrecke   # Linie Traunexpress, Linie S4, ...
class Line(db.Model):
    id = Column(Integer, primary_key=True)
    descr = Column(String(100))
    price = Column(Integer())
    route_id = Column(Integer(), ForeignKey("route.id"))
    route = relationship("Route")
    note = Column(String(1000))
    sections = relationship(
        "LineSection",
        backref=backref("line_parent", lazy="joined"),
        lazy="joined",
        order_by="LineSection.arrival",
    )
    trips = relationship(
        "Trip",
        backref=backref("line_parent", lazy="joined"),
        lazy="joined",
        # order_by="Trip.recurrence.date_start",  # ? how?
    )
    # https://docs.sqlalchemy.org/en/14/orm/backref.html
    # https://www.reddit.com/r/flask/comments/97p7gc/help_jinja_template_error_with_sqlalchemy/


class LineSchema(ma.SQLAlchemyAutoSchema):
    sections = Nested(LineSectionSchema, many=True)
    trips = Nested(TripSchema, many=True)

    class Meta:
        model = Line
        ordered = True
        fields = ("id", "descr", "route_id", "note", "sections", "trips")


line_schema = LineSchema()
lines_schema = LineSchema(many=True)
