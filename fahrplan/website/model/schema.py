from marshmallow import fields
from marshmallow_sqlalchemy.fields import Nested

from website.model.line import Line, LineSection, Recurrence, Route, Section, Trip
from website.model.user import User
from .. import db, ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        # include_fk = True
        ordered = True
        fields = ("id", "email", "first_name", "last_name", "birthday")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


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


class RouteSchema(ma.SQLAlchemyAutoSchema):
    sections = Nested(SectionSchema, many=True)

    class Meta:
        model = Route
        ordered = True
        fields = ("id", "name", "sections")


route_schema = RouteSchema()
routes_schema = RouteSchema(many=True)


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
        if (obj.mon and obj.tue and obj.wed and obj.thu and obj.fri == 1) and (
            obj.sat and obj.sun == 0
        ):
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
            "id",
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


class TripSchema(ma.SQLAlchemyAutoSchema):
    recurrence = Nested(RecurrenceSchema)  # many=False)
    personell = Nested(UserSchema, many=True)

    class Meta:
        model = Trip
        ordered = True
        fields = (
            "id",
            "line_parent.descr",
            "note",
            "departure",
            "train_id",
            "price",
            "recurrence",
            "personell",
        )


trip_schema = TripSchema()
trips_schema = TripSchema(many=True)


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


class LineSchema(ma.SQLAlchemyAutoSchema):
    sections = Nested(LineSectionSchema, many=True)
    trips = Nested(TripSchema, many=True)

    class Meta:
        model = Line
        ordered = True
        fields = ("id", "descr", "route_id", "note", "sections", "trips")


line_schema = LineSchema()
lines_schema = LineSchema(many=True)


class UserWithTripsSchema(ma.SQLAlchemyAutoSchema):
    trips = Nested(TripSchema, many=True)

    class Meta:
        model = User
        # include_fk = True
        ordered = True
        fields = ("id", "email", "first_name", "last_name", "birthday", "trips")


user_with_trips_schema = UserWithTripsSchema()
users_with_trips_schema = UserWithTripsSchema(many=True)