from flask import Blueprint, render_template, request, flash, jsonify,  redirect, url_for
from flask_login import login_required, current_user
from . import db
import json
from website.generate_seat import find_conection, avaible_seats, travel_info, get_ticket_info, get_station
from sqlalchemy import text
from sqlalchemy.sql import func

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    return redirect(url_for(".search"))


@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    station_list = get_station()
    if request.method == 'POST':
        starting_station = request.form.get('starting_station')
        destination_station = request.form.get('destination_station')
        arrival_date = request.form.get('arrival_date')
        num_ticket = request.form.get('num_ticket')
        if starting_station == destination_station:
            flash('Podaj różne stacje', category='error')
        elif arrival_date=="":
            flash('Podaj date podróży', category='error')
        elif num_ticket=="":
            flash('Podaj liczbe biletów', category='error')
        else:
            return redirect(url_for('.chooseLine', starting_station=starting_station, destination_station=destination_station, arrival_date=arrival_date, num_ticket=num_ticket))

    return render_template("search.html", user=current_user, station_list=station_list)

@views.route('/chooseLine', methods=['GET', 'POST'])
@login_required
def chooseLine():
    try:
        starting_station = request.args['starting_station']
        destination_station = request.args['destination_station']
        arrival_date = request.args['arrival_date']
        num_ticket =int(request.args['num_ticket'])
        avaible_seat = []
        line_info = []

        avaible_line = find_conection(starting_station, destination_station)

        for line in avaible_line:
            avaible_seat.append(avaible_seats(line[0], arrival_date))
            line_info.append(travel_info(line[0],starting_station, destination_station, avaible_seat[-1][1], avaible_seat[-1][0]))

        return render_template("chooseLine.html", user=current_user, avaible_seat=avaible_seat, line_info=line_info,
                               starting_station=starting_station, destination_station=destination_station, arrival_date=str(arrival_date), num_ticket=num_ticket)
    except:
        return render_template("home.html", user=current_user)

@views.route('/buy-ticket', methods=['POST'])
@login_required
def buy_ticket():
    dict = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    line_id = dict['line_id']
    expire_date = dict['date']
    seat_id = dict['seat_id']
    destination_station = dict['destination_station']
    starting_station = dict['starting_station']
    price = dict['price']
    num_ticket = dict["num_ticket"]
    purchase_date = func.now()
    print(seat_id)
    print(num_ticket)
    for i in range(num_ticket):
        db.session.execute(text("INSERT INTO "
                                "`ticket`(`id`, `user_id`, `seat_id`, `line_id`, `destination_station`, `starting_station`, `expire_date`, `price`) "
                                "VALUES(NULL, :user_id, :seat_id, :line_id, :destination_station, :starting_station, :expire_date, :price)"),
                           {'user_id': current_user.id, 'seat_id': seat_id[i], 'line_id': line_id, 'destination_station': destination_station,
                            'starting_station': starting_station, 'expire_date': expire_date, 'price': price, 'purchase_date': purchase_date})
        db.session.commit()
        db.session.execute(text("INSERT INTO `user_order`(`price`, `user_id`) VALUES(:price, :user_id)"), {'user_id': current_user.id,'price': price})
        db.session.commit()
    db.session.close()

    return jsonify({})

@views.route('/tickets', methods=['GET', 'POST'])
@login_required
def tickets():
    ticket_info, train_info = get_ticket_info(current_user.id)

    return render_template("tickets.html", user=current_user, ticket_info=ticket_info, train_info=train_info, length=len(ticket_info))

@views.route('/delete-ticket', methods=['POST'])
@login_required
def delete_ticket():
    dict = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    ticketId = dict['ticketId']
    print(ticketId)
    ticket = db.session.execute(text("SELECT * FROM `ticket` WHERE `ticket`.`id` = :ticketId"), {'ticketId': ticketId}).one()
    print(ticket)
    if ticket:
        if ticket[1] == current_user.id:
            db.session.execute(text("DELETE FROM `ticket` WHERE `ticket`.`id` = :ticketId"),{'ticketId':ticketId})
            db.session.commit()

    return jsonify({})