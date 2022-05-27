from .. import db

# trips = db.Table(
#     'trip',
#     db.Column(''))

# lines = db.Table('lines',
#     db.Column('section_id', db.Integer, db.ForeignKey('section.id'), primary_key=True),
#     db.Column('route_id', db.Integer, db.ForeignKey('route.id'), primary_key=True)
# )

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    left_id = db.Column(db.Integer, db.ForeignKey('left.id'), primary_key=True)
    right_id = db.Column(db.Integer, db.ForeignKey('right.id'), primary_key=True)

    extra_data = db.Column(db.String(50))

    left = db.relationship('Left', backref=db.backref('right_association'))
    right = db.relationship('Right', backref=db.backref('left_association'))
    descr = db.Column(db.String(100))
    
    
    
    
class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descr = db.Column(db.String(100))
    line_id = db.Column(db.Integer(), db.ForeignKey('line.id'))
    # line_name = db.Column(db.String(), db.ForeignKey('line.name')) # ? selbes tupel ?
    

    line = db.relationship('Line', backref=db.backref('line_association'))
    sections = db.relationship('Section', backref=db.backref('section_association'))
    

class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descr = db.Column(db.String(100))
    sections = db.relationship('Section', secondary=route, lazy='subquery',
        backref=db.backref('routes', lazy=True))

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(100))
    end = db.Column(db.String(100))
    duration = db.Column(db.Integer())