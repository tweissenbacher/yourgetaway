from email.policy import default
from flask_wtf import FlaskForm
from wtforms import (
    FormField,
    SubmitField,
    SelectMultipleField,
    BooleanField,
    IntegerField,
    DateField,
    TimeField,
    RadioField,
    SelectField,
    TextAreaField,
    StringField,
)
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.orm import model_form
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from website.model.line import Recurrence, Trip
from .. import db


# class


class TripCreateForm(FlaskForm):
    departure = TimeField("Abfahrtszeit:", validators=[DataRequired()], format="HH:MM")
    price = IntegerField("Preis:", validators=[DataRequired()])
    note = StringField("Notiz:", validators=[DataRequired()])

    train_id = SelectField("Zug:", validators=[DataRequired()], choices=[])

    personell = SelectMultipleField("Personal:")

    # recurrence = QuerySelectField


# ORMTripCreateForm = model_form(Trip, db.session, exclude=["line_id", "id"])


class RecurrenceChoiceForm(FlaskForm):
    recurrence = RadioField(
        "", choices=[(1, "Einmalig"), (2, "Intervall")], default=1, coerce=int
    )


class SingleForm(FlaskForm):
    date = DateField("Datum:", validators=[DataRequired()])


class RecurrenceForm(FlaskForm):
    date_start = DateField("Startdatum:", validators=[DataRequired()])
    date_end = DateField("Enddatum:", validators=[DataRequired()])
    mon = BooleanField("Montag:", default=1, validators=[])
    tue = BooleanField("Dienstag:", default=1, validators=[])
    wed = BooleanField("Mittwoch:", default=1, validators=[])
    thu = BooleanField("Donnerstag:", default=1, validators=[])
    fri = BooleanField("Freitag:", default=1, validators=[])
    sat = BooleanField("Samstag:", default=1, validators=[])
    sun = BooleanField("Sonntag:", default=1, validators=[])


class CompleteTripCreateForm(FlaskForm):
    departure = TimeField("Abfahrtszeit:", validators=[DataRequired()], format="HH:MM")
    recurrence_choice = FormField(RecurrenceChoiceForm)
    recurrence = FormField(RecurrenceForm, default=lambda: Recurrence())
    trip = FormField(TripCreateForm, default=lambda: Trip())

    proceed1 = SubmitField("Weiter")
    proceed2 = SubmitField("Weiter")
    proceed3 = SubmitField("Weiter")
    submit = SubmitField("Absenden!")


# class TripCreateForm(FlaskForm):
#     departure = TimeField("Abfahrtszeit:", validators=[DataRequired()], format="HH:MM")
#     price = IntegerField("Preis:", validators=[DataRequired()])
#     note = StringField("Notiz:", validators=[DataRequired()])

#     train_id = SelectField("Zug:", validators=[DataRequired()], choices=[])

#     personell = SelectMultipleField("Personal:")

#     # recurrence = QuerySelectField


# # ORMTripCreateForm = model_form(Trip, db.session, exclude=["line_id", "id"])

# class RecurrenceChoiceForm(FlaskForm):
#     recurrence = RadioField('', choices=[
#         (1,'Einmalig'), (2,'Intervall')],
#         default=1, coerce=int)


# class RecurrenceForm(FlaskForm):
#     date_start = DateField("Startdatum:", validators=[DataRequired()])
#     date_end = DateField("Enddatum:", validators=[DataRequired()])
#     mon = BooleanField("Montag:", default='checked', validators=[])
#     tue = BooleanField("Dienstag:", default=True, validators=[])
#     wed = BooleanField("Mittwoch:", default=1, validators=[])
#     thu = BooleanField("Donnerstag:", default=1, validators=[])
#     fri = BooleanField("Freitag:", default=1, validators=[])
#     sat = BooleanField("Samstag:", default=1, validators=[])
#     sun = BooleanField("Sonntag:", default=1, validators=[])


# class CompleteTripCreateForm(FlaskForm):
#     departure = TimeField("Abfahrtszeit:", validators=[DataRequired()], format="HH:MM")
#     recurrence_choice = FormField(RecurrenceChoiceForm)
#     recurrence = FormField(RecurrenceForm, default=lambda: Recurrence())
#     trip = FormField(TripCreateForm, default=lambda: Trip())

#     proceed1 = SubmitField("Weiter")
#     proceed2 = SubmitField("Weiter")
#     proceed3 = SubmitField("Weiter")
#     submit = SubmitField("Absenden!")
