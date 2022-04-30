import datetime

from flask import Flask, session, render_template, request, redirect, flash
from flask_restful import Api
from flask_jwt import JWT

from models.aktionModel import AktionModel
from models.streckeModel import StreckeModel
from models.adminModel import AdminModel
from resources.aktionResource import Aktion, Aktionsverwaltung, Aktionen, AktionDelete
from db import db
from resources.userResource import UserRegister, User
from security import authenticate
from models.userModel import UserModel
from dummyDatenFactory import DummyStrecken
import ticketmanagement
import aktionsmanagement
import usermanagement

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'valentina'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()
    if not AdminModel.find_admin('valentinahummenberger@gmx.at'):
        admin = AdminModel('valentinahummenberger@gmx.at')
        admin.save_to_db()
    session.clear()


#jwt = JWT(app, authenticate, identity)

#Ressourcen
api.add_resource(Aktion, '/rest/aktion/<int:_id>')
api.add_resource(Aktionsverwaltung, '/rest/aktionserstellung')
api.add_resource(UserRegister, '/rest/register')
api.add_resource(User, '/rest/user/<string:email>')
api.add_resource(Aktionen, '/rest/aktionen/')
api.add_resource(AktionDelete, '/rest/aktion/entfernen/<int:_id>')

#Ticketmanagement-Urls
app.add_url_rule('/tickets/neu', view_func=ticketmanagement.ticket_anlegen, methods =["GET", "POST"])

#Aktionsmanagement-Urls
app.add_url_rule('/aktionen/neu', view_func=aktionsmanagement.aktionAnlegen, methods =["GET", "POST"])
app.add_url_rule('/aktionEntfernen/<int:_id>', view_func=aktionsmanagement.aktionEntfernen, methods =["GET", "DELETE"])
app.add_url_rule('/alleAktionen', view_func=aktionsmanagement.alleAktionen)
app.add_url_rule('/aktionEditieren/<int:_id>', view_func=aktionsmanagement.aktionEditieren, methods =["GET", "POST"])

#Usermanagement-Urls
app.add_url_rule('/', view_func=usermanagement.login, methods =["GET", "POST"])
app.add_url_rule('/registrierung', view_func=usermanagement.register, methods =["GET", "POST"])
app.add_url_rule('/profil', view_func=usermanagement.profilEditieren, methods =["GET", "POST"])
app.add_url_rule('/ausloggen', view_func=usermanagement.ausloggen)


@app.route("/falscheEingabe")
def falscheEingabe():
    return render_template("falscheEingabe.html", email=session.get("email"))

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True,  use_reloader=True)

