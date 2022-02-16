from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


all_data_json = []

##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/random')
def random_coffe():
    all_coffies = db.session.query(Cafe).all()
    print(all_coffies)
    print(len(all_coffies))
    random_selector = random.randint(0, len(all_coffies))
    random_coffe = {"name": all_coffies[random_selector].name,
                    "map url": all_coffies[random_selector].map_url,
                    "img url": all_coffies[random_selector].img_url,
                    "location": all_coffies[random_selector].location,
                    "seats": all_coffies[random_selector].seats,
                    "toilets": all_coffies[random_selector].has_toilet,
                    "wifi": all_coffies[random_selector].has_wifi,
                    "sockets": all_coffies[random_selector].has_sockets,
                    "can you take a call": all_coffies[random_selector].can_take_calls,
                    "coffe price": all_coffies[random_selector].coffee_price}
    print(random_coffe)
    return jsonify(random_coffe)

@app.route('/all')
def all():
    all_coffies = db.session.query(Cafe).all()
    global all_data_json
    buffor = []
    for data in all_coffies:
        buffor = {"name": data.name,
                    "map url": data.map_url,
                    "img url": data.img_url,
                    "location": data.location,
                    "seats": data.seats,
                    "toilets": data.has_toilet,
                    "wifi": data.has_wifi,
                    "sockets": data.has_sockets,
                    "can you take a call": data.can_take_calls,
                    "coffe price": data.coffee_price}
        all_data_json.append(buffor)


    print(all_data_json)

    return jsonify(all_data_json)

@app.route('/search')
def search():
    location = request.args.get("loc")
    by_location = Cafe.query.filter_by(location=location).all()
    print(by_location)
    searched_by_location = []
    if by_location:
        for data in by_location:
            buffor = {"name": data.name,
                        "map url": data.map_url,
                        "img url": data.img_url,
                        "location": data.location,
                        "seats": data.seats,
                        "toilets": data.has_toilet,
                        "wifi": data.has_wifi,
                        "sockets": data.has_sockets,
                        "can you take a call": data.can_take_calls,
                        "coffe price": data.coffee_price}
            searched_by_location.append(buffor)

        return jsonify(searched_by_location)
    else:
        message = {"error": "Sory but hrere is no cafes in that location or the location is invalid"}
        return jsonify(message)


@app.route('/add', methods=['POST'])
def add():
    adding_buffor = Cafe(
                        name = request.args.get("name"),
                        map_url = request.args.get("map_url"),
                        img_url = request.args.get("img_url"),
                        location = request.args.get("location"),
                        seats = bool(request.args.get("seats")),
                        has_toilet = bool(request.args.get("has_toilet")),
                        has_wifi = bool(request.args.get("has_wifi")),
                        has_sockets = bool(request.args.get("has_sockets")),
                        can_take_calls = bool(request.args.get("can_take_calls")),
                        coffee_price = request.args.get("coffee_price")

    )
    try:
        db.session.add(adding_buffor)
        db.session.commit()
        print(adding_buffor)
        return jsonify(response={"succes": "Your coffee shop was added to database"})
    except:
        return jsonify(response={"error": "Argument's passed are invalid"}), 404

@app.route('/update-price/<int:id>', methods=['PATCH'])
def update_price(id):

    try:
        caffee_update = Cafe.query.get(id)
        caffee_update.coffee_price = request.args.get("new_price")
        db.session.commit()
        return jsonify(response={"congratulation": "coffe price was updated"})
    except:
        return jsonify(response={"error": "There is no coffe with this Id or inserted data are invalid "}), 404


@app.route('/report-closed/<int:id>', methods=['DELETE'])
def closed(id):
    # print(id)
    if request.args.get("api_key") == "TopSecretAPIKey":
        caffee_to_delete = db.session.query(Cafe).get(id)
        if caffee_to_delete:

            db.session.delete(caffee_to_delete)
            # print(caffee_to_delete)
            db.session.commit()
            return jsonify(response={"succes": "Congratulation the caffee was removed from database"})
        else:
            return jsonify(response={"error": "Invalid id item dos not exist in database"}), 404


    else:
        return jsonify(response={"error": "You don't have premission to remove coffees api_key reqired"}), 403




if __name__ == '__main__':
    app.run(debug=True)
