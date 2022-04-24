import datetime

from db import db

class AktionModel(db.Model):
    __tablename__ = 'aktionen'

    id = db.Column(db.Integer, primary_key = True)
    rabatt = db.Column(db.Float(precision=2))
    ist_strecken_rabatt = db.Column(db.Boolean, default = False)
    strecken_id = db.Column(db.Integer)
    startdatum = db.Column(db.String(100))
    enddatum = db.Column(db.String(100))


    #strecken_id = db.Column(db.int, db.ForeignKey('strecken.id'))
    #strecke = db.relationship('StreckeModel')

    def __init__(self, rabatt, ist_strecken_rabatt, strecken_id, startdatum, enddatum):
        self.rabatt = rabatt
        self.ist_strecken_rabatt = ist_strecken_rabatt
        self.strecken_id = strecken_id
        self.startdatum = startdatum
        self.enddatum = enddatum

    # def __init__(self, rabatt, ist_strecken_rabatt, startdatum, enddatum):
    #     self.rabatt = rabatt
    #     self.ist_strecken_rabatt = ist_strecken_rabatt
    #     self.startdatum = startdatum
    #     self.enddatum = enddatum

    def json(self):
        if self.ist_strecken_rabatt:
            return {'id': self.id, 'rabatt': self.rabatt, 'ist_strecken_rabatt': True,
                    'strecken_id': self.strecken_id, 'startdatum': self.startdatum, 'enddatum': self.enddatum}
        else:
            return {'id': self.id, 'rabatt': self.rabatt, 'ist_strecken_rabatt': False,
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

    @classmethod
    def check_data(cls, rabatt, startdatum, enddatum):
        if (rabatt > 0 and rabatt <= 100) and startdatum < enddatum and startdatum >= str(datetime.datetime.now()):
            return True
        return False