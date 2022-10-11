# from sympy import And, false
from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound
import requests

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

movies = []

ADDR = {
   "movie": "127.0.0.1:3200",
   "booking": "127.0.0.1:3201",
   "showtime": "127.0.0.1:3202",
   "user": "127.0.0.1:3203"
}

# connect to TMDB and get popular films
url = "https://imdb-api.com/en/API/Top250Movies/k_kkrkqjg3"
response = requests.get(url)

movies = response.json()["items"]

print(movies)


# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


# Load a html page from a template
@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'), 200)


# Get all movies
@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res


# Get movie from ID
@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie), 200)
            return res
    return make_response(jsonify({"error": "Movie ID not found"}), 400)


# Get movies from title search
@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie

    if not json:
        res = make_response(jsonify({"error": "movie title not found"}), 400)
    else:
        res = make_response(jsonify(json), 200)
    return res


# Add a movie
@app.route("/movies/<movieid>", methods=['POST'])
def create_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error": "movie ID already exists"}), 409)

    movies.append(req)
    res = make_response(jsonify({"message": "movie added"}), 201)
    return res


# Edit movie rate
@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = float(rate)
            res = make_response(jsonify(movie), 200)
            return res

    res = make_response(jsonify({"error": "movie ID not found"}), 201)
    return res


# Delete a movie
@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie), 200)

    res = make_response(jsonify({"error": "movie ID not found"}), 400)
    return res


# Get accessible API
@app.route("/accessibleapi", methods=['GET'])
def list_accessible_api():
    return make_response(jsonify({"movie":ADDR["movie"]}),200)


# Get API description
@app.route("/apidescription", methods=['GET'])
def get_api_description():
    with open('{}/UE-archi-distribuees-Movie-1.0.0-resolved.yaml'.format("."), "r") as yaml:
        res = make_response(yaml.read(),200);
        res.headers["Content-Type"] = "text/plain"
        return res


def checkInt(str):
    try:
        int(str)
        return True
    except ValueError:
        return False


# Get "n" best movies by ratings
@app.route("/bestmoviesbyratings/<number>", methods=['GET'])
def get_best_movies_by_ratings(number):
    if not(checkInt(number)) or 1 > int(number) > len(movies):
        res = make_response(jsonify({"error": "inconsistent number"}), 400)
        return res
    
    # res = make_response(jsonify(sorted(movies, key=lambda d: d['rating'], reverse=True)[0:int(number)]), 200)
    res = make_response(jsonify(sorted(movies, key=lambda d: d['imDbRating'], reverse=True)[0:int(number)]), 200)
    return res


if __name__ == "__main__":
    # p = sys.argv[1]
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)
