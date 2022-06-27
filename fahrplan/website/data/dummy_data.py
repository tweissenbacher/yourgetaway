from .. import db
from ..model import User
from werkzeug.security import generate_password_hash


def insert_users():
    new_user = User(
        email="Helene.Auer@yg.at",
        first_name="Helene",
        last_name="Auer",
        password=generate_password_hash("pwpw", method="sha256"),
        admin=1,
    )
    db.session.add(new_user)
    new_user = User(
        email="Heinz.Feiermeier@yg.at",
        first_name="Heinz",
        last_name="Feiermeier",
        password=generate_password_hash("pwpw", method="sha256"),
        admin=1,
    )
    db.session.add(new_user)
    new_user = User(
        email="Ferdinand.Gruenwies@yg.at",
        first_name="Ferdinand",
        last_name="Grünwies",
        password=generate_password_hash("pwpw", method="sha256"),
        admin=0,
    )
    db.session.add(new_user)
    db.session.commit()


trains = [
        {
            "id": 0,
            "bezeichnung": "REX 3920",
            "spurweite": "normal",
            "wagen": [
                {
                    "id": 0,
                    "bez": "Triebwagen",
                    "gewicht": 30000,
                    "sitze": 0
                },
                {
                    "id": 1,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 52
                },
                {
                    "id": 2,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 52
                },
                {
                    "id": 103,
                    "bez": "Speisewagen",
                    "gewicht": 19000,
                    "sitze": 52
                }
            ]
        },
        {
            "id": 1,
            "bezeichnung": "RJ 301",
            "spurweite": "normal",
            "wagen": [
                {
                    "id": 6,
                    "bez": "Triebwagen",
                    "gewicht": 30000,
                    "sitze": 0
                },
                {
                    "id": 8,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 52
                },
                {
                    "id": 15,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 52
                },
                {
                    "id": 102,
                    "bez": "Speisewagen",
                    "gewicht": 19000,
                    "sitze": 52
                }
            ]
        },
        {
            "id": 32,
            "bezeichnung": "IC 902",
            "spurweite": "normal",
            "wagen": [
                {
                    "id": 6,
                    "bez": "Triebwagen",
                    "gewicht": 30000,
                    "sitze": 0
                },
                {
                    "id": 8,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 52
                },
                {
                    "id": 15,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 52
                },
                {
                    "id": 102,
                    "bez": "Speisewagen",
                    "gewicht": 19000,
                    "sitze": 52
                }
            ]
        },
        {
            "id": 143,
            "bezeichnung": "Museumsbahn",
            "spurweite": "schmalspur",
            "wagen": [
                {
                    "id": 102,
                    "bez": "298.102 Steyrtalbahn Lok Nr. 2",
                    "gewicht": 30000,
                    "sitze": 0
                },
                {
                    "id": 103,
                    "bez": "Kohlewagen",
                    "gewicht": 19000,
                    "sitze": 0
                },
                {
                    "id": 233,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 24
                },
                {
                    "id": 234,
                    "bez": "Personenwagen",
                    "gewicht": 19000,
                    "sitze": 24
                },
                {
                    "id": 235,
                    "bez": "Speisewagen",
                    "gewicht": 19000,
                    "sitze": 12
                }
            ]
        }
    ]
