from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound
from google.protobuf.json_format import MessageToJson

import grpc
import movie_pb2
import movie_pb2_grpc
import booking_pb2
import booking_pb2_grpc

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]

# call the micro service to get bookings datas by user id
def GetBookingByUserId(stubBooking, userId):
    return stubBooking.GetBookingByUserId(booking_pb2.UserId(userid=userId))

# call the micro service to get movies datas by film id
def GetMovieById(stubMovie, userId):
    return stubMovie.GetMovieByID(movie_pb2.MovieID(id=userId))

# get booking list for a user id
@app.route("/getlistbookings/<userId>", methods=['GET'])
def get_booking_list(userId):
    with grpc.insecure_channel('localhost:3003') as channel:
        stubBooking = booking_pb2_grpc.BookingStub(channel)
        booking_list = GetBookingByUserId(stubBooking, userId)

    channel.close()

    return make_response(eval(MessageToJson(booking_list)), 200, {'Content-Type': 'application/json'})

# get movie list (with movie description) for a user id
@app.route("/usermovies/<id>", methods=['GET'])
def get_user_movies(id):
    
    # get booking list by user id
    with grpc.insecure_channel('localhost:3003') as channel:
        stubBooking = booking_pb2_grpc.BookingStub(channel)
        booking_list = GetBookingByUserId(stubBooking, id)

    channel.close()

    movies_list = []

    # get movie description for each movie id
    for i in booking_list.dates:
        for j in i.movies:
            with grpc.insecure_channel('localhost:3001') as channel:
                stub_movie = movie_pb2_grpc.MovieStub(channel)
                movies_list.append(eval(MessageToJson(GetMovieById(stub_movie, j))))
            channel.close()

    return make_response(jsonify(movies_list), 200)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)


# Convert python object to json string and return it
def toJson(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
