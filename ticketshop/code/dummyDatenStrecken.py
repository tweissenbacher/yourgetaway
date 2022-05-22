class DummyStrecken:

    @classmethod
    def getDummyStrecken(cls):
        strecken = []
        strecken.append(
            {
            "id": 1,
            "von": "Linz",
            "nach": "Wien Hbf",
            "abschnitte":
                [

                    {
                        "id": 2,
                        "von": "Linz",
                        "nach": "St. Pölten",
                        "zeitdauer": 60,
                        "kosten": 10
                    },
                    {
                        "id": 3,
                        "von": "St. Pölten",
                        "nach": "Meidling",
                        "zeitdauer": 45,
                        "kosten": 8
                    },
                    {
                        "id": 3,
                        "von": "Meidling",
                        "nach": "Wien Hbf",
                        "zeitdauer": 20,
                        "kosten": 5
                    }
                ],
            "warnings":
                    [
                        {
                            "id": 3,
                            "text": "30 Minuten Verspätung"
                        }
                    ]
            });
        strecken.append(
            {
            "id": 2,
            "von": "Grieskirchen",
            "nach": "Linz",
            "abschnitte":
                [
                    {
                        "id": 4,
                        "von": "Grieskirchen",
                        "nach": "Bad Schallerbach",
                        "zeitdauer": 25,
                        "kosten": 6
                    },
                    {
                        "id": 5,
                        "von": "Bad Schallerbach",
                        "nach": "Wels",
                        "zeitdauer": 25,
                        "kosten": 6
                    },
                    {
                        "id": 1,
                        "von": "Wels",
                        "nach": "Linz",
                        "zeitdauer": 20,
                        "kosten": 5
                    }
                ],
            "warnings":
                    []
            });
        strecken.append(
            {
            "id": 3,
            "von": "Salzburg",
            "nach": "Linz",
            "abschnitte": [],
            "warnings":
                    [
                        {
                            "id": 2,
                            "text": "20 Minuten Verspätung"
                        }
                    ]
            });
        strecken.append(
            {
            "id": 4,
            "von": "Wels",
            "nach": "Wien Hbf",
            "abschnitte":
                [
                        {
                            "id": 1,
                            "von": "Wels",
                            "nach": "Linz",
                            "zeitdauer": 20,
                            "kosten": 5
                        },
                        {
                            "id": 2,
                            "von": "Linz",
                            "nach": "St. Pölten",
                            "zeitdauer": 60,
                            "kosten": 10
                        },
                        {
                            "id": 3,
                            "von": "St. Pölten",
                            "nach": "Meidling",
                            "zeitdauer": 45,
                            "kosten": 8
                        },
                        {
                            "id": 3,
                            "von": "Meidling",
                            "nach": "Wien Hbf",
                            "zeitdauer": 20,
                            "kosten": 5
                        }
                ],
            "warnings":
                [
                    {
                        "id": 1,
                        "text": "10 Minuten Verspätung"
                    }
                ]
            });

        return strecken;

    @classmethod
    def getDummyStreckeById(cls, _id):
        strecken = cls.getDummyStrecken()
        for strecke in strecken:
            if strecke['id'] == int(_id):
                return strecke
        return None







