import grpc

import showtime_pb2
import showtime_pb2_grpc


def get_movies_by_date(stub, timeDate):
    movies = stub.GetMoviesByDate(timeDate)
    print("Movie at %s" %(timeDate.date))
    for movie in movies.MovieDatas:
        print("Movie with id %s" % (movie))


def get_show_times(stub):
    allShowtimes = stub.GetShowTimes(showtime_pb2.Empty())
    for showtime in allShowtimes:
        print("Showtime at %s" % (showtime.date))


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3002') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)

        print("-------------- GetShowTimes --------------")
        get_show_times(stub)

        print("-------------- GetMoviesByDate --------------")
        timeDate = showtime_pb2.Date(date="20151130")
        get_movies_by_date(stub, timeDate)

    channel.close()


if __name__ == '__main__':
    run()
