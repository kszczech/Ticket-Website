# from flask import Flask
# # from flask_sqlalchemy import SQLAlchemy
# # import pymysql
# # from os import path
# # from flask_login import LoginManager
# #
# # db = SQLAlchemy()
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text
import random
DB_USER = "kszczec2"
DB_PASS = "Gh0Hcr4uTnPi2JxL"
DB_HOST = "mysql.agh.edu.pl"
DB_NAME = "kszczec2"
DB_PORT = 3306
# #
# # def create_app():
# #     print(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}')
# #     app = Flask(__name__)
# #     app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
# #     app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}'
# #     db.init_app(app)
# #     return app
# #
# # app = create_app()
# # app.run(debug=True)
# #
# # result = db.session.execute('SELECT * FROM seat WHERE', {'val': 5})
# # print(result)


def generate_seat():
    engine = sqlalchemy.create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}')
    Session = scoped_session(sessionmaker(bind=engine))
    #
    # s = Session()
    # result = s.execute(text("SELECT * FROM seat WHERE seat_number = :val"), {'val': 5})
    # print(result)
    # r_dict = []
    # for r in result:
    #     print(r[1]) # Access by positional index


    s = Session()
    wagons = s.execute(text("SELECT * FROM wagon"))

    seat_list = []
    for wagon in wagons:
        for seat_num in range(1,7):
            line = []
            line.append(None)
            line.append(wagon[0])
            line.append(seat_num)
            seat_list.append(line)
    print(seat_list)
    for seat in seat_list:
        print(seat)
        s.execute(text("INSERT INTO seat (id, wagon_id, seat_number) VALUES (NULL, :wagon_id, :seat_num)"), {'wagon_id' : seat[1], 'seat_num' : seat[2]})
    s.commit()
    s.close()

def generate_route(start_hour,start_min, line):
    engine = sqlalchemy.create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}')
    Session = scoped_session(sessionmaker(bind=engine))

    s = Session()
    stations = s.execute(text("SELECT * FROM station"))
    lines = s.execute(text("SELECT * FROM line WHERE id = :line_id"), {'line_id' : line})
    for line in lines:
        first = line[2]

    time_hour = start_hour
    time_min = start_min
    stations_list = []
    time_list = []

    for station in stations:
        tem_min = 0
        print(station)
        tem_min = random.randint(13, 20) + time_min
        if tem_min >= 60:
            # print("nienormalne",tem_min)
            time_hour += 1
            time_min = 0
            # print("reszta:",tem_min % 60)
            time_min += tem_min % 60
        else:
            # print("zwykłe:", tem_min)
            time_min = tem_min
        if time_min < 10:
            departure_time = f"{time_hour}:0{time_min}:00"
        elif time_min < 10 and time_hour < 10:
            departure_time = f"0{time_hour}:0{time_min}:00"
        elif time_hour < 10:
            departure_time = f"0{time_hour}:{time_min}:00"
        else:
            departure_time = f"{time_hour}:{time_min}:00"
        time_list.append(departure_time)
        if first == "Krakow":
            stations_list.append(station[0])
        else:
            stations_list.insert(0,station[0])
    print(stations_list)
    print(time_list)

    for i in range(len(stations_list)):
        s.execute(text("INSERT INTO `route` (`id`, `line_id`, `station_id`, `departure_time`) VALUES (NULL, :line_id, :station_id, :departure_time)"),
                  {'line_id': line[0], 'station_id': stations_list[i], 'departure_time':time_list[i]})
    s.commit()
    s.close()


def find_conection(start, end):
    engine = sqlalchemy.create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}')
    Session = scoped_session(sessionmaker(bind=engine))

    s = Session()
    stations = s.execute(text("SELECT * FROM station"))
    lines = s.execute(text("SELECT * FROM line"))

    for id in s.execute(text("SELECT * FROM station WHERE city=:start"), {"start":start}):
        start_id = id[0]
    for id in s.execute(text("SELECT * FROM station WHERE city=:end"), {"end":end}):
        end_id = id[0]

    avaible_line = []

    for line in lines:
        for start_station in s.execute(text("SELECT * FROM route WHERE line_id = :line_id and station_id = :station_id"),
                                  {"line_id": line[0], "station_id": start_id}):
            start_time = start_station[3]
        for end_station in s.execute(text("SELECT * FROM route WHERE line_id = :line_id and station_id = :station_id"),
                                  {"line_id": line[0], "station_id": end_id}):
            end_time = end_station[3]

        if start_time < end_time:
            avaible_line.append(line)
    s.close()
    print(avaible_line)
    return avaible_line

