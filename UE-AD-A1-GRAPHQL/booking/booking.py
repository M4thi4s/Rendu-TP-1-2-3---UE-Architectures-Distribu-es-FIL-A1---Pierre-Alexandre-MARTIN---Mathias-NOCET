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
   
    def GetBookingByUserId(self, request, context):
        for booking in self.db:
            if booking['userid'] == request.userid:
                print("Booking found!")
                return booking_pb2.BookingData(userid=booking['userid'], dates=booking['dates'])
        return booking_pb2.BookingData(userid="", dates=[])
      
    def GetBooking(self, request, context):
        for booking in self.db:
            yield booking_pb2.BookingData(userid=booking['userid'], dates=booking['dates'])
   
    def AddBooking(self, request, context):
        added = False
        with grpc.insecure_channel('localhost:3002') as channel:
            stub = showtime_pb2_grpc.ShowtimeStub(channel)

            dateParameter = showtime_pb2.Date(date=request.date)
            response = stub.GetMoviesByDate(dateParameter)

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
