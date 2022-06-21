# served as dummy data for routes -> no longer relevant and also outdated
class DummyStrecken:

    @classmethod
    def getDummyStrecken(cls):
        strecken = []
        strecken.append(
            {
            "id": 1,
            "von": "Linz",
            "nach": "Wien Hbf",
            "sections":
                [

                    {
                        "id": 2,
                        "start": "Linz",
                        "end": "St. Pölten",
                        "time": 60,
                        "fee": 10,
                        "warnings": [
                            {
                                "id": 2,
                                "route_id": 0,
                                "section_id": 2,
                                "text": "Waggon 3 gesperrt."
                            }
                        ]
                    },
                    {
                        "id": 3,
                        "start": "St. Pölten",
                        "end": "Meidling",
                        "time": 45,
                        "fee": 8,
                        "warnings": [
                            {
                                "id": 3,
                                "route_id": 0,
                                "section_id": 3,
                                "text": "Achtung Maskenpflicht."
                            }
                        ]
                    },
                    {
                        "id": 3,
                        "start": "Meidling",
                        "end": "Wien Hbf",
                        "time": 20,
                        "fee": 5,
                        "warnings": []
                    }
                ],
            "warnings":
                    [
                        {
                            "id": 12,
                            "route_id": 1,
                            "section_id": 0,
                            "text": "30 Minuten Verspätung"
                        }
                    ]
            });
        strecken.append(
            {
            "id": 2,
            "von": "Grieskirchen",
            "nach": "Linz",
            "sections":
                [
                    {
                        "id": 4,
                        "start": "Grieskirchen",
                        "end": "Bad Schallerbach",
                        "time": 25,
                        "fee": 6,
                        "warnings": []
                    },
                    {
                        "id": 5,
                        "start": "Bad Schallerbach",
                        "end": "Wels",
                        "time": 25,
                        "fee": 6,
                        "warnings": []
                    },
                    {
                        "id": 1,
                        "start": "Wels",
                        "end": "Linz",
                        "time": 20,
                        "fee": 5,
                        "warnings": [
                            {
                                "id": 1,
                                "route_id": 0,
                                "section_id": 1,
                                "text": "Es kann zu Verzögerungen kommen."
                            }
                        ]
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
            "sections": [],
            "warnings":
                    [
                        {
                            "id": 11,
                            "route_id": 3,
                            "section_id": 0,
                            "text": "20 Minuten Verspätung"
                        }
                    ]
            });
        strecken.append(
            {
            "id": 4,
            "von": "Wels",
            "nach": "Wien Hbf",
            "sections":
                [
                        {
                            "id": 1,
                            "start": "Wels",
                            "end": "Linz",
                            "time": 20,
                            "fee": 5,
                            "warnings": [
                                {
                                    "id": 1,
                                    "route_id": 0,
                                    "section_id": 1,
                                    "text": "Es kann zu Verzögerungen kommen."
                                }
                            ]
                        },
                        {
                            "id": 2,
                            "start": "Linz",
                            "end": "St. Pölten",
                            "time": 60,
                            "fee": 10,
                            "warnings": [
                                {
                                    "id": 2,
                                    "route_id": 0,
                                    "section_id": 2,
                                    "text": "Waggon 3 gesperrt."
                                }
                            ]
                        },
                        {
                            "id": 3,
                            "start": "St. Pölten",
                            "end": "Meidling",
                            "time": 45,
                            "fee": 8,
                            "warnings": [
                                {
                                    "id": 3,
                                    "route_id": 0,
                                    "section_id": 3,
                                    "text": "Achtung Maskenpflicht."
                                }
                            ]
                        },
                        {
                            "id": 3,
                            "start": "Meidling",
                            "end": "Wien Hbf",
                            "time": 20,
                            "fee": 5,
                            "warnings": []
                        }
                ],
            "warnings":
                [
                    {
                        "id": 10,
                        "route_id": 4,
                        "section_id": 0,
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