def avaible_seats(lineId, date):
    engine = sqlalchemy.create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}')
    Session = scoped_session(sessionmaker(bind=engine))
    avaible_seat = []
    s = Session()

    # first_stationID = s.execute(text("SELECT station.id FROM station WHERE station.city = :startingStation "), {'startingStation': startingStation}).one()[0]
    #
    # timeStart = s.execute(text("SELECT route.departure_time FROM route WHERE route.line_id = :lineId and route.station_id = :first_stationID"), {'lineId': lineId, 'first_stationID': first_stationID}).one()[0]
    #
    # print(str(timeStart))
    #
    # full_date = str(date) + " " + str(timeStart)

    seats = s.execute(text("SELECT seat.id FROM seat, wagon, train, line WHERE "
                           "train.id = line.train_id AND "
                           "wagon.train_id = train.id AND "
                           "seat.wagon_id = wagon.id AND "
                           "line.id = :line_id "
                           "EXCEPT SELECT ticket.seat_id FROM ticket WHERE ticket.expire_date = :date"), {'line_id': lineId, 'date': date})

    for seat in seats:
        avaible_seat.append(seat[0])
    s.close()
    return avaible_seat, len(avaible_seat)

def travel_info(line_id, start, end, seat_num, seat_list):
    engine = sqlalchemy.create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}')
    Session = scoped_session(sessionmaker(bind=engine))
    s = Session()

    start_id = s.execute(text("SELECT station.id FROM station WHERE city=:start"), {"start":start}).one()[0]
    end_id = s.execute(text("SELECT station.id FROM station WHERE city=:end"), {"end":end}).one()[0]

    time_departure = s.execute(text("SELECT departure_time FROM route WHERE line_id=:line_id and station_id=:station_id"), {"line_id":line_id, "station_id":start_id}).one()[0]
    time_arrival = s.execute(text("SELECT departure_time FROM route WHERE line_id=:line_id and station_id=:station_id"), {"line_id":line_id, "station_id":end_id}).one()[0]


    time_departure_list = str(time_departure).split(":")
    time_arrival_list = str(time_arrival).split(":")

    price = ((int(time_arrival_list[0]) - int(time_departure_list[0]))*60 + (int(time_arrival_list[1]) - int(time_departure_list[1]))) * 0.4
    price = round(price, 2)

    price_sum = round(price * int(seat_num), 2)

    s.close()
    return {'line_id': line_id, 'time_departure' : time_departure, 'time_arrival': time_arrival, 'price' : price, 'seat_num' : seat_num, 'seat_list': seat_list}

def get_ticket_info(user_id):
    engine = sqlalchemy.create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}')
    Session = scoped_session(sessionmaker(bind=engine))
    s = Session()
    ticket_info = []
    train_info = []
    ticket_id_list = s.execute(text("SELECT id FROM ticket WHERE user_id = :ticket_id"),
                      {'ticket_id': user_id})

    for ticket_id in ticket_id_list:
        ticket_info.append(s.execute(text("SELECT * FROM ticket WHERE id = :ticket_id"),
                          {'ticket_id': ticket_id[0]}).one())

        seat_id = ticket_info[-1][2]
        train_info.append(s.execute(text("SELECT seat.seat_number, wagon.id, wagon.wagon_type, train.train_name FROM seat, wagon, train WHERE "
                               "wagon.train_id = train.id AND "
                               "seat.wagon_id = wagon.id AND "
                               "seat.id = :seat_id"),
                          {'seat_id': seat_id}).one())

    s.close()
    return ticket_info, train_info

def get_station():
    engine = sqlalchemy.create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}')
    Session = scoped_session(sessionmaker(bind=engine))
    s = Session()

    stations = s.execute(text("SELECT station.city FROM station"))
    station_list = []

    for station in stations:
        station_list.append(station[0])

    return station_list

def get_user_order(user_id):
    engine = sqlalchemy.create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}')
    Session = scoped_session(sessionmaker(bind=engine))
    s = Session()

    orders = s.execute(text("SELECT * FROM user_order WHERE user_id = :user_id"), {'user_id': user_id})
    orders_list = []

    for order in orders:
        orders_list.append(order[0])
    print(orders_list)
    return orders_list

if __name__ == '__main__':
    #generate_seat(),
    #generate_route(17, 30, 7)
    # avaible_line = find_conection("Krakow", "Tarnow")
    # avaible_seat, num = avaible_seats(1, "2023-02-09")
    # travel_info(1, 'Krakow', 'Przemysl', 2)
    # get_ticket_info(1)
    # get_station()
    get_user_order(1)





