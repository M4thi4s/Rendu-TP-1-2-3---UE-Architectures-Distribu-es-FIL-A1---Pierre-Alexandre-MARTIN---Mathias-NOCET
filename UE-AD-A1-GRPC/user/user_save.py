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


def GetBookingByUserId(stubBooking, userId):
    return stubBooking.GetBookingByUserId(booking_pb2.UserId(userid=userId))


def GetMovieById(stubMovie, userId):
    return stubMovie.GetMovieByID(movie_pb2.MovieID(id=userId))


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
   
   moviesList = []

   for i in booking_list.dates:
      for j in i.movies:
         with grpc.insecure_channel('localhost:3001') as channel:
            stubMovie = movie_pb2_grpc.MovieStub(channel)
            moviesList.append(json.dumps(GetMovieById(stubMovie, j)))
         channel.close()
         
   return make_response(jsonify(moviesList), 200)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
   
# Convert python object to json string and return it
def toJson(self):
       return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
