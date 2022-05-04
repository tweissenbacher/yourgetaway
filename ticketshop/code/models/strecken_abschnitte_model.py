from db import db

#Hilfstabelle, um Beziehung zw. Strecke und ihren Abschnitten darzustellen und die Reihenfolge der Abschnitte festzulegen
#Reihenfolge der Abschnitte bestimmt sich durch die Id (aufsteigend)
class StreckenAbschnitteModel(db.Model):
    __tablename__ = 'streckenabschnitte'

    id = db.Column(db.Integer, primary_key=True)
    strecken_id = db.Column(db.Integer)
    abschnitt_id =db.Column(db.Integer)

    # strecken_id = db.Column(db.Integer, db.ForeignKey('strecken.id'))
    # strecke = db.relationship('StreckeModel')
    #
    # abschnitt_id =db.Column(db.Integer, db.ForeignKey('abschnitt.id'))
    # abschnitt = db.relationship('AbschnittModel')

    def __init__(self, strecken_id, abschnitt_id):
        self.strecken_id = strecken_id
        self.abschnitt_id = abschnitt_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
