import datetime

from flask import Flask, session, render_template, request, redirect
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

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'valentina'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()
    admin = AdminModel('valentinahummenberger@gmx.at')
    admin.save_to_db()
    session.clear()


#jwt = JWT(app, authenticate, identity)

api.add_resource(Aktion, '/aktion/<int:_id>')
api.add_resource(Aktionsverwaltung, '/aktionserstellung')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<string:email>')
api.add_resource(Aktionen, '/aktionen/')
api.add_resource(AktionDelete, '/aktion/entfernen/<int:_id>')




@app.route("/", methods =["GET", "POST"])
def login():
    if request.method == "POST":
        email =request.form.get("email")
        password= request.form.get("password")
        #user is None or password is None:
        user = authenticate(email, password)
        if user:
            session.update({"email": email})
            user.check_if_admin()
            if user.ist_admin:
                return redirect ("/aktionen/neu")
            return redirect("/tickets/neu")
    return render_template("login.html", email = session.get("email"))

@app.route("/registrierung", methods =["GET", "POST"])
def register():
    if request.method == "POST":
        email =request.form.get("email")
        password = request.form.get("password")
        user = UserModel.find_by_email(email)
        if user is None:
            UserModel.save_to_db(UserModel(email, password))
            return redirect("/")
    return render_template("register.html", email = session.get("email"))


@app.route("/aktionen/neu", methods =["GET", "POST"])
def aktionAnlegen():
    if session.get("email") is None:
        return redirect ("/")

    user = UserModel.find_by_email(session.get("email"))
    user.check_if_admin()
    isAdmin= user.ist_admin
    if not isAdmin:
        return redirect("/")
    if request.method == "POST":
        rabatt= int(request.form.get("rabatt"))
        von =request.form.get("von")
        nach= request.form.get("nach")
        startdatum = request.form.get("startdatum").replace("T", " ")
        #startdatum = datetime.datetime.strptime(startdatum, '%Y-%m-%d %H:%M')
        enddatum = request.form.get("enddatum").replace("T", " ")
        #enddatum = datetime.datetime.strptime(enddatum, '%Y-%m-%d %H:%M')
        if AktionModel.check_data(rabatt, startdatum, enddatum) is False:
            return redirect("/falscheEingabe")
        if (von is None or nach is None):

            aktion = AktionModel(rabatt, False, 0, startdatum, enddatum)
            aktion.save_to_db()
            return alleAktionen()
        strecke = StreckeModel.findStreckeVonBis(von, nach)
        #check dataum start vor ende und start in Zukunft
        if rabatt <= 100 and rabatt > 0:
            #aktion = AktionModel(rabatt, True, strecke['id'])
            aktion = AktionModel(rabatt, True, 1, startdatum, enddatum)
            aktion.save_to_db()
            return alleAktionen()
    # today1 = datetime.datetime.now()
    # # today2 = datetime.datetime.now()
    # # today = str(datetime.datetime.strptime(str(today1), "%Y-%m-%d %H:%M:%S")) + 'T' + str(datetime.datetime.strptime(str(today2), "%H:%M"))
    # # now = datetime.datetime.now()
    # # print(now
    # #       )
    # today = str(datetime.datetime.strptime(str(today1), "%Y-%m-%d %H:%M:%S"))
    # today = today.replace(" ", "T")
    # today = today[:-3]
    # print(today)

    return render_template("aktionAnlegen.html", email=session.get("email"), isAdmin = isAdmin)

@app.route("/aktionEntfernen/<int:_id>", methods =["GET", "DELETE"])
def aktionEntfernen(_id):
    aktion = AktionModel.find_by_id(_id)
    aktion.delete_from_db()
    return alleAktionen()

@app.route("/alleAktionen")
def alleAktionen():
    aktionen = AktionModel.find_all()
    heute = str(datetime.datetime.now())
    heute = heute.rsplit(":", 1)
    heute = heute[0]
    return render_template("alleAktionen.html", aktionen = aktionen, heute = heute, email=session.get("email"))


@app.route("/profil")
def profilEditieren():
    return render_template("profil.html", email=session.get("email"))

@app.route("/ausloggen")
def ausloggen():
    session.clear()
    return redirect ("/")


@app.route("/falscheEingabe")
def falscheEingabe():
    return render_template("falscheEingabe.html", email=session.get("email"))

#Tickets

@app.route("/tickets/neu", methods =["GET", "POST"])
def ticketAnlegen():
    if session.get("email") is None:
        return redirect ("/")
    return render_template("ticketAnlegen.html", email=session.get("email"))

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)