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
        return strecken;
