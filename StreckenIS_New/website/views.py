from sqlalchemy.dialects import mysql

import website.trainstations
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
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
        us_password = request.form.get('us_password')

        new_user = User(email=us_email, first_name=us_first_name, password=us_password)
        db.session.add(new_user)
        db.session.commit()
        flash(' ---   user successfully created!   ---', category='success')

    all_users = User.query.all()

    return render_template("users.html", user=current_user, all_users=all_users)



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


@views.route('/edit_trainstation/<string:id>', methods=['GET', 'POST'])
def edit_trainstations(id):
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM trainstation_model WHERE id = %s", [id])

    trainstation = cur.fetchone()
    cur.close()

    ts_name = request.form.get('ts_name')
    ts_address = request.form.get('ts_address')

    if request.method == 'POST':
        ts_name = request.form['ts_name']
        ts_address = request.form['ts_address']

        cur = mysql.connection.cursor()

        cur.execute("UPDATE trainstation_model SET ts_name=%s, ts_addres=%s WHERE id= %s", (ts_name, ts_address, id))

        mysql.connection.commit()

        cur.close()

        all_trainstations = TrainstationModel.query.all()
    return render_template("trainstations.html", user=current_user, all_trainstations=all_trainstations)


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
        sec_start = request.form.get('sec_start')
        sec_end = request.form.get('sec_end')
        sec_track = request.form.get('sec_track')
        sec_fee = request.form.get('sec_fee')
        sec_time = request.form.get('sec_time')

        new_section = SectionModel(start=sec_start, end=sec_end, track=sec_track, fee=sec_fee, time=sec_time)
        db.session.add(new_section)
        db.session.commit()
        flash(' ---   section successfully created!   ---', category='success')

    all_sections = SectionModel.query.all()
    return render_template("sections.html", user=current_user, all_sections=all_sections)


@views.route('/all_routes', methods=['GET', 'POST'])
def get_all_routes():
    if request.method == 'POST':
        rou_name = request.form.get('rou_name')
        rou_start = request.form.get('rou_start')
        rou_end = request.form.get('rou_end')
        rou_v_max = request.form.get('rou_v_max')
        # sec_id = request.form.get('sec_id')
        # sec_name = request.form.get('sec_name')
        # sec_start = request.form.get('sec_start')

        route_sections = RouteModel.query.filter_by(name=rou_name).first()
        if route_sections:
            flash('Trainstation already exists!', category='error')
        elif len(rou_name) < 1:
            flash('Trainstation name must be greater than 1 character!', category='error')
        else:
            new_route_section = RouteModel(name=rou_name, start=rou_start, end=rou_end, v_max=rou_v_max)
            # sections = SectionModel(name=sec_name, start=sec_start)
            db.session.add(new_route_section)
            # db.session.add(sections)
            db.session.commit()
            flash(' ---   route successfully created!   ---', category='success')

    all_routes = RouteModel.query.all()
    all_sections = SectionModel.query.all()
    return render_template("routes.html", user=current_user, all_routes=all_routes, all_sections=all_sections)


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

        new_warning = WarningModel(warnings=war_warnings)
        db.session.add(new_warning)
        db.session.commit()
        flash(' ---   warning successfully created!   ---', category='success')

    all_warnings = WarningModel.query.all()
    return render_template("warnings.html", user=current_user, all_warnings=all_warnings)


@views.route('/delete-warning', methods=['POST'])
def delete_warning():
    warning = json.loads(request.data)
    warningId = warning['warningId']
    warning = WarningModel.query.get(warningId)
    if warning:
        db.session.delete(warning)
        db.session.commit()

    return jsonify({})


@views.route('/delete-section', methods=['POST'])
def delete_section():
    section = json.loads(request.data)
    sectionId = section['sectionId']
    section = SectionModel.query.get(sectionId)
    if section:
        db.session.delete(section)
        db.session.commit()

    return jsonify({})

@views.route('/delete-user', methods=['POST'])
def delete_user():
    user = json.loads(request.data)
    userId = user['userId']
    user = User.query.get(userId)
    if user:
        db.session.delete(user)
        db.session.commit()

    return jsonify({})

# @views.route('/trainstations', methods=['GET', 'POST', 'PATCH', 'PUT'])
# def trainstations():
#    trainstations = json.loads(request.data)
#    trainstations_id = trainstations['trainstations']
#    trainstations = trainstations.query.get(trainstations_id)
#    if trainstations:
#        if trainstations.user_id == current_user.id:
#            db.session.delete(trainstations)
#            db.session.commit()

#    return jsonify({})
