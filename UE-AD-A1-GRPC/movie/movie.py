import grpc
from concurrent import futures
import movie_pb2
import movie_pb2_grpc
import json
from google.protobuf.json_format import MessageToJson

class MovieServicer(movie_pb2_grpc.MovieServicer):

    def __init__(self):
        with open('{}/data/movies.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["movies"]

    # Get movie by ID
    def GetMovieByID(self, request, context):
        for movie in self.db:
            if movie['id'] == str(request.id):
                print("Movie found!")
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
        return movie_pb2.MovieData(title="", rating=-1, director="", id="")
    
    # Get all movie list
    def GetListMovies(self, request, context):
        for movie in self.db:
            yield movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])

    # Get movie by title
    def GetMovieByTitle(self, request, context):
        for movie in self.db:
            if movie['title'] == request.title:
                print("Movie found!")
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
        return movie_pb2.MovieData(title="", rating=-1, director="", id="")

    # Add a movie to the list
    def AddMovie(self, request, context):
        for movie in self.db:
            if movie['id'] == str(request.id):
                return movie_pb2.MovieData(title="", rating=-1, director="", id="")
        self.db.append(eval(MessageToJson(request)))
        print("Movie Added")
        return request

    # Delete a movie from the list
    def DeleteMovie(self, request, context):
        for movie in self.db:
            if str(movie["id"]) == str(request.id):
                self.db.remove(movie)
                print('Movie deleted')
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
        return movie_pb2.MovieData(title="", rating=-1, director="", id="")

    # Update a movie from the list
    def EditMovie(self, request, context):
        for movie in self.db:
            if str(movie["id"]) == str(request.movieID):
                movie["rating"] = request.rating
                print('Movie edited')
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
        return movie_pb2.MovieData(title="", rating=-1, director="", id="")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    movie_pb2_grpc.add_MovieServicer_to_server(MovieServicer(), server)
    server.add_insecure_port('[::]:3001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
