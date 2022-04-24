from db import db

class AbschnittModel(db.Model):
    __tablename__ = 'abschnitte'

    id = db.Column(db.Integer, primary_key = True)
    von = db.Column(db.String(100))
    nach = db.Column(db.String(100))
    #zeitdauer =
    entfernung = db.Column(db.Float)

    def __init__(self, von, nach, entfernung):
        self.von = von
        self.nach = nach
        self.entfernung = entfernung