import configparser
import os
import random

import pymysql
import redis
from flask import Blueprint, flash, redirect, url_for, request, session, send_file, render_template, jsonify, \
    current_app, make_response
from flask_jwt_extended import create_access_token, jwt_required
from flask_login import login_required, logout_user, login_user, UserMixin, current_user

import random
import string
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
import os

from biyesheji.authentication import set_password, check_password, creat_token, token_required

auth_blueprint = Blueprint('auth', __name__)

current_directory = os.path.dirname(os.path.realpath(__file__))
config_file_path = os.path.join(current_directory, '..', 'config.ini')
config = configparser.ConfigParser()
config.read(config_file_path)

mysql = pymysql.connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    password=config['mysql']['password'],
    db='mydatabase',
    cursorclass=pymysql.cursors.DictCursor  # 设置游标类以返回字典格式的结果
)
redis_client = redis.Redis(host='121.196.205.18', port=6379, db=0, password=123456)


# current_app.config['MAIL_SERVER'] = "smtp.qq.com"
# current_app.config['MAIL_USE_SSL'] = True
# current_app.config['MAIL_PORT'] = 465
# current_app.config['MAIL_USERNAME'] = "723927780@qq.com"
# current_app.config['MAIL_PASSWORD'] = "befuxpqlfjkubbjh"
# current_app.config['MAIL_DEFAULT_SENDER'] = "723927780@qq.com"
#
# mail = Mail(current_app)


@auth_blueprint.route('/logout')
@login_required  # 保证只有登录用户可以注销
def logout():
    logout_user()  # 注销用户
    flash('退出成功', 'success')
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        captcha = request.form['captcha']
        email_code = redis_client.get(email)
        if email_code:
            email_code = email_code.decode('utf-8')
        print(email_code, captcha)
        # cur = mysql.connection.cursor()
        if email_code:
            if email_code == captcha:
                cur = mysql.cursor()
                cur.execute("SELECT * FROM userdatabase WHERE username = %s", username)
                user = cur.fetchone()
                print(user)
                if user:
                    flash('您已注册过，请登录！', 'warning')
                    return '<script> alert("您已注册过，请登录！"); window.location.href="/"; </script>'
                cur.execute("INSERT INTO userdatabase (username, password,email) VALUES (%s, %s, %s)",
                            (username, set_password(password), email))
                # mysql.connection.commit()
                mysql.commit()
                cur.close()
                flash('注册成功！请登录', 'success')
                print("注册成功")
                return redirect(url_for('auth.login'))
            else:
                return '<script> alert("验证码错误");window.location.href="/register";</script>'
        else:
            return '<script> alert("您还没发送验证码");</script>'
    return render_template('register.html')


@auth_blueprint.route('/vcode')
def vcode():
    code, bstring = ImageCode().draw_verify_code()
    session['vcode'] = code.lower()

    print(session.get('vcode'))
    # 将图像数据转换为文件并发送给客户端
    return send_file(
        bstring,
        mimetype='image/png'
    )


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id  # 这里的 ID 应该是唯一标识用户的，通常是从数据库中获取的

    @staticmethod
    def get(user_id, USERS=None):
        # 在这里根据 user_id 获取用户数据，然后实例化 User 类
        # 如果找不到用户，返回 None
        # 从数据库中获取用户数据，可以是一个字典等
        if user_id:
            return User(user_id)

        return None

    def get_id(self):
        return str(self.id)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        entered_captcha = request.form['captcha']

        # 获取存储在会话中的验证码
        stored_captcha = session.get('vcode', '')
        if entered_captcha == "":
            flash('请输入验证码', 'danger')
            return redirect(url_for('auth.login'))

        print(stored_captcha, entered_captcha)
        # 验证验证码
        if entered_captcha == stored_captcha:
            # 继续用户身份验证逻辑
            cur = mysql.cursor()
            cur.execute("SELECT * FROM userdatabase WHERE username = %s", [username])
            user_data = cur.fetchone()
            cur.close()
            if user_data and check_password(password, user_data['password']):
                user_id = user_data['id']
                user = User(user_id)
                login_user(user)
                print("zzzzz", user_id)
                if user_data['IsAdmin'] == 1:
                    return redirect(url_for('admin.ho'))
                else:
                    return redirect(url_for('tools.home'))
            else:
                flash('登录失败！请检查用户名和密码', 'danger')
                return redirect(url_for('auth.login'))  # 重定向回登录页面以显示错误消息
        else:
            flash('验证码错误！请重试', 'danger')
            return redirect(url_for('auth.login'))  # 重定向回登录页面以显示错误消息

    return render_template('login.html')


