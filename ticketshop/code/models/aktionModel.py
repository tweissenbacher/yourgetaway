import datetime
from flask import flash

from db import db

from dummyDatenAbschnitte import DummyAbschnitte

from dummyDatenStrecken import DummyStrecken


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

    def __init__(self, rabatt, strecken_id, abschnitt_id, startdatum, enddatum):
        self.rabatt = rabatt
        self.strecken_id = strecken_id
        self.abschnitt_id =abschnitt_id
        self.startdatum = startdatum
        self.enddatum = enddatum


    def json(self):
        abschnitt = DummyAbschnitte.getDummyAbschnittById(self.abschnitt_id)
        strecke = DummyStrecken.getDummyStreckeById(self.strecken_id)
        return {'id': self.id, 'rabatt': self.rabatt, 'strecke': strecke, 'abschnitt': abschnitt,
                'startdatum': self.startdatum, 'enddatum': self.enddatum}

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
        return cls.query.filter_by(strecken_id = strecken_id or not strecken_id)

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