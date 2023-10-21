from flask import Blueprint, request, jsonify
from flask_login import login_required

from biyesheji import get_data
from biyesheji.newssss.new_search import search_new

new_blueprint = Blueprint('new', __name__)


@new_blueprint.route('/search_new', methods=['GET'])
@login_required
def search_newssss():
    new_key = request.args.get('keyword', default='', type=str)
    print("映射的music_key", new_key)
    if new_key:

        new_search_instance = search_new(new_key)  # 创建 search_movie 类的实例并传递关键字参数
        print(new_search_instance)
        result = new_search_instance.search_new_by_keyword()
        return jsonify(result)
    else:
        return jsonify([])


@new_blueprint.route('/get_news')
@login_required
def get_news():
    page = int(request.args.get('page', 1))  # Get 'page' parameter from the request query string
    page_size = int(request.args.get('limit', 10))  # Get 'limit' parameter from the request query string
    news = get_data.NewsDatabaseManager()
    json_data = news.get_json_data(page, page_size)
    return json_data
