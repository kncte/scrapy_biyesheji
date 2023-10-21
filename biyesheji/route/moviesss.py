from flask import Flask, Blueprint, request, jsonify
from flask_login import login_required

from biyesheji import get_data
from biyesheji.moviesss.movie_search import search_movie

movie_blueprint = Blueprint('movie', __name__)


@movie_blueprint.route('/search_movie', methods=['GET'])
@login_required
def search():
    keyword = request.args.get('keyword', default='', type=str)
    print("映射的keyword", keyword)
    if keyword:
        movie_search_instance = search_movie(keyword)  # 创建 search_movie 类的实例并传递关键字参数
        result = movie_search_instance.search_movies_by_keyword()
        return jsonify(result)
    else:
        return jsonify([])


@movie_blueprint.route('/get_movie')
@login_required
def get_movie():
    page = int(request.args.get('page', 1))  # Get 'page' parameter from the request query string
    page_size = int(request.args.get('limit', 10))  # Get 'limit' parameter from the request query string
    movie = get_data.MovieDatabaseManager()
    json_data = movie.get_json_data(page, page_size)
    return json_data