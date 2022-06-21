import datetime
from flask import flash
from sqlalchemy import desc
from db import db
from allEndpoints import SectionEndpoint, RouteEndpoint

# serves the representation of deal objects
class DealModel(db.Model):
    __tablename__ = 'deals'

    id = db.Column(db.Integer, primary_key = True)
    discount = db.Column(db.Float(precision=2))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))

    route_id = db.Column(db.Integer)

    def __init__(self, discount, route_id, start_date, end_date):
        self.discount = discount
        self.route_id = route_id
        self.start_date = start_date
        self.end_date = end_date

    # saves deal to db
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # deletes deal from db
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # finds deal by id
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()

    # finds all deals
    @classmethod
    def find_all(cls):
        return cls.query.all()

    # finds route deal given a certain route and date
    @classmethod
    def find_by_route_and_date(cls, route_id, date):
        return cls.query.filter_by(route_id = route_id).filter(DealModel.start_date <= date).filter(DealModel.end_date >= date)\
            .order_by(desc(DealModel.discount)).first()

    # finds all general deals given a certain date
    @classmethod
    def find_general_deals_by_date(cls, date):
        return cls.query.filter(DealModel.route_id <= -1)\
        .filter(DealModel.start_date <= date)\
        .filter(DealModel.end_date >= date)\
        .order_by(desc(DealModel.discount)).first()

    # checks if user input for deal creation is valid
    @classmethod
    def check_data(cls, discount, start_date, end_date):
        if not cls.discount_valid(discount):
            return False
        if start_date > end_date or start_date < str(datetime.datetime.now()):
            flash("Ungültige Eingaben: Das Startdatum muss in der Zukunft und VOR dem Enddatum liegen.")
            return False
        return True

    # checks if user input for discount is valid
    @classmethod
    def discount_valid(cls, discount):
        if discount < 0 or discount >= 100:
            flash("Ungültige Eingabe: Der Rabatt muss zwischen 1 und 100 Prozent betragen.")
            return False
        return True