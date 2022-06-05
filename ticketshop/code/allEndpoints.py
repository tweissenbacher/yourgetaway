from dummyDatenAbschnitte import DummyAbschnitte
from dummyDatenStrecken import DummyStrecken
from dummyDatenFahrtstrecken import DummyFahrtstrecken
from dummyTrains import DummyTrains
import requests

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
        request = requests.get('http://127.0.0.1:5000/ api / lines')
        json = request.json()
        return json

        # return DummyFahrtstrecken.getDummyFahrtstrecken()

    @classmethod
    def find_by_id(cls, _id):
        request = requests.get('http://127.0.0.1:5000/ api / lines /' + str(_id))
        json = request.json()
        return json

        # return DummyFahrtstrecken.getDummyFahrtstreckeById(_id)

class TrainEndpoint:

    @classmethod
    def find_all(cls):
        return DummyTrains.getDummyTrains()

    @classmethod
    def find_by_name(cls, name):
        return DummyTrains.getDummyTrainsByName(name)

