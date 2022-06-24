import datetime
from flask import flash
from db import db
from models.userModel import UserModel
from allEndpoints import TrainEndpoint, LineEndpoint
from models.lineModel import LineModel

TicketSectionDetail = db.Table('ticketSectionDetails',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('ticket_id', db.Integer, db.ForeignKey('tickets.id')),
    db.Column('section_id', db.Integer, db.ForeignKey('ticket_sections.id')))

# serves the representation of ticket objects
class TicketModel(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    from_ = db.Column(db.String(100))
    to = db.Column(db.String(100))
    price = db.Column(db.Float)
    date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    discount = db.Column(db.Float)
    seat_reservation = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    line_id = db.Column(db.Integer)
    line_date = db.Column(db.String(100))
    train = db.Column(db.String(100))

    sections = db.relationship('TicketSectionModel', passive_deletes=True, secondary=TicketSectionDetail, backref='TicketModel')

    def __init__(self, from_, to, price, date, end_date, discount, seat_reservation, user_id, line_id, line_date, train):
        self.from_ = from_
        self.to = to
        self.price = price
        self.date = date
        self.end_date = end_date
        self.discount = discount
        self.seat_reservation = seat_reservation
        self.user_id = user_id
        self.line_id = int(line_id)
        self.line_date = line_date
        self.train = train

    # adds the relevant sections to the ticket
    def add_sections(self):
        capacity = int(TrainEndpoint.find_by_name(self.train)['capacity'])
        relevant_sections = TicketModel.get_relevant_sections(self)
        for section in relevant_sections:
            section_start_date = TicketModel.get_time_for_ride(self.line_id, self.line_date, section.from_)
            section_end_date = TicketModel.get_time_for_ride(self.line_id, self.line_date, section.to)
            ticket_section = TicketSectionModel.get_section(self.line_id, section_start_date, section.from_)
            if not ticket_section:
                ticket_section = TicketSectionModel(section.from_, section.to, section_start_date, section_end_date, self.line_id, capacity)
            self.sections.append(ticket_section)

    # saves ticket to db
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
        return self.id

    # deletes ticket from db
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # finds ticket by id
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # finds all tickets
    @classmethod
    def find_all(cls):
        return cls.query.all();

    # finds all ticket of a certain user who is identified by email
    @classmethod
    def find_by_user(cls, email):
        user_id = UserModel.find_by_email(email).id
        return cls.query.filter_by(user_id=user_id)

    # checks whether a ticket is active (start date < now < end date)
    def ticket_active (self):
        today = str(datetime.datetime.now())
        return self.date < today

    # fetches all relevant sections for a certain ticket (based on the line the ticket refers to)
    def get_relevant_sections(self):
        sections = LineModel.json_to_object(LineEndpoint.find_by_id(int(self.line_id))).sections
        relevant_sections = []
        from_found = False
        for section in sections:
            if section.from_ == self.to:
                break
            if section.from_ == self.from_:
                from_found = True
            if from_found:
                relevant_sections.append(section)
        return relevant_sections

    # calculates the date the train is located at a certain destination (given the line the starting time of the trip)
    # line id and starting time serve to identify the desired trip within a line
    @classmethod
    def get_time_for_ride(cls, line_id, time_str, destination):
        line = LineModel.json_to_object(LineEndpoint.find_by_id(line_id))
        sections = line.sections
        date_format_str = '%Y-%m-%d %H:%M'
        time = datetime.datetime.strptime(time_str, date_format_str)

        for s in sections:
            if s.from_ == destination:
                return time.strftime('%Y-%m-%d %H:%M')
            time = time + datetime.timedelta(minutes=s.time)
        return time.strftime('%Y-%m-%d %H:%M')

# serves the representation of ticket section objects
# ticket sections are all sections which are relevant for the booked ride
class TicketSectionModel(db.Model):
    __tablename__ = 'ticket_sections'

    id = db.Column(db.Integer, primary_key = True)
    from_ = db.Column(db.String(100))
    to = db.Column(db.String(100))
    capacity = db.Column(db.Integer)
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    line_id = db.Column(db.Integer)
    tickets = db.relationship('TicketModel', secondary=TicketSectionDetail,
                               backref='TicketSectionModel', viewonly=True)

    def __init__(self, from_, to, start_date, end_date, line_id, capacity):
        self.from_ = from_
        self.to = to
        self.start_date = start_date
        self.end_date = end_date
        self.line_id = line_id
        self.capacity = capacity

    # saves ticket section to db
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
        return self.id

    # deletes ticket section from db
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # adds seat for passenger to ticket section
    def add_passenger(self):
        if self.capacity > 0:
            self.capacity -= 1
            self.save_to_db()
            return True
        flash("Kein Sitzplatz mehr verfügbar.")
        return False

    # removes passenger seat from ticket section
    def remove_passenger(self):
        self.capacity += 1
        self.save_to_db()

    # finds ticket section by id
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # finds all ticket sections
    @classmethod
    def find_all(cls):
        return cls.query.all();

    @classmethod
    def get_section(cls, line_id, date, from_):
        return cls.query.filter_by(line_id = line_id)\
            .filter(TicketSectionModel.start_date == date)\
            .filter(TicketSectionModel.from_ == from_).first()


