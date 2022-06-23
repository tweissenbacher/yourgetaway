from datetime import datetime, timedelta
from pydoc import resolve
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Table, Time, or_
import sqlalchemy
from sqlalchemy.orm import relationship, backref, object_session
from sqlalchemy.sql import func
from sqlalchemy.ext.associationproxy import association_proxy

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
    route_id = Column(Integer(), ForeignKey("route.id"))
    fee = Column(Integer())
    track = Column(String())

    def __repr__(self) -> str:
        return f"Section {self.id}: {self.from_station_name} to {self.to_station_name}"

    @classmethod
    def dict_to_obj(self, sectiondata):
        return Section(
            id=int(sectiondata["id"]),
            from_station=int(sectiondata["start"]["id"]),
            to_station=int(sectiondata["end"]["id"]),
            from_station_name=sectiondata["start"]["name"],
            to_station_name=sectiondata["end"]["name"],
            duration=int(sectiondata["time"]),
            fee=int(sectiondata["fee"]),
            track=sectiondata["track"],
        )


# *
# * Strecke (Westbahn,..)
class Route(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    # https://www.reddit.com/r/flask/comments/97p7gc/help_jinja_template_error_with_sqlalchemy/
    sections = relationship(
        "Section",
        backref=backref("route"),
        lazy="joined",
        order_by="Section.id",
    )

    @classmethod
    def dict_to_obj(self, routedata):
        id = routedata["id"]
        name = str(routedata["name"])
        # print(id)
        routesectiondata = routedata["route_sections"]
        sections = []
        for s in routesectiondata:
            s = Section.dict_to_obj(s)
            db_section = Section.query.get(s.id)
            print(db_section)
            if not db_section:
                db.session.add(s)

            # sections.append(Section.dict_to_obj(s))
        return Route(id=id, name=name, sections=sections)


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

    date_start = association_proxy('recurrence', 'date_start')
    date_end = association_proxy('recurrence', 'date_end')


    def __repr__(self) -> str:
        return (
            f" Trip {self.id}:"
            f" id:{self.id}"
            f" lineid:{self.line_id}"
            f" dep:{self.departure}"
            f" price:{self.price}"
            f" note:{self.note}"
            f" trainid:{self.train_id}"
            f" personell:({self.personell}"
            f" recurrence:({self.recurrence}"
        )

    def is_train_in_use(self, train_id):
        trips_with_train = Trip.query.filter(
            Trip.train_id == train_id,
            # or_(
            #     (
            #         Trip.recurrence.date_start >= self.recurrence.date_end,
            #         Trip.recurrence.date_end <= self.recurrence.date_start,
            #     ),
            #     (
            # self.date_end >= Trip.date_start, 
            # self.date_start <= Trip.date_end,
            #     ),
            # ),

            self.departure == Trip.departure
        )
        print(trips_with_train)
        return trips_with_train

    # @classmethod
    def is_trip_on_day(self, date):
        week = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        day = week[date.weekday()]
        print(day)
        return (
            (self.recurrence.mon == 1 and day == "mon")
            or (self.recurrence.tue == 1 and day == "tue")
            or (self.recurrence.wed == 1 and day == "wed")
            or (self.recurrence.thu == 1 and day == "thu")
            or (self.recurrence.fri == 1 and day == "fri")
            or (self.recurrence.sat == 1 and day == "sat")
            or (self.recurrence.sun == 1 and day == "sun")
        )

    def get_resolved_dict(self, date):
        return {
            "rec_id": self.recurrence.id,
            "note": self.note,
            "date": date,
            "line": self.line_parent,
            "departure": self.departure,
            "arrival": (
                datetime(
                    year=date.year,
                    month=date.month,
                    day=date.day,
                    hour=self.departure.hour,
                    minute=self.departure.minute,
                )
                + timedelta(minutes=self.line_parent.sections[-1].arrival)
            ).time(),
            "personell": self.personell,
            "train_id": self.train_id,
        }

    def get_resolved_all_dict(self):
        start_date = self.recurrence.date_start
        end_date = self.recurrence.date_end
        current_date = start_date
        resolved = []
        while current_date <= end_date:
            if self.is_trip_on_day(current_date):
                resolved.append(self.get_resolved_dict(current_date))
            current_date += timedelta(days=1)
        return resolved


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
