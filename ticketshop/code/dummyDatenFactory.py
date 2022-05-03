class DummyStrecken:

    @classmethod
    def getDummyStrecken(cls):
        strecken = []
        strecken.append(
            {
            "id": 1,
            "von": "Linz",
            "nach": "Wien"
            });
        strecken.append(
            {
            "id": 2,
            "von": "Grieskirchen",
            "nach": "Linz"
            });
        strecken.append(
            {
            "id": 3,
            "von": "Salzburg",
            "nach": "Linz"
            });
        strecken.append(
            {
            "id": 4,
            "von": "Wels",
            "nach": "Wien Hbf"
            });

        return strecken;

class DummyAbschnitte:

    @classmethod
    def getDummyAbschnitte(cls):
        abschnitte = []
        abschnitte.append(
            {
            "id": 1,
            "von": "Wels",
            "nach": "Linz",
            "kosten": 5
            });
        abschnitte.append(
            {
            "id": 2,
            "von": "Linz",
            "nach": "St. Pölten",
            "kosten": 10
            });
        abschnitte.append(
            {
            "id": 3,
            "von": "St. Pölten",
            "nach": "Meidling",
            "kosten": 8
            });
        abschnitte.append(
            {
            "id": 3,
            "von": "Meidling",
            "nach": "Wien Hbf",
            "kosten": 2
            });
        return abschnitte;



