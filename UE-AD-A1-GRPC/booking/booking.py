import grpc
from concurrent import futures

import booking_pb2
import booking_pb2_grpc
import json
import showtime_pb2
import showtime_pb2_grpc

class BookingServicer(booking_pb2_grpc.BookingServicer):
    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
   
    # Get booking of a user ID
    def GetBookingByUserId(self, request, context):
        for booking in self.db:
            if booking['userid'] == request.userid:
                print("Booking found!")
                return booking_pb2.BookingData(userid=booking['userid'], dates=booking['dates'])
        return booking_pb2.BookingData(userid="", dates=[])
      
    # Get all bookings
    def GetBooking(self, request, context):
        for booking in self.db:
            yield booking_pb2.BookingData(userid=booking['userid'], dates=booking['dates'])
   
    # Add a booking for a user
    def AddBooking(self, request, context):
        added = False
        with grpc.insecure_channel('localhost:3002') as channel:
            # check if showtime exist for movie at the date send
            stub = showtime_pb2_grpc.ShowtimeStub(channel)

            dateParameter = showtime_pb2.Date(date=request.date)
            response = stub.GetMoviesByDate(dateParameter)

            # if showtime exist => add movie to booking
            # On laisse la possibilité à un utilisateur d'acheter plusieurs place (ex : 2 places pour un couple)
            if request.movieid in response.MovieDatas:
                print("Movie found!")
                self.db.append(request)
                added = True
            else:
                print("Movie not found!")
         
        channel.close()

        if added:
            return booking_pb2.AddBookingReturnMessage(msg="item added")
        else:
            return booking_pb2.AddBookingReturnMessage(msg="item not added")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3003')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
