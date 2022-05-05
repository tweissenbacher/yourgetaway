from .. import db
from ..model import User, Section, Line
from werkzeug.security import check_password_hash, generate_password_hash


def insert_users():
    new_user = User(
        email="Helene.Auer@yg.at",
        first_name="Helene",
        last_name="Auer",
        password=generate_password_hash("password", method="sha256"),
        admin=1,
    )
    db.session.add(new_user)
    new_user = User(
        email="Heinz.Feiermeier@yg.at",
        first_name="Heinz",
        last_name="Feiermeier",
        password=generate_password_hash("password", method="sha256"),
        admin=1,
    )
    db.session.add(new_user)
    new_user = User(
        email="Ferdinand.Grünwies@yg.at",
        first_name="Ferdinand",
        last_name="Grünwies",
        password=generate_password_hash("password", method="sha256"),
        admin=0,
    )
    db.session.add(new_user)
    db.session.commit()


def dummy_sections():
    new_section = Section()
    db.session.add(new_section)

    db.session.commit()


def dummy_lines():
    new_line = Line(
        id=0,
        description="Pyhrnbahn",
        price=1240,
        # note =
        # date = db.Column(db.DateTime(timezone=True), default=func.now())
        sections={},
    )
    db.session.add(new_line)

    db.session.commit()
