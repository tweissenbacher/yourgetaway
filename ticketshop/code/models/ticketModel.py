import datetime
from flask import flash

from db import db

from models.ticketWarnungModel import TicketWarnungModel

from models.userModel import UserModel


class TicketModel(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    von = db.Column(db.String(100))
    nach = db.Column(db.String(100))
    preis = db.Column(db.Float)
    datum = db.Column(db.String(100))
    rabatt = db.Column(db.Float)
    sitzplatz_reserviert = db.Column(db.Boolean)


    user_id = db.Column(db.Integer)
    #user = db.relationship(userModel)

    fahrtdurchfuehrung_id = db.Column(db.Integer)

    # Warnungen -> in Hilfstabelle ausgegliedert

    def __init__(self, id, von, nach, preis, datum, rabatt, sitzplatz_reserviert, user_id, fahrtdurchfuehrung_id):
        self.id = id
        self.von = von
        self.nach = nach
        self.preis = preis
        self.datum = datum
        self.rabatt = rabatt
        self.sitzplatz_reserviert = sitzplatz_reserviert
        self.user_id = user_id
        self.fahrtdurchfuehrung_id = fahrtdurchfuehrung_id

    def json(self):
        #fahrtdurchfuehrung = get_fahrtdurchfuehrung_by_id... -> schnittstelle
        fahrtdurchfuehrung = ''
        warnungen = []
        for warnung in TicketWarnungModel.find_by_ticket(self.id):
            warnung.add(warnung.json())
        user = UserModel.find_by_id(self.user_id).json()
        return {
            "id": self.id,
            "von": self.von,
            "nach": self.nach,
            "preis": self.preis,
            "datum": self.datum,
            "rabatt": self.rabatt,
            "sitzplatz_reserviert": self.sitzplatz_reserviert,

            "fahrtdurchfuehrung": fahrtdurchfuehrung,

            "warnungen": warnungen,

            "user": user

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
    def find_all(cls):
        return cls.query.all();

    def ticket_aktiv (self):
        heute = str(datetime.datetime.now())
        return self.datum < heute






