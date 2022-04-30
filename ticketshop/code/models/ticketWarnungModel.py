import datetime
from flask import flash

from db import db

class TicketWarnungModel(db.Model):
    __tablename__ = 'ticket_warnungen'

    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer)
    text = db.Column(db.String(200))

    def json(self):
        return {
            "id": self.id,
            "ticekt_id": self.ticket_id,
            "text": self.text
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_ticket(cls, ticket_id):
        return cls.query.filter_by(ticket_id=ticket_id).all();

    @classmethod
    def find_all(cls):
        return cls.query.all();