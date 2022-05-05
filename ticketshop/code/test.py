import datetime

from dummyDatenAbschnitte import DummyAbschnitte
from models.abschnittModel import AbschnittModel

date = str(datetime.datetime.now())

date = date.rsplit(":", 1)
date = date[0]

print(date)

print(DummyAbschnitte.getDummyAbschnitte()[0]['id'])

