# delivers dummy data for trains
class DummyTrains:

    @classmethod
    def getDummyTrains(cls):
        trains = []
        trains.append(
            {
                'id': 0,
                'name': 'Lokalexpress',
                'capacity': 50
            }

        );
        trains.append(
            {
                'id': 1,
                'name': 'REX3912',
                'capacity': 300
            }

        );
        trains.append(
            {
                'id': 2,
                'name': 'IC233',
                'capacity': 400
            }

        );
        trains.append(
            {
                'id': 3,
                'name': 'IC4533',
                'capacity': 150
            }

        );
        trains.append(
            {
                'id': 4,
                'name': 'REX11912',
                'capacity': 55
            }

        );
        trains.append(
            {
                'id': 5,
                'name': 'Spezialexpress',
                'capacity': 2
            }

        );
        return trains

    @classmethod
    def getDummyTrainsByName(cls, name):
        trains = cls.getDummyTrains()
        for train in trains:
            if train['name'] == name:
                return train
        return trains[0]

    @classmethod
    def getDummyTrainsById(cls, id):
        trains = cls.getDummyTrains()
        for train in trains:
            if train['id'] == id:
                return train
        return trains[0]


