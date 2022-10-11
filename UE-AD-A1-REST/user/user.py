from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

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

# get booking list for a user id
@app.route("/bookinglist/<id>", methods=['GET'])
def get_booking_list(id):
   res = call_service("booking", "/bookings/{}".format(id), "GET")
   return make_response(jsonify(res.json()),res.status_code)

# get movie list (with movie description) for a user id
@app.route("/usermovies/<id>", methods=['GET'])
def get_user_movies(id):
       
   # get booking list
   res = call_service("booking", "/bookings/{}".format(id), "GET")
   if res.status_code != 200:
      return make_response(jsonify(res.json()),res.status_code)

   moviesList = []
   
   # get movie description for each movie id
   for i in res.json().get("dates"):
      for j in i.get("movies"):
         res = call_service("movie", "/movies/{}".format(j), "GET")
         if res.status_code != 200:
            return make_response(jsonify(res.json()),res.status_code)
         moviesList.append(res.json())

   return make_response(jsonify(moviesList),200)

# get accessible API
@app.route("/accessibleapi", methods=['GET'])
def list_accessible_api():
   return make_response(jsonify({"user":ADDR["user"], "movie":ADDR["movie"], "booking":ADDR["booking"]}),200)

# get API description
@app.route("/apidescription", methods=['GET'])
def get_api_description():
   with open('{}/UE-archi-distribuees-user-1.0.0-resolved.yaml'.format("."), "r") as yaml:
      res = make_response(yaml.read(),200);
      res.headers["Content-Type"] = "text/plain"
      return res
   
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)

