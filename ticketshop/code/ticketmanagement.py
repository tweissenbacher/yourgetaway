import datetime

from flask import Flask, session, render_template, request, redirect, flash

from models.userModel import UserModel
from models.ticketModel import TicketModel
from dummyDatenFahrtstrecken import DummyFahrtstrecken
from dummyDatenFahrtdurchfuehrungen import DummyFahrtdurchfuehrungen
from models.aktionModel import AktionModel


def ticket_anlegen():
    if session.get("email") is None:
        return redirect ("/")
    user = UserModel.find_by_email(session.get("email"))
    user.check_if_admin()
    ist_admin= user.ist_admin
    if ist_admin:
        return redirect("/")
    clear_ticket_session_data()

    if request.method == "POST":
        von = request.form.get("von")
        nach = request.form.get("nach")
        datum = request.form.get("datum").replace("T", " ")

        # Fahrtstrecken holen
        # prüfen, ob es passende strecken gibt, sonst fehlermeldung
        fahrtstrecken = DummyFahrtstrecken.getDummyFahrtstrecken()
        fahrtstrecken = filter_strecke(von, nach, fahrtstrecken)
        if len(fahrtstrecken) <= 0:
            flash ("Es gibt keine Fahrtdurchführungen zur angegebenen Strecke. Die Strecke existiert nicht.")
            return redirect("/")
        #alle fahrtdurchführungen für passende Strecken holen
        fahrtdurchfuehrungen = DummyFahrtdurchfuehrungen.getDummyFahrtdurchfuehrungenByFahrtStrecke(fahrtstrecken)

        session['von'] =von
        session['nach'] =nach
        session['datum'] = datum
        session['fahrtdurchfuehrungen'] = fahrtdurchfuehrungen

        return redirect('/tickets/fahrtSuchen')
    return render_template("ticketAnlegen.html", email=session.get("email"), ist_admin = ist_admin)

def fahrt_suchen():
    if session.get('email') is None:
        return redirect ("/")
    user = UserModel.find_by_email(session.get("email"))
    user.check_if_admin()
    ist_admin= user.ist_admin
    if ist_admin:
        return redirect("/")

    von = session.get('von')
    nach = session.get('nach')
    datum = session.get('datum')
    fahrtdurchfuehrungen = session.get('fahrtdurchfuehrungen')
    # if von is None or nach is None or datum is None or fahrtdurchfuehrungen is None:
    #     return redirect("/")

    #fahrtdurchfuehrungen nach Datum filtern
    #fahrtdurchfuehrungen_gefiltert

    if request.method == "POST":
        return redirect("/tickets")

    return render_template("fahrtSuchen.html", email=session.get("email"), ist_admin=ist_admin,
                           von = von, nach = nach, fahrtdurchfuehrungen =fahrtdurchfuehrungen)


def details_festlegen(fahrtdurchfuehrung_id):
    if session.get("email") is None:
        return redirect ("/")
    user = UserModel.find_by_email(session.get("email"))
    user.check_if_admin()
    ist_admin= user.ist_admin
    if ist_admin:
        return redirect("/")

    von = session.get('von')
    nach = session.get('nach')
    datum = session.get('datum')
    fahrtdurchfuehrungen = session.get('fahrtdurchfuehrungen')
    if von is None or nach is None or datum is None or fahrtdurchfuehrungen is None:
        return redirect("/")

    #fahrtdurchführung holen
    fahrtdurchfuehrung = DummyFahrtdurchfuehrungen.getDummyFahrtdurchfuehrungById(fahrtdurchfuehrung_id)

    #preis ausrechnen und nach rabatt suchen
    preis = berechne_preis(von, nach, fahrtdurchfuehrung)
    rabatt = berechne_rabatt(fahrtdurchfuehrung['fahrtstrecke']['strecken_id'])
    sitzplatz_gebucht = False
    ticket = TicketModel(von, nach, preis, datum,
                         rabatt, sitzplatz_gebucht, user.id, fahrtdurchfuehrung_id)

    if request.method == "POST":
        TicketModel.save_to_db(ticket)
        return redirect("/tickets")

    return render_template("detailsFestlegen.html", email=session.get("email"), ist_admin=ist_admin, ticket =ticket)

def alle_tickets():
    if session.get("email") is None:
        return redirect ("/")
    user = UserModel.find_by_email(session.get("email"))
    user.check_if_admin()
    ist_admin= user.ist_admin
    if ist_admin:
        return redirect("/")
    heute = (str(datetime.datetime.now())).rsplit(":", 1)[0]
    tickets = TicketModel.find_by_user(session.get("email"))

    return render_template("alleTickets.html", email=session.get("email"), ist_admin=ist_admin, tickets=tickets,
                           heute = heute, get_fahrtdurchfuehrung = get_fahrtdurchfuehrung_of_ticket)



# Hilfsmethoden

def filter_strecke(von, nach, fahrtstrecken):
    fahrtstrecken_gefiltert = []
    von_gefunden = False

    for f in fahrtstrecken:
        for a in f['abschnitte']:
            if a['von'] == nach and not von_gefunden:
                break;
            if a['von'] == von:
                von_gefunden = True
            if a['nach'] == nach and von_gefunden:
                fahrtstrecken_gefiltert.append(f)
                von_gefunden = False
                break;

    return fahrtstrecken_gefiltert

def filter_fahrtdurchfuehrungen(datum, fahrtdurchfuehrungen):
    fahrtdurchfuehrungen_gefiltert = []



def berechne_preis (von, nach, fahrtdurchfuehrung):
    von_gefunden = False
    preis = 0
    for a in fahrtdurchfuehrung['fahrtstrecke']['abschnitte']:
        if a['von'] == von:
            von_gefunden = True
        if von_gefunden:
            preis += a['kosten']
        if a['nach'] == nach:
            return preis
    return preis

def berechne_rabatt (strecken_id):
    aktionen = AktionModel.find_by_strecke(strecken_id)
    rabatt = 0
    for aktion in aktionen:
        if aktion.rabatt > rabatt:
            rabatt = aktion.rabatt
    return rabatt

def clear_ticket_session_data ():
    session['von'] = ''
    session['datum'] = ''
    session['fahrtdurchfuehrungen'] = ''

def get_fahrtdurchfuehrung_of_ticket(ticket):
    return TicketModel.get_fahrtdurchfuehrung(ticket)