from dummyDatenFahrtstrecken import DummyFahrtstrecken
from dummyDatenAbschnitte import DummyAbschnitte


class DummyFahrtdurchfuehrungen:


    @classmethod
    def getDummyFahrtdurchfuehrungen(cls):
        fahrtdurchfuehrungen = []
        abschnitte = DummyAbschnitte.getDummyAbschnitte()

        fahrtdurchfuehrungen.append(
            {    "id": 1,
                 "zug":
                     { "id": 1,
                       "name": "IC2352",
                       "passagieranzahl": 200

                },
                "datum": "2022-05-12 10:00",
                "fahrtstrecke":
                     {
                        "id": 1,
                        "strecken_id": 4,
                        "von": "Wels",
                        "nach": "Wien Hbf",
                        "abschnitte": abschnitte
                    }

            });

        fahrtdurchfuehrungen.append(
            {"id": 2,
             "zug":
                 {"id": 2,
                  "name": "REX1312",
                  "passagieranzahl": 300

                  },
             "datum": "2022-05-12 11:00",
             "fahrtstrecke":
                 {
                     "id": 2,
                     "strecken_id": 4,
                     "von": "Wels",
                     "nach": "Linz",
                     "abschnitte": abschnitte[:1]
                 }
             });
        return fahrtdurchfuehrungen



    @classmethod
    def getDummyFahrtdurchfuehrungenByFahrtStrecke (cls, fahrtstrecken):
        fahrtdurchfuehrungen = cls.getDummyFahrtdurchfuehrungen()
        fahrtdurchfuehrungen_gefiltert = []
        for fd in fahrtdurchfuehrungen:
            for fs in fahrtstrecken:
                if fs['id'] == fd['fahrtstrecke']['id']:
                    fahrtdurchfuehrungen_gefiltert.append(fd)
                    break

        # fahrtstrecken = DummyFahrtstrecken.getDummyFahrtstrecken()
        #filter

        return fahrtdurchfuehrungen_gefiltert

    @classmethod
    def getDummyFahrtdurchfuehrungById(cls, _id):
        fahrtdurchfuehrungen = cls.getDummyFahrtdurchfuehrungen()
        for f in fahrtdurchfuehrungen:
            if f['id'] == _id:
                return f
        return None

