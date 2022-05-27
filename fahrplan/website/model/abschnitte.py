import sqlalchemy
from sqlalchemy.sql import func
from marshmallow_sqlalchemy.fields import Nested

from .. import db, ma


# class Route(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.Integer())




# class Fahrtstrecke(db.Model):
#     __tablename__ = 'ItemDetail'
#     id = db.Column(db.Integer, primary_key=True, index=True)
#     StreckeId = db.Column(db.Integer, db.ForeignKey('Item.id'))
#     detailId = db.Column(db.Integer, db.ForeignKey('Detail.id'))
#     endDate = db.Column(db.Date)

# class Item(db.Model):
#     __tablename__ = 'Item'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     description = db.Column(db.Text)
#     details = db.relationship('Detail', secondary=ItemDetail.__table__, backref='Item')

# class Detail(db.Model):
#     __tablename__ = 'Detail'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     value = db.Column(db.String)
#     items = db.relationship('Item', secondary=ItemDetail.__table__, backref='Detail')