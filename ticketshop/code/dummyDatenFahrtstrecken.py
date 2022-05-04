from dummyDatenAbschnitte import DummyAbschnitte


class DummyFahrtstrecken:

    # != strecken

    @classmethod
    def getDummyFahrtstrecken(cls):
        fahrtstrecken = []
        abschnitte = DummyAbschnitte.getDummyAbschnitte()

        fahrtstrecken.append(
            {
                "id": 1,
                "strecken_id": 4,
                "von": "Wels",
                "nach": "Wien Hbf",
                "abschnitte": abschnitte

            }
        );
        fahrtstrecken.append(
            {
                "id": 2,
                "strecken_id": 4,
                "von": "Wels",
                "nach": "Linz",
                "abschnitte":
                    [
                        {
                            "id": 1,
                            "von": "Wels",
                            "nach": "Linz",
                            "zeitdauer": 20,
                            "kosten": 5
                        }
                    ]
            }
        );

        return fahrtstrecken

    @classmethod
    def getDummyFahrtstreckeById(cls, _id):
        fahrtstrecken = cls.getDummyFahrtstrecken()
        for fahrtstrecke in fahrtstrecken:
            if fahrtstrecke['id'] == _id:
                return fahrtstrecke
        return None
