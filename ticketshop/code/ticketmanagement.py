import datetime
from flask import session, render_template, request, redirect, flash
from models.userModel import UserModel
from models.ticketModel import TicketModel, TicketSectionModel
from models.dealModel import DealModel
from helpers.dateHelper import DateHelper
from allEndpoints import LineEndpoint, RouteEndpoint
from models.lineModel import LineModel
from models.routeModel import RouteModel
from helpers.sessionHelper import SessionHelper

# takes care of user input for ticket creation
def ticket_anlegen():
    user = SessionHelper.normal_user_check(session.get("email"))
    if not user:
        return redirect("/")
    clear_ticket_session_data()
    today = DateHelper.get_today()

    if request.method == "POST":
        from_ = request.form.get("from_")
        to = request.form.get("to")
        date = request.form.get("date").replace("T", " ")
        if date < today:
            flash("Der Fahrtzeitpunkt muss in der Zukunft liegen.")
        else:
            session['from_'] = from_
            session['to'] = to
            session['date'] = date
            return redirect('/tickets/fahrtSuchen')
    return render_template("ticketAnlegen.html", email=session.get("email"), today = today)

# searches for possible rides
def fahrt_suchen():
    user = SessionHelper.normal_user_check(session.get("email"))
    if not user:
        return redirect("/")
    from_ = session.get('from_')
    to = session.get('to')
    date = session.get('date')
    if not from_ or not to or not date:
        return redirect("/")

    # fetch lines
    lines = [LineModel.json_to_object(line) for line in LineEndpoint.find_all()]
    # filter lines by destination
    lines = filter_by_destination(from_, to, lines)
    if len(lines) <= 0:
        flash("Es gibt keine Fahrtdurchführungen zur angegebenen Strecke. Die Strecke existiert nicht.")
        return redirect('/tickets/neu')
    # fetch times for possible rides
    times = filter_by_date(date, lines, from_)
    if len(times) < 3: # if less than 3 results times of the following day are also fetched
        times_for_next_day = filter_by_date(DateHelper.get_next_day(date), lines, from_)
        times = times + times_for_next_day
    if len(times) <= 0:
        flash(
            "Leider konnten für das angegebene Datum keine Fahrtdurchführungen für die Strecke " + from_ + " - " + to + " gefunden werden.")
        return redirect('/tickets/neu')
    times.sort(key=lambda x: x['line_date'])
    session['times'] = times

    if request.method == "POST":
        return redirect('/tickets/neu')

    return render_template("fahrtSuchen.html", email=session.get("email"),from_ = from_, to = to,
                           times =times, get_time = DateHelper.get_time_for_ride, get_warnings = get_warnings)

# calculates price including discounts and takes care of seat reservations
def details_festlegen(time_number):
    user = SessionHelper.normal_user_check(session.get("email"))
    if not user:
        return redirect("/")
    from_ = session.get('from_')
    to = session.get('to')
    date = session.get('date')
    times = session.get('times')
    if from_ is None or to is None or date is None or times is None:
        return redirect("/")

    # fetch time details for ride
    time = times[time_number]

    # calculate price and fetch discounts
    line = LineModel.json_to_object(LineEndpoint.find_by_id(time['line_id']))
    price = calculate_price(from_, to, line, time['price'])
    discount = calculate_discount(line.route_id, DateHelper.get_time_for_ride(time['line_id'], time['line_date'], from_))
    ticket = TicketModel(from_, to, price, DateHelper.get_time_for_ride(time['line_id'], time['line_date'], from_),
                         DateHelper.get_time_for_ride(time['line_id'], time['line_date'], to),
                         discount, False, user.id, time['line_id'], time['line_date'], time['train'])
    TicketModel.add_sections(ticket)

    # seat reservations and finalization of the transaction
    if request.method == "POST":
        if request.form.get('seat_reservation') == 'on':
            reservation_successful = make_seat_reservation(ticket)
            if reservation_successful:
                ticket.seat_reservation = True
            else:
                return render_template("detailsFestlegen.html", email=session.get("email"),
                                       ticket=ticket, get_time=DateHelper.get_time_for_ride)
        ticket_id = TicketModel.save_to_db(ticket)
        flash("Ticketkauf erfolgreich")
        return redirect("/tickets")

    return render_template("detailsFestlegen.html", email=session.get("email"), ticket =ticket, get_time = DateHelper.get_time_for_ride)

