from flask import Flask, session, render_template, request, redirect, flash
from flask_restful import Api
from sqlalchemy import event
from models.adminModel import AdminModel
from db import db
from security import authenticate
import ticketmanagement
import aktionsmanagement
import usermanagement

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'valentina'
api = Api(app)

# Ticketmanagement-Urls
app.add_url_rule('/tickets/neu', view_func=ticketmanagement.ticket_anlegen, methods=["GET", "POST"])
app.add_url_rule('/tickets/details/<int:time_number>', view_func=ticketmanagement.details_festlegen,
                 methods=["GET", "POST"])
app.add_url_rule('/tickets/fahrtSuchen', view_func=ticketmanagement.fahrt_suchen, methods=["GET", "POST"])
app.add_url_rule('/tickets', view_func=ticketmanagement.alle_tickets, methods=["GET", "POST"])
app.add_url_rule('/ticketEntfernen/<int:_id>', view_func=ticketmanagement.delete_ticket, methods=["GET", "DELETE"])
app.add_url_rule('/timetableRide/<int:ticket_id>', view_func=ticketmanagement.ticket_timetale, methods=["GET", "POST"])

# Dealmanagement-Urls
app.add_url_rule('/aktionen/neu', view_func=aktionsmanagement.aktionAnlegen, methods=["GET", "POST"])
app.add_url_rule('/aktionEntfernen/<int:_id>', view_func=aktionsmanagement.aktionEntfernen, methods=["GET", "DELETE"])
app.add_url_rule('/alleAktionen', view_func=aktionsmanagement.alleAktionen)
app.add_url_rule('/aktionEditieren/<int:_id>', view_func=aktionsmanagement.aktionEditieren, methods=["GET", "POST"])

# Usermanagement-Urls
app.add_url_rule('/', view_func=usermanagement.login, methods=["GET", "POST"])
app.add_url_rule('/registrierung', view_func=usermanagement.register, methods=["GET", "POST"])
app.add_url_rule('/profil', view_func=usermanagement.profilEditieren, methods=["GET", "POST"])
app.add_url_rule('/ausloggen', view_func=usermanagement.ausloggen)


# creates tables
@app.before_first_request
def create_tables():
    db.create_all()
    if not AdminModel.find_admin('admin@jku.at'):
        admin = AdminModel('admin@jku.at')
        admin.save_to_db()
    session.clear()

if __name__ == '__main__':
    db.init_app(app)
    db.get_engine(app).execute('pragma foreign_keys=ON')
    app.run(port=5001, debug=True, use_reloader=True)
