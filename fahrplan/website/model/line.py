# from dataclasses import fields
from flask_login import UserMixin
from marshmallow_sqlalchemy.fields import Nested

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Table, Time
from sqlalchemy.orm import relationship, backref, object_session
from sqlalchemy.sql import func

from .. import db, ma
from .user import user_trip

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
    fee = Column(Integer())

    def __init__(self, id, from_station, to_station, duration):
        self.id = id
        self.from_station = from_station
        self.to_station = to_station
        self.duration = duration

    def __repr__(self) -> str:
        return f"Section {self.id}: {self.from_station_name} to {self.to_station_name}"


# *
# * Strecke (Westbahn,..)
class Route(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    # sections = relationship("Section", backref=backref("route"), lazy="joined")  # ??
    # https://www.reddit.com/r/flask/comments/97p7gc/help_jinja_template_error_with_sqlalchemy/
    sections = relationship(
        "Section",
        backref=backref("route"),
        lazy="joined",
        order_by="Section.id",
    )


# *
# * Durchführungintervall
# ?? stundenintervall?? time_start, time_end, interval (h)
class Recurrence(db.Model):
    # ? PK: keine ID stattdessen kombi aus daten (redundanz reduzieren)
    id = Column(Integer(), primary_key=True)
    date_start = Column(Date())
    date_end = Column(Date())
    mon = Column(Integer())
    tue = Column(Integer())
    wed = Column(Integer())
    thu = Column(Integer())
    fri = Column(Integer())
    sat = Column(Integer())
    sun = Column(Integer())

    # def __init__(self, date_start, date_end, mon, tue, wed, thu, fri, sat, sun):
    #     self.date_start = date_start
    #     self.date_end = date_end
    #     self.mon = mon
    #     self.tue = tue
    #     self.wed = wed
    #     self.thu = thu
    #     self.fri = fri
    #     self.sat = sat
    #     self.sun = sun


class Trip(db.Model):
    id = Column(Integer(), primary_key=True)
    line_id = Column(Integer(), ForeignKey("line.id"))
    
    departure = Column(Time())  # ? auslagern in recurence? stundenintervall?
    price = Column(Integer())
    note = Column(String(100))
    train_id = Column(Integer())
    # train_name =
    personell = relationship(
        "User",
        secondary=user_trip,
        # cascade="all, delete-orphan",
        lazy="joined",
        back_populates="trips",
        # backref=backref("trips", lazy="joined"),
        # order_by="User.id",
    )

    recurrence_id = Column(Integer(), ForeignKey("recurrence.id"))
    recurrence = relationship("Recurrence", uselist=False)
    # recurrence_date_start = Column(Date(), ForeignKey("recurrence.date_start"))  #? for trips order_by date_start ?
    # recurrence_date_start =

    # @property  # https://docs.sqlalchemy.org/en/14/orm/join_conditions.html#building-query-enabled-properties
    # def recurrence_date_start(self):
    #     return object_session(self).query(Recurrence).with_parent(self).first()

    def __repr__(self) -> str:
        return f"Trip {self.id}:\
            id:{self.id} \
            lineid:{self.line_id} \
                dep:{self.departure} \
                    price:{self.price}\
                        note:{self.note} \
                            trainid:{self.train_id} \
                                personell:({self.personell}\
                                    recurrence:({self.recurrence}"


# *
# * association: line with selected sections and arrival time (=sum of prev durations)
class LineSection(db.Model):
    line_id = Column(Integer(), ForeignKey("line.id"), primary_key=True)
    section_id = Column(Integer(), ForeignKey("section.id"), primary_key=True)
    section = relationship("Section")
    arrival = Column(Integer())
    # line = relationship("Line", back_populates="")
    # order = Column(Integer()) # ordered by arrival


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
        cascade="all, delete-orphan",
        lazy="joined",
        order_by="LineSection.arrival",
    )
    trips = relationship(
        "Trip",
        backref=backref("line_parent", lazy="joined"),
        lazy="joined",
        # order_by="Trip.recurrence_date_start",  # ? how?
    )
    # https://docs.sqlalchemy.org/en/14/orm/backref.html
    # https://www.reddit.com/r/flask/comments/97p7gc/help_jinja_template_error_with_sqlalchemy/

    def update(self, descr, price, note, sections):
        self.descr = descr
        self.price = price
        self.note = note
        self.sections = sections
