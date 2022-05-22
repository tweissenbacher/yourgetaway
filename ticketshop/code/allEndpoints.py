from dummyData.dummyDatenAbschnitte import DummyAbschnitte
from dummyData.dummyDatenStrecken import DummyStrecken
from dummyData.dummyDatenFahrtstrecken import DummyFahrtstrecken
from dummyData.dummyTrains import DummyTrains

class SectionEndpoint:

    @classmethod
    def find_all(cls):
        return DummyAbschnitte.getDummyAbschnitte()

    @classmethod
    def find_by_id(cls, _id):
        return DummyAbschnitte.getDummyAbschnittById(_id)

class RouteEndpoint:

    @classmethod
    def find_all(cls):
        return DummyStrecken.getDummyStrecken()

    @classmethod
    def find_by_id(cls, _id):
        return DummyStrecken.getDummyStreckeById(_id)

class LineEndpoint:

    @classmethod
    def find_all(cls):
        return DummyFahrtstrecken.getDummyFahrtstrecken()

    @classmethod
    def find_by_id(cls, _id):
        return DummyFahrtstrecken.getDummyFahrtstreckeById(_id)

class TrainEndpoint:

    @classmethod
    def find_all(cls):
        return DummyTrains.getDummyTrains()

    @classmethod
    def find_by_name(cls, name):
        return DummyTrains.getDummyTrainsByName(name)

