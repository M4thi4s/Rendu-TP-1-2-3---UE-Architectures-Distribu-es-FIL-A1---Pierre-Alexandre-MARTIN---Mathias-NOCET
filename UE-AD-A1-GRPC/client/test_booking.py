import grpc

import booking_pb2
import booking_pb2_grpc


def get_booking_by_user_id(stub, userid):
    bookings = stub.GetBookingByUserId(userid)
    print("Bookings for %s" %(userid.userid))
    for movies in bookings.dates:
        print("Booking for %s" % (movies.date))
        for movie in movies.movies:
            print("Movie id %s" %(movie))


def get_bookings(stub):
    allBookings = stub.GetBooking(booking_pb2.EmptyBooking())
    for booking in allBookings:
        print("User %s est inscrit" % (booking.userid))


def add_booking(stub, booking):
    msg_retour = stub.AddBooking(booking)
    print(msg_retour.msg)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3003') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)

        print("-------------- GetBooking --------------")
        get_bookings(stub)

        print("-------------- AddBooking --------------")
        booking = booking_pb2.AddBookingParameter(userid="dwight_schrute", date="20151205", movieid="39ab85e5-5e8e-4dc5-afea-65dc368bd7ab")
        add_booking(stub, booking)

        print("-------------- GetBookingByUserId --------------")
        userid = booking_pb2.UserId(userid="dwight_schrute")
        get_booking_by_user_id(stub, userid)

    channel.close()


if __name__ == '__main__':
    run()
