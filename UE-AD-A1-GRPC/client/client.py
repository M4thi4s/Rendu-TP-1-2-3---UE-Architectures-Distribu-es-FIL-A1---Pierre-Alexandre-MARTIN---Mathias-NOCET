import grpc

import movie_pb2
import movie_pb2_grpc


def get_movie_by_id(stub, id):
    movie = stub.GetMovieByID(id)
    print(movie)


def get_list_movies(stub):
    allmovies = stub.GetListMovies(movie_pb2.Empty())
    for movie in allmovies:
        print("Movie called %s" % (movie.title))


def add_movie(stub, movieData):
    movie = stub.AddMovie(movieData)
    print(movie)


def edit_movie(stub, movieData):
    movie = stub.EditMovie(movieData)
    print(movie)


def delete_movie(stub, movieData):
    movie = stub.DeleteMovie(movieData)
    print(movie)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3001') as channel:
        stub = movie_pb2_grpc.MovieStub(channel)

        print("-------------- GetMovieByID --------------")
        movieid = movie_pb2.MovieID(id="a8034f44-aee4-44cf-b32c-74cf452aaaae")
        get_movie_by_id(stub, movieid)
        
        print("-------------- GetListMovies --------------")
        get_list_movies(stub)

        print("-------------- AddMovie --------------")
        movieData = movie_pb2.MovieData(title="Cobaye", rating=2, director="PAMathias", id="123456")
        add_movie(stub, movieData)

        print("-------------- EditMovie --------------")
        rateData = movie_pb2.EditData(movieID="123456", rating=8)
        edit_movie(stub, rateData)

        print("-------------- DeleteMovie --------------")
        delData = movie_pb2.MovieID(id="123456")
        delete_movie(stub, delData)
        
    channel.close()


if __name__ == '__main__':
    run()
