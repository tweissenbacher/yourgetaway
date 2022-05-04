class DummyAbschnitte:

    @classmethod
    def getDummyAbschnitte(cls):
        abschnitte = []
        abschnitte.append(
            {
            "id": 1,
            "von": "Wels",
            "nach": "Linz",
            "zeitdauer": 20,
            "kosten": 5
            });
        abschnitte.append(
            {
            "id": 2,
            "von": "Linz",
            "nach": "St. Pölten",
            "zeitdauer": 60,
            "kosten": 10
            });
        abschnitte.append(
            {
            "id": 3,
            "von": "St. Pölten",
            "nach": "Meidling",
            "zeitdauer": 45,
            "kosten": 8
            });
        abschnitte.append(
            {
            "id": 3,
            "von": "Meidling",
            "nach": "Wien Hbf",
            "zeitdauer": 20,
            "kosten": 5
            });
        # abschnitte.append(
        #     {
        #     "id": 4,
        #     "von": "Grieskirchen",
        #     "nach": "Bad Schallerbach",
        #     "zeitdauer": 25,
        #     "kosten": 6
        #     });
        # abschnitte.append(
        #     {
        #     "id": 5,
        #     "von": "Bad Schallerbach",
        #     "nach": "Wels",
        #     "zeitdauer": 25,
        #     "kosten": 6
        #     });
        return abschnitte;

    @classmethod
    def getDummyAbschnittById(cls, _id):
        abschnitte = cls.getDummyAbschnitte()
        for abschnitt in abschnitte:
            if abschnitt['id'] == _id:
                return abschnitt
        return None
