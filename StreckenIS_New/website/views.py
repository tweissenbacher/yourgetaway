import website.trainstations
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Note, TrainstationModel, SectionModel, RouteModel
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():


    return render_template("home.html", user=current_user)


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
            flash('Trainstation created!', category='success')

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
    all_sections = SectionModel.query.all()
    return render_template("sections.html", user=current_user, all_sections=all_sections)


@views.route('/all_routes', methods=['GET', 'POST'])
def get_all_routes():
    all_routes = RouteModel.query.all()
    return render_template("routes.html", user=current_user, all_routes=all_routes)



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
