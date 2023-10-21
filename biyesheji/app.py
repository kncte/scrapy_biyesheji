import random

import pymysql
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
# from flask_login import LoginManager
from flask_login import LoginManager
from flask_mail import Message, Mail

from biyesheji.route.admin import admin_blueprint
from biyesheji.route.auth import auth_blueprint, User, redis_client
from biyesheji.route.auth import config
from biyesheji.route.moviesss import movie_blueprint
from biyesheji.route.musicsss import music_blueprint
from biyesheji.route.newssss import new_blueprint
from biyesheji.route.tool import toolssssss

app = Flask(__name__)
CORS(app)
app.secret_key = '666666'
app.config['STATIC_FOLDER'] = 'static'

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = "请登录以继续访问该页面。"
app.config['MAIL_SERVER'] = "smtp.qq.com"
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "723927780@qq.com"
app.config['MAIL_PASSWORD'] = "befuxpqlfjkubbjh"
app.config['MAIL_DEFAULT_SENDER'] = "723927780@qq.com"
mail = Mail(app)
mysql = pymysql.connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    password=config['mysql']['password'],
    db='mydatabase',
    cursorclass=pymysql.cursors.DictCursor  # 设置游标类以返回字典格式的结果
)

app.register_blueprint(auth_blueprint, url_prefix='/')
app.register_blueprint(movie_blueprint, url_prefix='/')
app.register_blueprint(new_blueprint, url_prefix='/')
app.register_blueprint(music_blueprint, url_prefix='/')
app.register_blueprint(toolssssss, url_prefix='/')
app.register_blueprint(admin_blueprint, url_prefix='/')


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/send_email')
def send_emai():
    try:
        email = request.args.get('email')
        if not email:
            return jsonify({"code": 400, "message": "邮箱地址为空"}), 400

        captcha = random.randint(1111, 9999)

        # 创建邮件消息
        msg = Message('注册验证码', recipients=[email])
        msg.body = f'您的验证码是：{captcha}'

        # 发送邮件
        mail.send(msg)

        # 存储验证码到 Redis
        redis_client.set(email, captcha)

        return jsonify({"code": 200, "message": "验证码已发送"})
    except Exception as e:
        return jsonify({"code": 500, "message": f"邮件发送失败，原因：{str(e)}"}), 500


@app.route('/send_forget')
def send_forget():
    try:
        email = request.args.get('email')
        if not email:
            return jsonify({"code": 400, "message": "邮箱地址为空"}), 400

        captcha = random.randint(1111, 9999)

        # 创建邮件消息
        msg = Message('更换密码验证码', recipients=[email])
        msg.body = f'您的验证码是：{captcha}'
        print(msg.body)
        # 发送邮件
        mail.send(msg)

        # 存储验证码到 Redis
        redis_client.set(email, captcha)

        return jsonify({"code": 200, "message": "验证码已发送"})
    except Exception as e:
        print(jsonify({"code": 500, "message": f"邮件发送失败，原因：{str(e)}"}), 500)
        return jsonify({"code": 500, "message": f"邮件发送失败，原因：{str(e)}"}), 500


# 主页

@app.route('/')
def home111():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=1314)
