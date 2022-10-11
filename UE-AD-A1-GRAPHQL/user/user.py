from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound
from google.protobuf.json_format import MessageToJson

import grpc
import booking_pb2
import booking_pb2_grpc

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

ADDR = {
   "movie": "127.0.0.1:3200",
   "booking": "127.0.0.1:3201",
   "showtime": "127.0.0.1:3202",
   "user": "127.0.0.1:3203"
}

def call_service(service, endpoint, method, data=None):
   url = "http://{}".format(ADDR[service])
   if method == "GET":
      return requests.get(url + endpoint)
   elif method == "POST":
      return requests.post(url + endpoint, json=data)
   elif method == "PUT":
      return requests.put(url + endpoint, data=data)
   elif method == "DELETE":
      return requests.delete(url + endpoint)
   else:
      raise Exception("Unknown method")

with open('{}/data/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


def GetBookingByUserId(stubBooking, userId):
    return stubBooking.GetBookingByUserId(booking_pb2.UserId(userid=userId))


def GetMovieById(userId):
   res = call_service("movie", "/graphql", "POST", data={"query": "{movie_with_id(_id: \"" + userId + "\") {id, title, rating, actors {firstname, lastname, birthyear}}}"})
   return res.json().get("data").get("movie_with_id")

@app.route("/getlistbookings/<userId>", methods=['GET'])
def get_booking_list(userId):
    with grpc.insecure_channel('localhost:3003') as channel:
        stubBooking = booking_pb2_grpc.BookingStub(channel)
        booking_list = GetBookingByUserId(stubBooking, userId)

    channel.close()

    return make_response(eval(MessageToJson(booking_list)), 200, {'Content-Type': 'application/json'})


@app.route("/usermovies/<id>", methods=['GET'])
def get_user_movies(id):
    with grpc.insecure_channel('localhost:3003') as channel:
        stubBooking = booking_pb2_grpc.BookingStub(channel)
        booking_list = GetBookingByUserId(stubBooking, id)

    channel.close()

    movies_list = []

    for i in booking_list.dates:
        for j in i.movies:
            movies_list.append(GetMovieById(j))

    return make_response(jsonify(movies_list), 200)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)


# Convert python object to json string and return it
def toJson(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
