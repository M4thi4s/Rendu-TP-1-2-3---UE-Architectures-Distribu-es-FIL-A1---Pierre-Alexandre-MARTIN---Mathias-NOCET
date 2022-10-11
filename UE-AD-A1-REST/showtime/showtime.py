from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

ADDR = {
   "movie": "127.0.0.1:3200",
   "booking": "127.0.0.1:3201",
   "showtime": "127.0.0.1:3202",
   "user": "127.0.0.1:3203"
}

with open('{}/databases/times.json'.format("."), "r") as jsf:
    schedule = json.load(jsf)["schedule"]

# home page
@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

# Get all showtime
@app.route("/showtimes", methods=['GET'])
def get_schedule():
    return make_response(jsonify(schedule),200)

# Get showtime for a date
@app.route("/showmovies/<date>", methods=['GET'])
def get_movie_byid(date):
    for movies in schedule:
        if str(movies["date"]) == str(date):
            res = make_response(jsonify(movies),200)
            return res
    return make_response(jsonify({"error":"bad input parameter"}),400)

# get accessible API
@app.route("/accessibleapi", methods=['GET'])
def get_accessible_api():
   return make_response(jsonify({"showtime":ADDR["showtime"]}),200)

# get API description
@app.route("/apidescription", methods=['GET'])
def get_api_description():
   with open('{}/UE-archi-distribuees-Showtime-1.0.0-resolved.yaml'.format("."), "r") as yaml:
      res = make_response(yaml.read(),200);
      res.headers["Content-Type"] = "text/plain"
      return res

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)

