# app.py
from flask import Flask, render_template, jsonify
from threading import Thread
import subprocess

app = Flask(__name__)


def run_spider():
    subprocess.run(['scrapy', 'crawl', 'movie'])


@app.route('/')
def index():
    return render_template('1.html')


@app.route('/data')
def get_data():
    # 在此处获取爬取的数据，可以从文件或数据库中读取
    data = {'example_key': 'example_value'}
    return jsonify(data)


if __name__ == '__main__':
    # 在启动Flask应用时，启动爬虫线程
    spider_thread = Thread(target=run_spider)
    spider_thread.start()
    app.run(debug=True)
