from dummyDatenFahrtstrecken import DummyFahrtstrecken
from dummyDatenFactory import DummyAbschnitte


class DummyFahrtdurchfuehrungen:


    @classmethod
    def getDummyFahrtdurchfuehrungen(cls):
        fahrtdurchfuehrungen = []
        abschnitte = DummyAbschnitte.getDummyAbschnitte()

        fahrtdurchfuehrungen.append(
            {    "id": 1,
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
        abschnitte = DummyAbschnitte.getDummyAbschnitte()
        if _id == 1:
            return             \
            {    "id": 1,
                "datum": "2022-05-12 10:00",
                "fahrtstrecke":
                     {
                        "id": 1,
                        "strecken_id": 4,
                        "von": "Wels",
                        "nach": "Wien Hbf",
                        "abschnitte": abschnitte
                    }

            }

        else:
            return
        {"id": 2,
         "datum": "2022-05-12 11:00",
         "fahrtstrecke":
             {
                 "id": 2,
                 "strecken_id": 4,
                 "von": "Wels",
                 "nach": "Linz",
                 "abschnitte": abschnitte[:1]
             }
         }