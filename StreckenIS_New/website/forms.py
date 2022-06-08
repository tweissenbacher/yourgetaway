from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, DateField, BooleanField
from wtforms.validators import DataRequired, Length


class EditProfileForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[Length(min=3, max=150)])
    email = StringField('email', validators=[Length(min=3, max=150)])
    password1 = StringField('password1', validators=[Length(min=3, max=150)])
    password2 = StringField('password2', validators=[Length(min=3, max=150)])
    birthday = DateField('birthday')
    admin = BooleanField('admin')
    submit = SubmitField('submit')


class EditTrainstationForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    address = StringField('address', validators=[Length(min=3, max=150)])
    submit = SubmitField('submit')


class EditSectionForm(FlaskForm):
    start = StringField('start', validators=[DataRequired()])
    end = StringField('end', validators=[Length(min=3, max=150)])
    track = StringField('track', validators=[Length(min=3, max=150)])
    fee = StringField('fee')
    time = StringField('time')
    submit = SubmitField('submit')


class EditRouteForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    start = StringField('start', validators=[Length(min=3, max=150)])
    end = StringField('end', validators=[Length(min=3, max=150)])
    route_sections = StringField('route_sections', validators=[Length(min=3, max=150)])
    v_max = StringField('v_max')
    submit = SubmitField('submit')


class EditWarningsForm(FlaskForm):
    warnings = StringField('warnings', validators=[DataRequired()])
    submit = SubmitField('submit')
