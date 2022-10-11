from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

ADDR = {
   "movie": "127.0.0.1:3200",
   "booking": "127.0.0.1:3201",
   "showtime": "127.0.0.1:3202",
   "user": "127.0.0.1:3203"
}

# call the micro service to get datas
def call_service(service, endpoint, method, data=None):
    url = "http://{}".format(ADDR[service])
    if method == "GET":
        return requests.get(url + endpoint)
    elif method == "POST":
        return requests.post(url + endpoint, data=data)
    elif method == "PUT":
        return requests.put(url + endpoint, data=data)
    elif method == "DELETE":
        return requests.delete(url + endpoint)
    else:
        raise Exception("Unknown method")

# get all bookings
with open('{}/databases/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]

# home page
@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


# Get all movies
@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res

# Get booking for a user id
@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_byuserid(userid):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            res = make_response(jsonify(booking), 200)
            return res
    return make_response(jsonify({"error": "User ID not found"}), 400)

# add a booking for a user
@app.route("/bookings/<userid>", methods=['POST'])
def create_booking(userid):
    req = request.get_json()

    # check if showtime exist for movie at the date send
    res = call_service("showtime", "/showmovies/{}".format(req["date"]), "GET")
    if res.status_code != 200:
        return make_response(jsonify({"error": "call showtime error"}), res.status_code)

    if req["date"] in res.json()["date"]:
        print("Movie found!")
        
        for booking in bookings:
            if str(booking["userid"]) == str(userid):
                for date in booking["dates"]:
                    if req["movieid"] in date["movies"]:
                        return make_response(jsonify({"error": "an existing item already exists"}), 409)
                for date in booking["dates"]:
                    if req["date"] == date["date"]:
                        date["movies"].append(req["movieid"])
                        return make_response(jsonify({"message": "Booking added"}), 200)
                booking["dates"].append({"date": req["date"], "movies": [req["movieid"]]})
                return make_response(jsonify({"message": "Booking added"}), 200)

        bookings.append({"dates": [{"date": req["date"], "movies": [req["movieid"]]}], "userid": userid})
        return make_response(jsonify({"message": "Booking added"}), 200);
    
    else:
        print("Movie not found at the date send!")
        return make_response(jsonify({"error": "an existing item already exists"}), 409)

# liste les API accessibles à l'utilisateur
@app.route("/accessibleapi", methods=['GET'])
def list_accessible_api():
    return make_response(jsonify({"booking":ADDR["booking"], "movie":ADDR["movie"]}),200)

# description de l'API
@app.route("/apidescription", methods=['GET'])
def get_api_description():
    with open('{}/UE-archi-distribuees-Booking-1.0.0-resolved.yaml'.format("."), "r") as yaml:
        res = make_response(yaml.read(), 200);
        res.headers["Content-Type"] = "text/plain"
        return res


if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
