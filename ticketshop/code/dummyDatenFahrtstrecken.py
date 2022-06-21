from dummyDatenAbschnitte import DummyAbschnitte

# served as dummy data for lines -> no longer relevant and outdated
class DummyFahrtstrecken:

    # != strecken
    # fahrtstrecke = line
    # strecke = route

    @classmethod
    def getDummyFahrtstrecken(cls):
        fahrtstrecken = []
        abschnitte = DummyAbschnitte.getDummyAbschnitte()

        fahrtstrecken.append(
            {
                "id": 1,
                "route_id": 4,
                "starting_point": "Wels",
                "destination": "Wien Hbf",
                "sections": abschnitte,
                "trips": [
                    {
                        "note": "Tägliche Fahrt",
                        "departure": "10:43:00",
                        "train_id": 1,
                        "train": "REX3912",
                        "price": "12.40",
                        "recurrence": {
                            "date_start": "2022-03-01",
                            "date_end": "2022-06-30",
                            "weekdays": [
                                "Monday",
                                "Tuesday",
                                "Wednesday",
                                "Thursday",
                                "Friday",
                                "Saturday",
                                "Sunday"
                            ]
                        },
                        "personell": [
                            {
                                "id": 0,
                                "fname": "Karl",
                                "sname": "Meier"
                            },
                            {
                                "id": 1,
                                "fname": "Ferdinand",
                                "sname": "Grünwies"
                            }
                        ]
                    },
                    {
                        "note": "Tägliche Fahrt",
                        "departure": "11:43:00",
                        "train_id": 1,
                        "train": "REX3912",
                        "price": "12.40",
                        "recurrence": {
                            "date_start": "2022-03-01",
                            "date_end": "2022-06-30",
                            "weekdays": [
                                "Monday",
                                "Tuesday",
                                "Wednesday",
                                "Thursday",
                                "Friday",
                                "Saturday",
                                "Sunday"
                            ]
                        },
                        "personell": [
                            {
                                "id": 0,
                                "fname": "Karl",
                                "sname": "Meier"
                            },
                            {
                                "id": 1,
                                "fname": "Ferdinand",
                                "sname": "Grünwies"
                            }
                        ]
                    },
                    {
                        "note": "Werktagsfahrt frühmorgens, keine Fahrradmitnahme",
                        "departure": "06:43:00",
                        "train_id": 1,
                        "train": "REX3912",
                        "price": "12.40",
                        "recurrence": {
                            "date_start": "2022-03-01",
                            "date_end": "2022-06-30",
                            "weekdays": [
                                "Monday",
                                "Tuesday",
                                "Wednesday",
                                "Thursday",
                                "Friday"
                            ]
                        },
                        "personell": [
                            {
                                "id": 0,
                                "fname": "Karl",
                                "sname": "Meier"
                            },
                            {
                                "id": 1,
                                "fname": "Ferdinand",
                                "sname": "Grünwies"
                            }
                        ]
                    },
                    {
                        "note": "Sonderfahrt nur Montag, 2.Juni",
                        "departure": "08:43:00",
                        "train_id": 5,
                        "train": "Spezialexpress",
                        "price": "12.40",
                        "recurrence": {
                            "date_start": "2022-06-02",
                            "date_end": "2022-06-02",
                            "weekdays": [
                                "Thursday"
                            ]
                        },
                        "personell": [
                            {
                                "id": 0,
                                "fname": "Karl",
                                "sname": "Meier"
                            },
                            {
                                "id": 1,
                                "fname": "Ferdinand",
                                "sname": "Grünwies"
                            }
                        ]
                    },
                    {
                        "note": "Wochenendfahrt Abends",
                        "departure": "18:43:00",
                        "train_id": 4,
                        "train": "REX11912",
                        "price": "12.40",
                        "recurrence": {
                            "date_start": "2022-03-01",
                            "date_end": "2022-06-30",
                            "weekdays": [
                                "Saturday",
                                "Sunday"
                            ]
                        },
                        "personell": [
                            {
                                "id": 0,
                                "fname": "Karl",
                                "sname": "Meier"
                            },
                            {
                                "id": 1,
                                "fname": "Ferdinand",
                                "sname": "Grünwies"
                            }
                        ]
                    }
                ]
            }
        );
        fahrtstrecken.append(
            {
                "id": 2,
                "route_id": 4,
                "starting_point": "Wels",
                "destination": "Linz",
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
                        }
                    ],
                "trips": [
                    {
                        "note": "Tägliche Fahrt",
                        "departure": "10:30:00",
                        "train_id": 2,
                        "train": "IC233",
                        "price": "12.40",
                        "recurrence": {
                            "date_start": "2022-03-01",
                            "date_end": "2022-06-30",
                            "weekdays": [
                                "Monday",
                                "Tuesday",
                                "Wednesday",
                                "Thursday",
                                "Friday",
                                "Saturday",
                                "Sunday"
                            ]
                        },
                        "personell": [
                            {
                                "id": 0,
                                "fname": "Karl",
                                "sname": "Meier"
                            },
                            {
                                "id": 1,
                                "fname": "Ferdinand",
                                "sname": "Grünwies"
                            }
                        ]
                    },
                    {
                        "note": "Tägliche Fahrt",
                        "departure": "11:30:00",
                        "train_id": 3,
                        "train": "IC4533",
                        "price": "12.40",
                        "recurrence": {
                            "date_start": "2022-03-01",
                            "date_end": "2022-06-30",
                            "weekdays": [
                                "Monday",
                                "Tuesday",
                                "Wednesday",
                                "Thursday",
                                "Friday",
                                "Saturday",
                                "Sunday"
                            ]
                        },
                        "personell": [
                            {
                                "id": 0,
                                "fname": "Karl",
                                "sname": "Meier"
                            },
                            {
                                "id": 1,
                                "fname": "Ferdinand",
                                "sname": "Grünwies"
                            }
                        ]
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