# presentation of all tickets belonging to the logged in user
def alle_tickets():
    user = SessionHelper.normal_user_check(session.get("email"))
    if not user:
        return redirect("/")
    tickets = user.tickets

    return render_template("alleTickets.html", email=session.get("email"), tickets=tickets,
                           today = DateHelper.get_today, get_warnings = get_warnings)
# deletes a ticket by id
def delete_ticket(_id):
    ticket = TicketModel.find_by_id(_id)
    if ticket.seat_reservation:
        for section in ticket.sections:
            section.capacity += 1
            TicketSectionModel.save_to_db(section)
    ticket.delete_from_db()
    flash("Ticket erfolgreich storniert.")
    return alle_tickets()

# fetches timetable for a ticket
def ticket_timetale(ticket_id):
    user = SessionHelper.normal_user_check(session.get("email"))
    if not user:
        return redirect("/")

    ticket = TicketModel.find_by_id(ticket_id)

    if request.method == "POST" or not ticket:
        return redirect("/tickets")

    return render_template("timetableRide.html", email=session.get("email"), ticket = ticket)

# Helper methods

# filters lines by destination
def filter_by_destination(from_, to, lines):
    lines_filtered = []
    from_found = False

    for l in lines:
        for s in l.sections:
            if s.from_ == to and not from_found:
                break;
            if s.from_ == from_:
                from_found = True
            if s.to == to and from_found:
                lines_filtered.append(l)
                from_found = False
                break;

    return lines_filtered

# returns possible ride-times for a certain date and destination
def filter_by_date(date, lines, destination):
    times = []
    date_format_str = '%Y-%m-%d %H:%M'
    weekday = datetime.datetime.strptime(date, date_format_str)
    hours = date.split(' ')[1]
    day = date.split(' ')[0]
    for l in lines:
        for t in l.trips:
            departure = t.departure[0:-3]
            if (day >= t.date_start and day <= t.date_end):
                new_time = day + ' ' + departure
                date_for_ride = DateHelper.get_time_for_ride(l.id, new_time, destination)
                weekday = DateHelper.get_weekday(date_for_ride)
                if date_for_ride >= date and weekday in t.weekdays:
                    times.append(
                        { 'line_id': l.id,
                          'line_date': new_time,
                          'train': t.train,
                          'price': t.price
                        }
                    )
    return times

# calculates price for the actual ride based on the trip price by taking only relevant sections into consideration
def calculate_price (from_, to, line, price):
    if not line or not from_ or not to or not price:
        return 0
    number_of_relevant_sections = len(LineModel.get_relevant_sections(line.id, from_, to))
    price_per_section = round(float(price) / len(line.sections), 2)
    result = price_per_section * number_of_relevant_sections
    return round(result, 2)

# calculates discount given a certain date and route
def calculate_discount (route_id, date):
    discount_percentage = 0
    route_deal = DealModel.find_by_route_and_date(route_id, date)
    if route_deal:
        discount_percentage = route_deal.discount
    general_deal = DealModel.find_general_deals_by_date(date)
    if general_deal and general_deal.discount > discount_percentage:
        discount_percentage = general_deal.discount
    return discount_percentage

# clears session data regarding ticket booking
def clear_ticket_session_data ():
    session['from_'] = ''
    session['date'] = ''
    session['times'] = ''

# takes care of seat reservations
def make_seat_reservation(ticket):
    # Check whether seat reservation is possible for all relevant sections (otherwise: reservation not possible)
    for section in ticket.sections:
        if section.capacity < 1:
            flash("Sitzplatzreservierung leider nicht möglich.")
            return False
        section.capacity -= 1

    # save changes to db
    for section in ticket.sections:
        TicketSectionModel.save_to_db(section)
    flash("Sitzplatzreservierung erfolgreich")
    return True

# fetch warnings from route information system
def get_warnings(line_id, from_, to):
    # json_line = LineEndpoint.find_by_id(int(line_id))
    # if not json_line:
    #     return []
    # route_id = json_line['route_id']
    # route = RouteEndpoint.find_by_id(route_id)
    # if not route:
    #     return []
    # line = LineModel.json_to_object(json_line)
    # if not line:
    #     return []
    # route = RouteModel.json_to_object(RouteEndpoint.find_by_id(int(line.route_id)))
    # warnings = []
    # from_found = False
    # for section in route.sections:
    #     if section.from_ == from_:
    #         from_found = True
    #     if from_found:
    #         for warning in section.warnings:
    #             warnings.append(warning)
    #     if section.from_ == to:
    #         break
    # return warnings

    return []





