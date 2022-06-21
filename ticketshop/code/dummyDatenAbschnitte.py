# served as dummy data for sections -> no longer relevant and outdated
class DummyAbschnitte:

    @classmethod
    def getDummyAbschnitte(cls):
        sections = []
        sections.append(
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
            });
        sections.append(
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
            });
        sections.append(
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
            });
        sections.append(
            {
            "id": 3,
            "start": "Meidling",
            "end": "Wien Hbf",
            "time": 20,
            "fee": 5,
            "warnings": []
            });
        return sections;

    @classmethod
    def getDummyAbschnittById(cls, _id):
        sections = cls.getDummyAbschnitte()
        for section in sections:
            if section['id'] == _id:
                return section
        return None
