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

api.add_resource(Aktion, '/rest/aktion/<int:_id>')
api.add_resource(Aktionsverwaltung, '/rest/aktionserstellung')
api.add_resource(UserRegister, '/rest/register')
api.add_resource(User, '/rest/user/<string:email>')
api.add_resource(Aktionen, '/rest/aktionen/')
api.add_resource(AktionDelete, '/rest/aktion/entfernen/<int:_id>')




@app.route("/", methods =["GET", "POST"])
def login():
    if request.method == "POST":
        email =request.form.get("email")
        password= request.form.get("password")
        user = authenticate(email, password)
        if user:
            session.update({"email": email})
            user.check_if_admin()
            if user.ist_admin:
                return redirect ("/aktionen/neu")
            return redirect("/tickets/neu")
        flash("Inkorrekte Email und/oder inkorrektes Passwort.\nVersuchen Sie es erneut oder registrieren Sie sich, wenn Sie noch keinen Account haben.")
    return render_template("login.html", email = session.get("email"))

@app.route("/registrierung", methods =["GET", "POST"])
def register():
    if request.method == "POST":
        email =request.form.get("email")
        password = request.form.get("password")
        vorname = request.form.get("vorname")
        nachname = request.form.get("nachname")
        geburtsdatum = request.form.get("geburtsdatum")
        if geburtsdatum:
            geburtsdatum = geburtsdatum.replace("T", " ")
        user = UserModel.find_by_email(email)
        if user is None:
            UserModel.save_to_db(UserModel(email, password, vorname, nachname, '', geburtsdatum))
            flash("Registrierung erfolgreich! Sie können sich nun einloggen.")
            return redirect("/")
        flash("Es gibt bereits einen User mit dieser Email-Adresse. Bitte loggen Sie sich ein oder wählen Sie eine andere Emailadresse.")
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
    heute = str(datetime.datetime.now())
    heute = heute.rsplit(":", 1)
    heute = heute[0]
    strecken = DummyStrecken.getDummyStrecken()

    if request.method == "POST":
        rabatt= int(request.form.get("rabatt"))
        von =request.form.get("von")
        nach= request.form.get("nach")
        startdatum = request.form.get("startdatum").replace("T", " ")
        #startdatum = datetime.datetime.strptime(startdatum, '%Y-%m-%d %H:%M')
        enddatum = request.form.get("enddatum").replace("T", " ")
        #enddatum = datetime.datetime.strptime(enddatum, '%Y-%m-%d %H:%M')
        if AktionModel.check_data(rabatt, startdatum, enddatum) is False:
            return render_template("aktionAnlegen.html", email=session.get("email"), isAdmin=isAdmin, heute=heute, strecken = strecken)
        if(von == "" and nach != "") or (von != "" and nach == ""):
            flash("Ungültige Eingabe. Wenn ein Streckenrabatt angelegt werden soll, muss 'von' und 'nach' befüllt werden.")
            return render_template("aktionAnlegen.html", email=session.get("email"), isAdmin=isAdmin, heute=heute, strecken = strecken)

        # Allgemeine Aktion
        if (von == "" and nach == ""):
            aktion = AktionModel(rabatt, False, 0, startdatum, enddatum)
            aktion.save_to_db()
            return alleAktionen()
        # Streckenaktion
        strecke = StreckeModel.findStreckeVonBis(von, nach)
        if strecke:
            aktion = AktionModel(rabatt, True, strecke['id'], startdatum, enddatum)
            aktion.save_to_db()
            return alleAktionen()
        flash("Ungülige Eingabe. Die angegeben Strecke existiert nicht.")
    return render_template("aktionAnlegen.html", email=session.get("email"), isAdmin = isAdmin, heute = heute, strecken = strecken)

@app.route("/aktionEntfernen/<int:_id>", methods =["GET", "DELETE"])
def aktionEntfernen(_id):
    aktion = AktionModel.find_by_id(_id)
    aktion.delete_from_db()
    return alleAktionen()

@app.route("/alleAktionen")
def alleAktionen():
    if session.get("email") is None:
        return redirect ("/")
    user = UserModel.find_by_email(session.get("email"))
    user.check_if_admin()
    isAdmin= user.ist_admin
    if not isAdmin:
        return redirect("/")
    aktionen = AktionModel.find_all()
    streckenDictionary = StreckeModel.getStreckenDictionary()
    heute = str(datetime.datetime.now())
    heute = heute.rsplit(":", 1)
    heute = heute[0]
    return render_template("alleAktionen.html", aktionen = aktionen, heute = heute, email=session.get("email"),
                           streckenDictionary = streckenDictionary, isAdmin = isAdmin)


