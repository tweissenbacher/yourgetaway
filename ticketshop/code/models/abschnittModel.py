from db import db
from dummyDatenFactory import DummyAbschnitte

class AbschnittModel(db.Model):
    __tablename__ = 'abschnitte'

    id = db.Column(db.Integer, primary_key = True)
    von = db.Column(db.String(100))
    nach = db.Column(db.String(100))
    zeitdauer = db.Column(db.Integer) # in Minuten
    kosten = db.Column(db.Float)

    def __init__(self, von, nach, zeitdauer, kosten):
        self.von = von
        self.nach = nach
        self.zeitdauer = zeitdauer
        self.kosten = kosten

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def findAbschnittVonNach(cls, von, nach):
        # Alle Abschnitte von Thomas holen, entsprechend filtern und in Liste speichern
        # vorerst DummyDaten

        abschnitte = DummyAbschnitte.getDummyAbschnitte()
        filteredAbschnitte = list(filter(lambda x: (x['von'] == von and x['nach'] == nach) or (x['von'] == nach and x['nach'] == von), abschnitte))
        if len(filteredAbschnitte) <= 0:
            return None
        return filteredAbschnitte[0]