from datetime import date, time
from flask_login import UserMixin
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.sql import func

from .. import db, ma

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Table, Time
from sqlalchemy.orm import relationship, backref, object_session


user_trip = db.Table(
    "user_trip",
    Column("user_id", Integer(), ForeignKey("user.id"), primary_key=True),
    Column("trip_id", Integer(), ForeignKey("trip.id"), primary_key=True),
)


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True)
    password = Column(String(150))
    first_name = Column(String(150))
    last_name = Column(String(150))
    birthday = Column(Date, default=func.now())
    admin = Column(Integer, default=0)
    trips = relationship(
        "Trip",
        secondary=user_trip,
        # cascade="all, delete-orphan",
        lazy="joined",
        back_populates="personell",
        # backref=backref("trip_user", lazy="joined"),
        # order_by="UserTrip.arrival",
    )

    def __repr__(self) -> str:
        return f"{self.last_name} {self.first_name}"

    def update(self, email, first_name, last_name, admin, password1=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        # self.birthday=birthday
        if admin == "on":
            self.admin = 1
        else:
            self.admin = 0
        if password1 is not None:
            self.password = password1

    def is_blocked(self, departure: time, dt_start: date, dt_end: date):
        for day in range(dt_start.toordinal(), dt_end.toordinal()):
            if self.trips:
                for trip in self.trips:
                    print(self.first_name)
                    return (
                        departure == trip.departure
                        and day >= trip.recurrence.date_start
                        and day <= trip.recurrence.date_end
                    )