@app.route("/profil", methods =["GET", "POST"])
def profilEditieren():
    if session.get("email") is None:
        return redirect ("/")
    user = UserModel.find_by_email(session.get("email"))
    user.check_if_admin()
    isAdmin= user.ist_admin

    if request.method == "POST":
        password = request.form.get("password")
        if authenticate(user.email, password):
            password_new = request.form.get("new-password")
            if password_new and password_new == password:
                flash("Das neue Passwort darf nicht dasselbe wie das alte Passwort sein. Versuchen Sie es noch einmal.")
            else:
                vorname = request.form.get("vorname")
                nachname = request.form.get("nachname")
                geburtsdatum = request.form.get("geburtsdatum")
                if geburtsdatum:
                    geburtsdatum = geburtsdatum.replace("T", " ")
                user.vorname = vorname
                user.nachname = nachname
                user.geburtsdatum = geburtsdatum

                UserModel.save_to_db(user)
                flash("Profil erfolgreich editiert.")
        else:
            flash("Falsches Passwort. Versuchen Sie es noch einmal.")
    return render_template("profil.html", email=session.get("email"), isAdmin = isAdmin, user=user)

@app.route("/aktionEditieren/<int:_id>", methods =["GET", "POST"])
def aktionEditieren(_id):
    if session.get("email") is None:
        return redirect ("/")
    user = UserModel.find_by_email(session.get("email"))
    user.check_if_admin()
    isAdmin= user.ist_admin
    if not isAdmin:
        return redirect("/")
    aktion = AktionModel.find_by_id(_id)
    if aktion is None:
        return redirect("/falscheEingabe")
    strecke = StreckeModel.getStreckenDictionary()[aktion.strecken_id]
    heute = str(datetime.datetime.now())
    heute = heute.rsplit(":", 1)
    heute = heute[0]
    aktion_aktiv = aktion.startdatum < heute

    if request.method == "POST":
        rabatt= int(float(request.form.get("rabatt")))
        von = request.form.get("von")
        nach = request.form.get("nach")
        startdatum = request.form.get("startdatum").replace("T", " ")
        enddatum = request.form.get("enddatum").replace("T", " ")
        if AktionModel.check_data(rabatt, startdatum, enddatum) is False:
            flash("Ungültige Eingaben. Das Startdatum muss in der Zukunft und VOR dem Enddatum liegen. Der Rabatt muss zwischen 1 und 100 Prozent betragen.")
            return render_template("aktionEditieren.html", email=session.get("email"), isAdmin=isAdmin, aktion=aktion,
                               strecke=strecke, aktion_aktiv=aktion_aktiv)
        if(von == "" and nach != "") or (von != "" and nach == ""):
            flash("Ungültige Eingabe. Wenn ein Streckenrabatt angelegt werden soll, muss 'von' und 'nach' befüllt werden.")
            return render_template("aktionEditieren.html", email=session.get("email"), isAdmin=isAdmin, aktion=aktion,
                               strecke=strecke, aktion_aktiv=aktion_aktiv)
        strecke_neu = StreckeModel.findStreckeVonBis(von, nach)
        if von != "" and nach != "" and not strecke_neu:
            flash("Ungülige Eingabe. Die angegeben Strecke existiert nicht.")
            return render_template("aktionEditieren.html", email=session.get("email"), isAdmin=isAdmin, aktion=aktion,
                               strecke=strecke, aktion_aktiv=aktion_aktiv)
        aktion.ist_strecken_rabatt = not (von == "" and nach == "")
        aktion.rabatt = rabatt
        if strecke_neu:
            aktion.strecken_id = strecke_neu['id']
        if not aktion_aktiv and startdatum < heute:
            flash("Ungülige Eingabe. Das Startdatum muss in der Zukunft liegen.")
            return render_template("aktionEditieren.html", email=session.get("email"), isAdmin=isAdmin, aktion=aktion,
                               strecke=strecke, aktion_aktiv=aktion_aktiv)
        if startdatum > enddatum:
            flash("Das Startdatum darf nicht nach dem Enddatum sein.")
            return render_template("aktionEditieren.html", email=session.get("email"), isAdmin=isAdmin, aktion=aktion,
                               strecke=strecke, aktion_aktiv=aktion_aktiv)
        aktion.startdatum = startdatum
        aktion.enddatum = enddatum

        aktion.save_to_db()
        flash("Aktion erfolgreich editiert!")
        return redirect("/alleAktionen")

    # return render_template("aktionEditieren.html", email=session.get("email"), isAdmin=isAdmin, aktion=aktion,
    #                        strecke=strecke)
    return render_template("aktionEditieren.html", email=session.get("email"), isAdmin = isAdmin, aktion=aktion, strecke = strecke, aktion_aktiv = aktion_aktiv)

@app.route("/ausloggen")
def ausloggen():
    session.clear()
    flash("Erfolgreich ausgeloggt.")
    return redirect("/")


@app.route("/falscheEingabe")
def falscheEingabe():
    return render_template("falscheEingabe.html", email=session.get("email"))



if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)