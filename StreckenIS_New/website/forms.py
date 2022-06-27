from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, DateField, BooleanField, EmailField, widgets
from wtforms.validators import DataRequired, Length, Email, InputRequired, EqualTo, email_validator
from wtforms.widgets import PasswordInput


# WTForm to edit a user (employee view)
class EditEmpUserForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[Length(min=3, max=150)])
    email = EmailField('email', validators=email_validator)
    password = StringField('password required to save your changes', validators=[InputRequired()],
                           widget=PasswordInput(hide_value=True))
    birthday = DateField('birthday')
    submit = SubmitField('submit')


# WTForm to edit a user (admin view)
class EditUserForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[Length(min=3, max=150)])
    email = EmailField('email', validators=email_validator)
    password = PasswordField('password', widget=PasswordInput(hide_value=False))
    birthday = DateField('birthday')
    admin = BooleanField('admin')
    submit = SubmitField('submit')


# WTForm to edit a trainstation (admin view)
class EditTrainstationForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    address = StringField('address', validators=[Length(min=3, max=150)])
    submit = SubmitField('submit')


# WTForm to edit a section (admin view)
class EditSectionForm(FlaskForm):
    track = StringField('track', validators=[Length(min=3, max=150)])
    fee = IntegerField('fee')
    time = IntegerField('time')
    submit = SubmitField('submit')


# WTForm to edit a route (admin view)
class EditRouteForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    v_max = IntegerField('max_speed')
    submit = SubmitField('submit')


# WTForm to edit a warning (admin view)
class EditWarningsForm(FlaskForm):
    warnings = StringField('warnings', validators=[DataRequired()])
    submit = SubmitField('submit')
