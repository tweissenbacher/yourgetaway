from dummyDatenFactory import DummyAbschnitte


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
                "abschnitte": abschnitte[:1]
            }
        );

        return fahrtstrecken
