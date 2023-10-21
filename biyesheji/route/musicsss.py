from flask import Blueprint, request, jsonify
from flask_login import login_required

from biyesheji import get_data
from biyesheji.musicsss.music_search import search_music

music_blueprint = Blueprint('music', __name__)


@music_blueprint.route('/get_music')
@login_required
def get_music():
    page = int(request.args.get('page', 1))  # Get 'page' parameter from the request query string
    page_size = int(request.args.get('limit', 10))  # Get 'limit' parameter from the request query string
    music = get_data.MusicDatabaseManager()
    json_data = music.get_json_data(page, page_size)
    return json_data


@music_blueprint.route('/search_music', methods=['GET'])
@login_required
def search_musicsss():
    music_key = request.args.get('keyword', default='', type=str)
    print("映射的music_key", music_key)
    if music_key:
        music_search_instance = search_music()  # 创建 search_movie 类的实例并传递关键字参数
        print(music_search_instance)
        result = music_search_instance.search_music_by_keyword(music_key)
        return jsonify(result)
    else:
        return jsonify([])
