import datetime

from flask import Flask, session, render_template, request, redirect, flash
from flask_restful import Api
from flask_jwt import JWT

from models.aktionModel import AktionModel
from models.streckeModel import StreckeModel
from models.userModel import UserModel
from dummyDatenStrecken import DummyStrecken
from models.abschnittModel import AbschnittModel


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
        enddatum = request.form.get("enddatum").replace("T", " ")
        if AktionModel.check_data(rabatt, startdatum, enddatum) is False:
            return render_template("aktionAnlegen.html", email=session.get("email"), isAdmin=isAdmin, heute=heute, strecken = strecken)
        if(von == "" and nach != "") or (von != "" and nach == ""):
            flash("Ungültige Eingabe. Wenn ein Streckenrabatt angelegt werden soll, muss 'von' und 'nach' befüllt werden.")
            return render_template("aktionAnlegen.html", email=session.get("email"), isAdmin=isAdmin, heute=heute, strecken = strecken)

        # Allgemeine Aktion
        if (von == "" and nach == ""):
            aktion = AktionModel(rabatt, 0, 0, startdatum, enddatum)
            aktion.save_to_db()
            return alleAktionen()
        # Streckenaktion bzw. Abschnittsaktion
        strecke = StreckeModel.findStreckeVonBis(von, nach)
        abschnitt = AbschnittModel.findAbschnittVonNach(von, nach)
        if strecke or abschnitt:
            if strecke:
                aktion = AktionModel(rabatt, strecke['id'], 0, startdatum, enddatum)
            else:
                aktion = AktionModel(rabatt, 0, abschnitt['id'], startdatum, enddatum)
            aktion.save_to_db()
            return alleAktionen()
        flash("Ungülige Eingabe. Es existiert keine Strecke bzw. kein Abschnitt für die gegebenen Parameter.")
    return render_template("aktionAnlegen.html", email=session.get("email"), isAdmin = isAdmin, heute = heute, strecken = strecken)

def aktionEntfernen(_id):
    aktion = AktionModel.find_by_id(_id)
    aktion.delete_from_db()
    return alleAktionen()

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
    abschnittDictionary = AbschnittModel.getAbschnitteDictionary()
    heute = (str(datetime.datetime.now())).rsplit(":", 1)[0]
    return render_template("alleAktionen.html", aktionen = aktionen, heute = heute, email=session.get("email"),
                           streckenDictionary = streckenDictionary, abschnittDictionary =abschnittDictionary, isAdmin = isAdmin)

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

    #Abschnitt und Strecke holen
    if aktion.strecken_id > 0:
        strecke = StreckeModel.getStreckenDictionary()[aktion.strecken_id]
    else:
        strecke = None
    if aktion.abschnitt_id > 0:
        abschnitt = AbschnittModel.getAbschnitteDictionary()[aktion.abschnitt_id]
    else:
        abschnitt = None


    heute = (str(datetime.datetime.now())).rsplit(":", 1)[0]
    aktion_aktiv = aktion.startdatum < heute

    if request.method == "POST":
        rabatt= int(float(request.form.get("rabatt")))
        von = request.form.get("von")
        nach = request.form.get("nach")
        startdatum = request.form.get("startdatum").replace("T", " ")
        enddatum = request.form.get("enddatum").replace("T", " ")
        if not AktionModel.check_rabatt(rabatt):
            return render_template("aktionEditieren.html", email=session.get("email"), isAdmin=isAdmin, aktion=aktion,
                                   strecke=strecke, abschnitt=abschnitt, aktion_aktiv=aktion_aktiv)
        if(von == "" and nach != "") or (von != "" and nach == ""):
            flash("Ungültige Eingabe. Wenn ein Streckenrabatt angelegt werden soll, muss 'von' und 'nach' befüllt werden.")
            return render_template("aktionEditieren.html", email=session.get("email"), isAdmin=isAdmin, aktion=aktion,
                                   strecke=strecke, abschnitt=abschnitt, aktion_aktiv=aktion_aktiv)
        strecke_neu = StreckeModel.findStreckeVonBis(von, nach)
        abschnitt_neu = AbschnittModel.findAbschnittVonNach(von, nach)
        if von != "" and nach != "" and not strecke_neu and not abschnitt_neu:
            flash("Ungülige Eingabe. Die angegeben Strecke existiert nicht.")
            return render_template("aktionEditieren.html", email=session.get("email"), isAdmin=isAdmin, aktion=aktion,
                                   strecke=strecke, abschnitt=abschnitt, aktion_aktiv=aktion_aktiv)

        aktion.rabatt = rabatt
        if strecke_neu:
            aktion.strecken_id = strecke_neu['id']
        else:
            aktion.strecken_id = 0
        if abschnitt_neu and not strecke_neu:
            aktion.abschnitt_id = abschnitt_neu['id']
        else:
            aktion.abschnitt_id = 0
        if not aktion_aktiv and startdatum < heute:
            flash("Ungülige Eingabe. Das Startdatum muss in der Zukunft liegen.")
            return render_template("aktionEditieren.html", email=session.get("email"), isAdmin=isAdmin, aktion=aktion,
                                   strecke=strecke, abschnitt=abschnitt, aktion_aktiv=aktion_aktiv)
        if startdatum > enddatum:
            flash("Das Startdatum darf nicht nach dem Enddatum sein.")
            return render_template("aktionEditieren.html", email=session.get("email"), isAdmin=isAdmin, aktion=aktion,
                                   strecke=strecke, abschnitt=abschnitt, aktion_aktiv=aktion_aktiv)
        aktion.startdatum = startdatum
        aktion.enddatum = enddatum

        aktion.save_to_db()
        flash("Aktion erfolgreich editiert!")
        return redirect("/alleAktionen")

    return render_template("aktionEditieren.html", email=session.get("email"), isAdmin = isAdmin, aktion=aktion, strecke = strecke, abschnitt = abschnitt, aktion_aktiv = aktion_aktiv)