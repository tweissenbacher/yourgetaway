import datetime
from flask import flash

from db import db

class AktionModel(db.Model):
    __tablename__ = 'aktionen'

    id = db.Column(db.Integer, primary_key = True)
    rabatt = db.Column(db.Float(precision=2))
    ist_strecken_rabatt = db.Column(db.Boolean, default = False)
    startdatum = db.Column(db.String(100))
    enddatum = db.Column(db.String(100))

    strecken_id = db.Column(db.Integer)
    # strecken_id = db.Column(db.Integer, db.ForeignKey('strecken.id'))
    # strecke = db.relationship('StreckeModel')

    abschnitt_id = db.Column(db.Integer)
    # abchnitt_id = db.Column(db.Integer, db.ForeignKey('abschnitte.id'))
    # abschnitt = db.relationship('AbschnittModel')

    def __init__(self, rabatt, ist_strecken_rabatt, strecken_id, startdatum, enddatum):
        self.rabatt = rabatt
        self.ist_strecken_rabatt = ist_strecken_rabatt
        self.strecken_id = strecken_id
        self.startdatum = startdatum
        self.enddatum = enddatum


    def json(self):
        return {'id': self.id, 'rabatt': self.rabatt, 'ist_strecken_rabatt': self.ist_strecken_rabatt,
                    'strecken_id': self.strecken_id, 'startdatum': self.startdatum, 'enddatum': self.enddatum}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all();

    @classmethod # retourniert allgemeine Aktionen und solche, die sich auf die angegebene Strecke beziehen
    def find_by_strecke(cls, strecken_id):
        return cls.query.filter_by(strecken_id = strecken_id or strecken_id is None)

    @classmethod
    def check_data(cls, rabatt, startdatum, enddatum):
        if not cls.check_rabatt(rabatt):
            return False
        if startdatum > enddatum or startdatum < str(datetime.datetime.now()):
            flash("Ungültige Eingaben: Das Startdatum muss in der Zukunft und VOR dem Enddatum liegen.")
            return False;
        return True;

    @classmethod
    def check_rabatt(cls, rabatt):
        if rabatt < 0 or rabatt >= 100:
            flash("Ungültige Eingabe: Der Rabatt muss zwischen 1 und 100 Prozent betragen.")
            return False
        return True