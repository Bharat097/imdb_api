import os
from os import name
from flask import Blueprint, request, jsonify
from flask import json
from flask.globals import current_app
from flask.views import MethodView
from app.auth.helper import token_required, response
from app.models import User, MovieData


# Initialize blueprint
imdb = Blueprint('imdb', __name__)

DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class GetMovies(MethodView):
    """
    View functions for search movie
    """
    decorators = [token_required]

    def load_db(self, current_user):
        filename = os.path.join(DIR, 'imdb.json')
        with open(filename, 'r') as f:
            content = json.load(f)
            for each in content[50:]:
                movie = MovieData(
                    name=each.get('name'),
                    director=each.get('director'),
                    imdb_score=float(each.get('imdb_score')),
                    popularity=float(each.get('99popularity'))
                    )
                movie.save()
                print("saved {}".format(movie))

    def get(self, current_user):
        if not request.args:
            movies = MovieData.query.all()
            return jsonify([movie.to_json() for movie in movies])
        params = request.args
        movies = MovieData.query.filter_by(**params).all()
        return jsonify([movie.to_json() for movie in movies])


class Movie(MethodView):
    decorators = [token_required]

    def post(self, current_user):
        if not current_user.is_admin:
            return response("Unauthorized", "Unauthorized", 401)
        if not request.get_json():
            return response(
                status='failed',
                message='Missing Payload',
                status_code=400
            )
        post_data = request.get_json()

        if not post_data.get('name'):
            return response(
                status='failed',
                message='Name is Missing',
                status_code=400
            )
        if not post_data.get('director'):
            return response(
                status='failed',
                message='Director is Missing',
                status_code=400
            )
        if not post_data.get('rating') or not(0 <= float(post_data.get('rating')) <= 10):
            return response(
                status='failed',
                message='Rating is Missing or Invalid(0 <= Rating <= 10)',
                status_code=400
            )
        if not post_data.get('popularity') or not(0 <= float(post_data.get('popularity')) <= 100):
            return response(
                status='failed',
                message='Popularity is Missing or Invalid(0 <= Rating <= 100)',
                status_code=400
            )
        movie = MovieData(
            post_data.get('name'),
            post_data.get('director'),
            float(post_data.get('rating')),
            float(post_data.get('popularity'))
            )
        movie.save()
        return response(
            status='success',
            message='Successfully Added',
            status_code=201
        )

    def delete(self, current_user):
        if not current_user.is_admin:
            return response("Unauthorized", "Unauthorized", 401)
        params = request.args
        if not params or not params.get('name'):
            return response("failed", "Missing Param", 400)
        movie = MovieData.get_by_name(params.get('name'))
        movie.remove()
        return response(
            status='success',
            message='Successfully Deleted',
            status_code=200
        )

    def put(self, current_user):
        if not current_user.is_admin:
            return response("Unauthorized", "Unauthorized", 401)
        params = request.get_json()
        if not params or not params.get('name'):
            return response("failed", "Missing Param", 400)
        movie = MovieData.get_by_name(params.get('name'))
        if not movie:
            return response(
                status='failed',
                message='Movie Not Found',
                status_code=400
            )
        if params.get('director'):
            movie.director = params.get('director')
        if params.get('rating'):
            movie.imdb_score = params.get('rating')
        if params.get('popularity'):
            movie.popularity = params.get('popularity')
        movie.save()
        return response(
            status='success',
            message='Successfully Updated',
            status_code=200
        )


imdb.add_url_rule('/movies', view_func=GetMovies.as_view('get_movies'))
imdb.add_url_rule('/movie/add', view_func=Movie.as_view('add_movie'), methods=['POST', ])
imdb.add_url_rule('/movie/update', view_func=Movie.as_view('update_movie'), methods=['PUT', ])
imdb.add_url_rule('/movie/delete', view_func=Movie.as_view('delete_movie'), methods=['DELETE', ])
