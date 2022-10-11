import json


# Resolver retournant la liste des films de la base de données
def get_all_movies(_, info):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        return movies["movies"]


# Resolver retournant un film en fonction de l'id passé en paramètres
def movie_with_id(_, info, _id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie


# Resolver permettant la modification de la note d'un film via son id
def update_movie_rate(_, info, _id, _rate):
    new_movies = {}
    new_movie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                new_movie = movie
                new_movies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(new_movies, wfile)
    return new_movie


# Resolver retournant la liste des acteurs présents dans un film
def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
        return actors


# Resolver retournant un acteur en fonction de l'id passé en paramètre
def actor_with_id(_, info, _id):
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        for actor in data['actors']:
            if actor['id'] == _id:
                return actor


# Resolver permettant l'ajout d'un film et retournant ce dernier
def add_movie(_, info, _id, _title, _director, _rate):
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie
        new_movie = {"title": _title, "rating": _rate, "director": _director, "id": _id}
        movies["movies"].append(new_movie)
        new_movies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(new_movies, wfile)
    return new_movie


# Resolver permettant la suppression d'un film et retournant ce dernier si réussite
def delete_movie(_, _info, _id):
    new_movies = {"title": "", "rating": "", "director": "", "id": -1}
    old_movie = None
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movies["movies"].remove(movie)
                new_movies = movies
                old_movie = movie
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(new_movies, wfile)
    return old_movie
