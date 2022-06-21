from dummyDatenAbschnitte import DummyAbschnitte
from dummyDatenStrecken import DummyStrecken
from dummyDatenFahrtstrecken import DummyFahrtstrecken
from dummyTrains import DummyTrains
import requests

# represents endpoint for sections
class SectionEndpoint:

    # fetches all sections from strecken-informationssystem
    @classmethod
    def find_all(cls):
        request = requests.get('http://127.0.0.1:5002/api/sections/')
        json = request.json()
        return json['sections']

        # return DummyAbschnitte.getDummyAbschnitte()

    # fetches a section from strecken-informationssystem given a certain id
    @classmethod
    def find_by_id(cls, _id):
        request = requests.get('http://127.0.0.1:5002/api/sections/' + str(_id))
        json = request.json()
        return json

        # return DummyAbschnitte.getDummyAbschnittById(_id)

# represents endpoint for routes
class RouteEndpoint:

    # fetches all routes from strecken-informationssystem
    @classmethod
    def find_all(cls):
        request = requests.get('http://127.0.0.1:5002/api/routes/')
        json = request.json()
        return json['routes']
        # return DummyStrecken.getDummyStrecken()

    # fetches a route from strecken-informationssystem given a certain id
    @classmethod
    def find_by_id(cls, _id):
        request = requests.get('http://127.0.0.1:5002/api/routes/' + str(_id))
        json = request.json()
        return json

        # return DummyStrecken.getDummyStreckeById(_id)

# represents endpoint for lines
class LineEndpoint:

    # fetches all lines from fahrplan-informationssystem
    @classmethod
    def find_all(cls):
        request = requests.get('http://127.0.0.1:5000/api/lines')
        json = request.json()
        return json['lines']

        # return DummyFahrtstrecken.getDummyFahrtstrecken()

    # fetches a line from fahrplan-informationssystem given a certain id
    @classmethod
    def find_by_id(cls, _id):
        request = requests.get('http://127.0.0.1:5000/api/lines/' + str(_id))
        json = request.json()
        return json

        # return DummyFahrtstrecken.getDummyFahrtstreckeById(_id)

# represents endpoint for trains (based on dummy data)
class TrainEndpoint:

    # fetches all trains from dummy data
    @classmethod
    def find_all(cls):
        return DummyTrains.getDummyTrains()

    # fetches train by name from dummy data
    @classmethod
    def find_by_name(cls, name):
        return DummyTrains.getDummyTrainsByName(name)

    # fetches train by id from dummy data
    @classmethod
    def find_by_id(cls, id):
        return DummyTrains.getDummyTrainsById(id)