def allowed_file(filename):
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
        os.makedirs(current_app.config['UPLOAD_FOLDER'])
    # 允许上传的文件类型
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@auth_blueprint.route('/get_user')
@login_required
def get_user():
    user_id = current_user.get_id()
    cur = mysql.cursor()
    cur.execute("SELECT username,email,avatarUrl,nickname,IsAdmin FROM `userdatabase` WHERE id = %s", user_id)

    user_data = cur.fetchone()
    print("user_data", user_data)
    cur.close()
    if user_data:
        user_dict = {
            'username': user_data['username'],
            'email': user_data['email'],
            'avatarUrl': user_data['avatarUrl'],
            'nickname': user_data['nickname'],
            'IsAdmin': user_data['IsAdmin']
        }
        return jsonify(user_dict), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@auth_blueprint.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    # 获取请求中的表单字段
    print(request.files)
    username = request.form['username']
    email = request.form['email']
    nickname = request.form['nickname']
    user_id = int(current_user.get_id())  # 获取当前登录用户的ID
    file = request.files['avatar']
    print(file)
    try:
        cur = mysql.cursor()
        # 构建基本的 SQL UPDATE 语句
        sql = "UPDATE userdatabase SET "
        update_data = []  # 用于存储要更新的字段和值
        if nickname:
            sql += "nickname = %s, "
            update_data.append(nickname)
        if username:
            sql += "username = %s, "
            update_data.append(username)
        if email:
            sql += "email = %s, "
            update_data.append(email)

        if file and file.filename != '' and allowed_file(file.filename):
            user_id = int(current_user.id)
            filename = f"id_{user_id}.png"
            print(filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file_data = f"../static/uploads/" + filename
            cur = mysql.cursor()
            # 使用单个 SQL 查询同时更新昵称和邮箱
            cur.execute("UPDATE userdatabase SET avatarUrl = %s WHERE id = %s", (file_data, user_id))
            mysql.commit()
            cur.close()
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)
            return jsonify({'code': 0, 'message': '更新成功'})

        # 去掉最后一个逗号和空格
        if update_data:
            sql = sql[:-2]

        # 添加 WHERE 子句
        sql += " WHERE id = %s"

        # 添加用户ID到更新数据中
        print("id--", user_id)
        update_data.append(user_id)
        # 执行更新操作
        print("----11", update_data, tuple(update_data))
        cur.execute(sql, tuple(update_data))
        mysql.commit()
        cur.close()
    except Exception as e:
        mysql.rollback()
        print("错误---", e)
        return jsonify({'code': 2, 'message': '更新失败'})

    # 检查是否包含文件
    # if 'avatar' in request.files:
    #     file = request.files['avatar']
    #
    #     # 仅在包含文件并且文件不为空且文件类型有效时执行文件上传操作
    #

    # 返回成功响应，无论是否上传了文件
    return jsonify({'code': 0, 'message': '更新成功'})


@auth_blueprint.route('/change_password', methods=['POST'])
@login_required
def change_password():
    if request.method == 'POST':
        oldpassword = request.form['oldpassword']
        newpassword = request.form['newpassword']
        print(oldpassword, newpassword)
        # cur = mysql.connection.cursor()
        user_id = current_user.get_id()
        cur = mysql.cursor()
        cur.execute("SELECT password FROM userdatabase WHERE id = %s", user_id)
        get_oldpassword = cur.fetchone()

        if get_oldpassword and check_password(oldpassword, get_oldpassword['password']):
            cur.execute("UPDATE userdatabase SET password = %s WHERE id = %s", (set_password(newpassword), user_id))
            cur.fetchone()
            cur.close()
            return jsonify({'code': 0, 'message': 'yes'})
        else:
            return jsonify({'code': 0, 'message': 'no'})
    return jsonify({'code': 2, 'message': 'nonnnnnnn'})


class ImageCode:

    def rand_color(self):
        """生成用于绘制字符串的随机颜色(可以随意指定0-255之间的数字)"""
        red = random.randint(32, 200)
        green = random.randint(22, 255)
        blue = random.randint(0, 200)
        return red, green, blue

    def gen_text(self):
        """生成4位随机字符串"""
        # sample 用于从一个大的列表或字符串中，随机取得N个字符，来构建出一个子列表
        list = random.sample(string.ascii_letters, 5)
        return ''.join(list)

    def draw_lines(self, draw, num, width, height):
        """
        绘制干扰线
        :param draw: 图片对象
        :param num: 干扰线数量
        :param width: 图片的宽
        :param height: 图片的高
        :return:
        """
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=2)

    def draw_verify_code(self):
        """绘制验证码图片"""
        code = self.gen_text()
        width, height = 120, 50  # 设定图片大小，可根据实际需求调整
        im = Image.new('RGB', (width, height), 'white')  # 创建图片对象，并设定背景色为白色
        font_relative_path = 'font/Arial.ttf'  # 字体文件的相对路径
        font_path = os.path.join(current_app.config['STATIC_FOLDER'], font_relative_path)
        font = ImageFont.truetype(font=font_path, size=40)

        draw = ImageDraw.Draw(im)  # 新建ImageDraw对象
        # 绘制字符串
        for i in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)), text=code[i],
                      fill=self.rand_color(), font=font)
            self.draw_lines(draw, 2, width, height)  # 绘制干扰线
        # im.show()  # 如需临时调试，可以直接将生成的图片显示出来

        bstring = BytesIO()
        im.save(bstring, 'PNG')
        bstring.seek(0)
        return code[:4], bstring
