from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#client and order

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class User_order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'))
    line_id = db.Column(db.Integer, db.ForeignKey('line.id'))
    destination_station = db.Column(db.String(150))
    starting_station = db.Column(db.String(150))
    purchase_date = db.Column(db.DateTime(timezone=True), default=func.now())
    expire_date = db.Column(db.Date)
    price = db.Column(db.Float)

#PKP

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wagon_id = db.Column(db.Integer, db.ForeignKey('wagon.id'))
    seat_number = db.Column(db.Integer)

class Wagon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'))
    wagon_type = db.Column(db.String(25))

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train_name = db.Column(db.String(150))

class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'))
    first_station = db.Column(db.String(150))
    last_station = db.Column(db.String(150))

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.Integer, db.ForeignKey('line.id'))
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'))
    departure_time = db.Column(db.Time)

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(150))
    city = db.Column(db.String(150))