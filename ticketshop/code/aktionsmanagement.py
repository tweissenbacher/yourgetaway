import datetime
from flask import session, render_template, request, redirect, flash
from models.dealModel import DealModel
from models.routeModel import RouteModel
from models.userModel import UserModel
from models.sectionModel import SectionModel
from allEndpoints import RouteEndpoint, SectionEndpoint
from helpers.sessionHelper import SessionHelper
from helpers.dateHelper import DateHelper

# takes care of user interaction for deal creation
def aktionAnlegen():
    # permission check
    user = SessionHelper.admin_check(session.get("email"))
    if not user:
        return redirect("/")

    if request.method == "POST":
        # get input
        discount = int(request.form.get("discount"))
        start_date = request.form.get("start_date").replace("T", " ")
        end_date = request.form.get("end_date").replace("T", " ")
        route_id = request.form.get("route_picker")
        # check data
        if DealModel.check_data(discount, start_date, end_date) is False:
            return render_template("aktionAnlegen.html", email=session.get("email"), get_routes = get_routes, today = DateHelper.get_today)
        # save to db
        if route_id:
            deal = DealModel(discount, int(route_id), start_date, end_date)
        else:
            deal = DealModel(discount, -1, start_date, end_date)
        deal.save_to_db()
        return alleAktionen()
    return render_template("aktionAnlegen.html", email=session.get("email"), get_routes = get_routes, today = DateHelper.get_today)

# deletes a certain deal by id
def aktionEntfernen(_id):
    deal = DealModel.find_by_id(_id)
    deal.delete_from_db()
    return alleAktionen()

# fetches all existing deals and displays them for the user
def alleAktionen():
    user = SessionHelper.admin_check(session.get("email"))
    if not user:
        return redirect("/")
    deals = DealModel.find_all()
    return render_template("alleAktionen.html", deals=deals, today = DateHelper.get_today, email=session.get("email"),
                           get_route_by_id = RouteModel.get_route_by_id)

# takes care of user interaction for adapting a certain deal which is identified by id
def aktionEditieren(_id):
    user = SessionHelper.admin_check(session.get("email"))
    if not user:
        return redirect("/")
    deal = DealModel.find_by_id(int(_id))
    if deal is None:
        return redirect("/alleAktionen")

    # fetch route
    if deal.route_id > 0:
        route = RouteEndpoint.find_by_id(deal.route_id)
    else:
        route = None
    today = DateHelper.get_today()
    deal_active = deal.start_date < today

    if request.method == "POST":
        # get input
        discount = int(float(request.form.get("discount")))
        from_ = request.form.get("from_")
        to = request.form.get("to")
        start_date = request.form.get("start_date").replace("T", " ")
        end_date = request.form.get("end_date").replace("T", " ")
        route_id = request.form.get("route_picker")
        # check data
        if not DealModel.discount_valid(discount):
            return render_template("aktionEditieren.html", email=session.get("email"), deal = deal, route = route, deal_active = deal_active, get_routes = get_routes())
        if not deal_active and start_date < today:
            flash("Ungülige Eingabe. Das Startdatum muss in der Zukunft liegen.")
            return render_template("aktionEditieren.html", email=session.get("email"), deal = deal, route=route, deal_active = deal_active, get_routes = get_routes())
        if start_date > end_date:
            flash("Das Startdatum darf nicht nach dem Enddatum sein.")
            return render_template("aktionEditieren.html", email=session.get("email"), deal = deal, route=route, deal_active = deal_active, get_routes = get_routes())
        # save to db
        deal.discount = discount
        deal.start_date = start_date
        deal.end_date = end_date
        if route_id:
            deal.route_id = int(route_id)
        else:
            deal.route_id = -1
        deal.save_to_db()
        flash("Aktion erfolgreich editiert!")
        return redirect("/alleAktionen")

    return render_template("aktionEditieren.html", email=session.get("email"), deal = deal, route=route,  deal_active = deal_active, get_routes = get_routes())

# Helper methods

# fetches all routes
def get_routes():
    routes = RouteEndpoint.find_all()
    routes = [RouteModel.json_to_object(r) for r in routes]
    routes.sort(key=lambda x: x.from_)
    return routes

