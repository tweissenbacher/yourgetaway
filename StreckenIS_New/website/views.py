from sqlalchemy.dialects import mysql

from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import EditUserForm, EditTrainstationForm, EditSectionForm, EditRouteForm, EditWarningsForm, EditEmpUserForm
from .models import User, Note, TrainstationModel, SectionModel, RouteModel, WarningModel
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/all_users', methods=['GET', 'POST'])
def get_all_users():
    if request.method == 'POST':
        us_email = request.form.get('us_email')
        us_first_name = request.form.get('us_first_name')
        us_last_name = request.form.get('us_last_name')
        us_password1 = request.form.get('us_password1')
        us_password2 = request.form.get('us_password2')
        us_birthday = request.form.get('us_birthday')
        us_admin = request.form.get('us_admin')

        new_user = User.query.filter_by(email=us_email).first()
        if new_user:
            flash('Email already exists.', category='error')
        elif len(us_email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(us_first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif us_password1 != us_password2:
            flash('Passwords don\'t match.', category='error')
        elif len(us_password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=us_email, first_name=us_first_name, last_name=us_last_name, birthday=us_birthday,
                            admin=us_admin, password=generate_password_hash(us_password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash(' ---   user successfully created!   ---', category='success')
            return redirect('/all_users')

    all_users = User.query.all()

    return render_template("users.html", user=current_user, all_users=all_users)


@views.route('/edit_emp_user/<int:user_id>', methods=['GET', 'POST'])
def edit_emp_users(user_id):
    form = EditEmpUserForm()
    emp_user_edit = User.query.get(user_id)
    if form.validate_on_submit():
        emp_user_edit.first_name = form.first_name.data
        emp_user_edit.last_name = form.last_name.data
        emp_user_edit.email = form.email.data
        emp_user_edit.password = form.password.data
        emp_user_edit.password = generate_password_hash(emp_user_edit.password)
        emp_user_edit.birthday = form.birthday.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect('/all_users')
    elif request.method == 'GET':
        form.first_name.data = emp_user_edit.first_name
        form.last_name.data = emp_user_edit.last_name
        form.email.data = emp_user_edit.email
        form.password.data = emp_user_edit.password
        form.birthday.data = emp_user_edit.birthday
    return render_template('edit_emp_user.html', title='Edit Your Profile', user=current_user, form=form)


@views.route('/edit_users/<int:user_id>', methods=['GET', 'POST'])
def edit_users(user_id):
    form = EditUserForm()
    user_edit = User.query.get(user_id)
    if form.validate_on_submit():
        user_edit.first_name = form.first_name.data
        user_edit.last_name = form.last_name.data
        user_edit.email = form.email.data
        user_edit.password = form.password.data
        user_edit.password = generate_password_hash(user_edit.password)
        user_edit.birthday = form.birthday.data
        user_edit.admin = form.admin.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect('/all_users')
    elif request.method == 'GET':
        form.first_name.data = user_edit.first_name
        form.last_name.data = user_edit.last_name
        form.email.data = user_edit.email
        form.password.data = user_edit.password
        form.birthday.data = user_edit.birthday
        form.admin.data = user_edit.admin
    return render_template('edit_users.html', title='Edit Users', user=current_user, form=form)


@views.route('/delete-user', methods=['POST'])
def delete_user():
    user = json.loads(request.data)
    userId = user['userId']
    user = User.query.get(userId)
    if user == current_user:
        flash('You cannot delete the logged in user!', category='error')
    else:
        db.session.delete(user)
        db.session.commit()

    return jsonify({})


@views.route('/all_trainstations', methods=['GET', 'POST'])
def get_all_trainstations():
    if request.method == 'POST':
        ts_name = request.form.get('ts_name')
        ts_address = request.form.get('ts_address')

        trainstation = TrainstationModel.query.filter_by(name=ts_name).first()
        if trainstation:
            flash('Trainstation already exists!', category='error')
        elif len(ts_name) < 1:
            flash('Trainstation name must be greater than 1 character!', category='error')
        elif len(ts_address) < 1:
            flash('Trainstation address must be greater than 1 character!', category='error')
        else:
            new_trainstation = TrainstationModel(name=ts_name, address=ts_address)
            db.session.add(new_trainstation)
            db.session.commit()
            flash(' ---   trainstation successfully created!   ---', category='success')

    all_trainstations = TrainstationModel.query.all()

    return render_template("trainstations.html", user=current_user, all_trainstations=all_trainstations)


@views.route('/edit_trainstations/<int:trainstations_id>', methods=['GET', 'POST'])
def edit_trainstations(trainstations_id):
    form = EditTrainstationForm()
    trainstation_edit = TrainstationModel.query.get(trainstations_id)
    if form.validate_on_submit():
        trainstation_edit.name = form.name.data
        trainstation_edit.address = form.address.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect('/all_trainstations')
    elif request.method == 'GET':
        form.name.data = trainstation_edit.name
        form.address.data = trainstation_edit.address
    return render_template('edit_trainstations.html', title='Edit Trainstation', user=current_user, form=form)


@views.route('/delete-trainstation', methods=['POST'])
def delete_trainstation():
    trainstation = json.loads(request.data)
    trainstationId = trainstation['trainstationId']
    trainstation = TrainstationModel.query.get(trainstationId)
    if trainstation:
        db.session.delete(trainstation)
        db.session.commit()

    return jsonify({})


@views.route('/all_sections', methods=['GET', 'POST'])
def get_all_sections():
    if request.method == 'POST':
        #sec_id = request.form.get('sec_id')
        sec_start = request.form.get('sec_start')
        sec_end = request.form.get('sec_end')
        sec_track = request.form.get('sec_track')
        sec_fee = request.form.get('sec_fee')
        sec_time = request.form.get('sec_time')
        sec_warning = request.form.getlist('sec_warning')

        sec_start = TrainstationModel.query.get(sec_start)
        sec_end = TrainstationModel.query.get(sec_end)
        warnings = []

        if sec_start == sec_end:
            flash('section start cannot be the same as section end', category='error')
        elif len(sec_fee) > 3:
            flash('section fee cannot be over 3 digits', category='error')
        elif len(sec_time) > 3:
            flash('section time cannot be over 3 digits', category='error')
        else:
            # for w in sec_warning:
            # warning = WarningModel.query.get(w)
            # warnings.append(warning)

            new_section = SectionModel(start=sec_start, end=sec_end, track=sec_track, fee=sec_fee,
                                       time=sec_time, section_warnings=warnings)
            db.session.add(new_section)
            db.session.commit()
            flash(' ---   section successfully created!   ---', category='success')

    all_sections = SectionModel.query.all()
    all_trainstations = TrainstationModel.query.all()
    all_warnings = WarningModel.query.all()
    return render_template("sections.html", user=current_user, all_sections=all_sections,
                           all_trainstations=all_trainstations, all_warnings=all_warnings)


@views.route('/edit_sections/<int:sections_id>', methods=['GET', 'POST'])
def edit_sections(sections_id):
    form = EditSectionForm()
    sections_edit = SectionModel.query.get(sections_id)
    if form.validate_on_submit():
        sections_edit.track = form.track.data
        sections_edit.fee = form.fee.data
        sections_edit.time = form.time.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect('/all_sections')
    elif request.method == 'GET':
        form.track.data = sections_edit.track
        form.fee.data = sections_edit.fee
        form.time.data = sections_edit.time
    return render_template('edit_sections.html', title='Edit Sections', user=current_user, form=form)


@views.route('/delete-section', methods=['POST'])
def delete_section():
    section = json.loads(request.data)
    sectionId = section['sectionId']
    section = SectionModel.query.get(sectionId)
    if section:
        db.session.delete(section)
        db.session.commit()

    return jsonify({})


@views.route('/all_routes', methods=['GET', 'POST'])
def get_all_routes():
    if request.method == 'POST':
        rou_name = request.form.get('rou_name')
        rou_start = request.form.get('rou_start')
        rou_end = request.form.get('rou_end')
        rou_sections = request.form.getlist('rou_sections')
        rou_v_max = request.form.get('rou_v_max')

        rou_start = TrainstationModel.query.get(rou_start)
        rou_end = TrainstationModel.query.get(rou_end)
        sections = []

        if rou_start == rou_end:
            flash('route start cannot be the same as route end', category='error')
        elif len(rou_name) < 1:
            flash('route name cannot be empty', category='error')
        elif len(rou_v_max) < 1:
            flash('route max_speed cannot be empty', category='error')
        elif len(rou_v_max) != 3:
            flash('max_speed value need to be 3 digits long', category='error')
        else:
            for r_s in rou_sections:
                section = SectionModel.query.get(r_s)
                sections.append(section)

            new_route = RouteModel(name=rou_name, start=rou_start, end=rou_end, route_sections=sections,
                                   v_max=rou_v_max)
            db.session.add(new_route)
            db.session.commit()
            flash(' ---   route successfully created!   ---', category='success')

    all_routes = RouteModel.query.all()
    all_sections = SectionModel.query.all()
    all_trainstations = TrainstationModel.query.all()
    return render_template("routes.html", user=current_user, all_routes=all_routes, all_sections=all_sections,
                           all_trainstations=all_trainstations)


@views.route('/edit_routes/<int:routes_id>', methods=['GET', 'POST'])
def edit_routes(routes_id):
    form = EditRouteForm()
    routes_edit = RouteModel.query.get(routes_id)
    if form.validate_on_submit():
        routes_edit.name = form.name.data
        routes_edit.v_max = form.v_max.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect('/all_routes')
    elif request.method == 'GET':
        form.name.data = routes_edit.name
        form.v_max.data = routes_edit.v_max
    return render_template('edit_routes.html', title='Edit Routes', user=current_user, form=form)


@views.route('/delete-route', methods=['POST'])
def delete_route():
    route = json.loads(request.data)
    routeId = route['routeId']
    route = RouteModel.query.get(routeId)
    if route:
        db.session.delete(route)
        db.session.commit()

    return jsonify({})


@views.route('/all_warnings', methods=['GET', 'POST'])
def get_all_warnings():
    if request.method == 'POST':
        war_warnings = request.form.get('war_warnings')
        war_section = request.form.get('war_section')

        war_section = SectionModel.query.get(war_section)

        new_warning = WarningModel(warnings=war_warnings, warning_section=war_section)
        db.session.add(new_warning)
        db.session.commit()
        flash(' ---   warning successfully created!   ---', category='success')

    all_warnings = WarningModel.query.all()
    all_sections = SectionModel.query.all()
    return render_template("warnings.html", user=current_user, all_warnings=all_warnings, all_sections=all_sections)


@views.route('/edit_warnings/<int:warnings_id>', methods=['GET', 'POST'])
def edit_warnings(warnings_id):
    form = EditWarningsForm()
    warnings_edit = WarningModel.query.get(warnings_id)
    if form.validate_on_submit():
        warnings_edit.warnings = form.warnings.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect('/all_warnings')
    elif request.method == 'GET':
        form.warnings.data = warnings_edit.warnings
    return render_template('edit_warnings.html', title='Edit Warnings', user=current_user, form=form)


@views.route('/delete-warning', methods=['POST'])
def delete_warning():
    warning = json.loads(request.data)
    warningId = warning['warningId']
    warning = WarningModel.query.get(warningId)
    if warning:
        db.session.delete(warning)
        db.session.commit()

    return jsonify({})
