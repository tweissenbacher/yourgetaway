class DummyTrains:

    @classmethod
    def getDummyTrains(cls):
        trains = []
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
        return trains

    @classmethod
    def getDummyTrainsByName(cls, name):
        trains = cls.getDummyTrains()
        for train in trains:
            if train['name'] == name:
                return train
        return None


