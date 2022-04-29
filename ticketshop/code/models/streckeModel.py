from db import db

from dummyDatenFactory import DummyStrecken


class StreckeModel(db.Model):
    __tablename__ = 'strecken'

    id = db.Column(db.Integer, primary_key=True)
    von = db.Column(db.String(50))
    nach = db.Column(db.String(50))

    def __init__(self, id, von, nach):
        self.id = id
        self.von = von
        self.nach = nach


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def findStreckeVonBis(cls, von, nach):
# Strecken von Thomas holen und in Liste speichern
# vorerst DummyDaten
        strecken = DummyStrecken.getDummyStrecken()
        filteredStrecken = \
            list(filter(lambda x: (x['von'] == von and x['nach'] == nach) or (x['von'] == nach and x['nach'] == von), strecken))
        if len(filteredStrecken) <= 0:
            return None
        return filteredStrecken[0]

    @classmethod
    def getStreckenDictionary(cls):
        alleStrecken = DummyStrecken.getDummyStrecken()
        dictionary = {}
        for strecke in alleStrecken:
            dictionary[strecke['id']] = strecke

        return dictionary
