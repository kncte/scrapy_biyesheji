import json
import os
import signal
import subprocess
from datetime import datetime
import redis
from flask import Blueprint, render_template, session, send_file, jsonify, request, current_app
from flask_login import login_required, current_user

from biyesheji.authentication import set_password
from biyesheji.plt import create_pic, create_music_pic
from biyesheji.route.auth import mysql, allowed_file, ImageCode
# from biyesheji.tools.yzm import ImageCode
from concurrent.futures import ThreadPoolExecutor
import psutil

from scrapy import cmdline

toolssssss = Blueprint('tools', __name__)

redis_client = redis.Redis(host='121.196.205.18', port=6379, db=0, password=123456)


@toolssssss.route('/del_route', methods=['DELETE'])
@login_required
def delete_route():
    try:
        with mysql.cursor() as cur:
            cur.execute('TRUNCATE TABLE CrawlTasks')
        mysql.connection.commit()
        return "success", 204  # 返回 204 No Content 表示成功但没有内容返回
    except Exception as e:
        print(f"Error in delete_route: {str(e)}")
        return f"Error: {str(e)}", 500


@toolssssss.route('/stop_task', methods=['POST'])
@login_required

def stop_task():
    redis_client.set('state', 'True')
    return jsonify({'status': 'success'})


@toolssssss.route('/do', methods=['POST'])
@login_required

def submit():
    COMMANDS = {
        '音乐': 'scrapy crawl music',
        '电影': 'scrapy crawl movie',
        '新闻': 'scrapy crawl news',
    }
    redis_client.set('state', 'False')
    data = request.get_json()
    thread_count = int(data['thread_count'])
    task_type = data['task_type']
    keyword = data['keyword']
    print("keyword", keyword)

    # 记录任务开始时间
    start_time = datetime.now()
    if task_type == '音乐':
        if redis_client.exists('music_data_list'):
            redis_client.delete('music_data_list')
    if task_type == '电影':
        if redis_client.exists('movie_data_list'):
            redis_client.delete('movie_data_list')
    if task_type == '新闻':
        if redis_client.exists('new_data_list'):
            redis_client.delete('new_data_list')
    cur = mysql.cursor()
    sql = "INSERT INTO CrawlTasks (type,gjz, start_time, IsTrue) VALUES (%s, %s, %s, %s)"
    cur.execute(sql, (task_type, keyword, start_time.strftime("%H:%M:%S"), 0))  # 设置 IsTrue 为 0，表示任务未完成
    cur.close()
    mysql.commit()

    # 获取任务对应的命令
    command = COMMANDS.get(task_type)
    work_data = command + " -a key=" + keyword
    print("data_aaaaa", work_data)
    if command:
        def crawl_spider():
            try:
                result = subprocess.run(work_data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                               encoding='utf-8')
                # cmdline.execute(work_data.split())
                print("aaaaaaaaaaaaaaa",result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"Error running Scrapy process: {e}")

        futures = []
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            for _ in range(thread_count):
                try:
                    future = executor.submit(crawl_spider)
                    futures.append(future)
                except Exception as e:
                    print(f"Error submitting task to ThreadPoolExecutor: {e}")

        if redis_client.get('state') == b'True':
            for future in futures:
                future.cancel()

        for future in futures:
            future.result()
        # 记录任务结束时间
        end_time = datetime.now()

        # 更新数据库，设置 end_time，计算时间差，设置 IsTrue 为 1
        cur = mysql.cursor()
        sql = "UPDATE CrawlTasks SET end_time = %s, Time = %s, IsTrue = %s WHERE gjz = %s AND start_time = %s"
        time_diff = end_time - start_time
        cur.execute(sql, (end_time.strftime("%H:%M:%S"), time_diff, 1, keyword, start_time.strftime("%H:%M:%S")))
        cur.close()
        mysql.commit()

        redis_client.set('state', 'True')
        return "任务已经完成"
    else:
        return "无效的任务类型"


# 路由处理函数，用于返回 crawl 任务数据
@toolssssss.route('/get_crawl_tasks', methods=['GET'])
@login_required

def get_crawl_tasks():
    cur = mysql.cursor()

    try:
        # 执行查询 SQL
        sql = "SELECT * FROM CrawlTasks"
        cur.execute(sql)
        result = cur.fetchall()
    finally:
        cur.close()
    return jsonify(result)


@toolssssss.route('/update_profile', methods=['POST'])
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

    return jsonify({'code': 0, 'message': '更新成功'})


@toolssssss.route('/home')
@login_required
def home():
    return render_template('home.html')


@toolssssss.route('/first')
@login_required

def first():
    # print(redis_client.get("aaaa"))
    return render_template('first.html')
    # return render_template('first.html')


@toolssssss.route('/working')
@login_required

def working():
    # print(redis_client.get("aaaa"))

    return render_template('working.html')
    # return render_template('first.html')


# 第二个视图
@toolssssss.route('/work')
@login_required

def work():
    # return render_template('second.html')
    return render_template('second.html')


@toolssssss.route('/change_view', methods=['GET', 'POST'])
@login_required

def change_view():
    if request.method == 'POST':
        content_type = request.form.get('content_type')
        if content_type == 'music':
            pic = create_music_pic()
        else:
            pic = create_pic()
        return render_template('third.html', img_data=pic)
    else:
        return render_template('third.html', img_data=None)


# 第三个视图
@toolssssss.route('/view')
@login_required

def view():
    img_data = create_pic()
    return render_template('third.html', img_data="")


# 管理员
@toolssssss.route('/admin')
@login_required

def admin_login():
    return render_template('admin.html')


@toolssssss.route('/set_message')

@login_required
def set_message():
    print(current_user.id)
    return render_template('message.html')


@toolssssss.route('/submit_message', methods=['POST'])
@login_required
def submit_message():
    user_id = current_user.id
    content = request.get_json().get('message')
    print("aaaaa", content)
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if user_id and content:
        cur = mysql.cursor()
        sql = "INSERT INTO complaintdatabase ( user_id, content, is_handle,submit_time) VALUES ( %s, %s, %s, %s)"
        cur.execute(sql, (user_id, content, 0, now_time))
        cur.close()
        mysql.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': '提交失败'})


@toolssssss.route('/get_message')
@login_required
def get_message():
    user_id = current_user.id
    cur = mysql.cursor()
    cur.execute("SELECT * FROM complaintdatabase WHERE user_id = %s", user_id)
    message_data = cur.fetchall()
    print("zzzzzzzz", message_data)
    cur.close()

    return jsonify(message_data), 200


@toolssssss.route('/validate_user', methods=['POST'])
@login_required
def validate_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    cur = mysql.cursor()
    cur.execute("SELECT username, email FROM userdatabase WHERE username = %s", (username,))
    user_data = cur.fetchone()

    print("zzzz", user_data)
    if user_data is None:
        cur.close()
        return jsonify({'valid': False, 'message': '没有此用户'})

    # 验证用户名和邮箱是否匹配
    if user_data['username'] == username and user_data['email'] == email:
        cur.close()
        return jsonify({'valid': True})
    else:
        cur.close()
        return jsonify({'valid': False, 'message': '用户名和邮箱不匹配'})


@toolssssss.route('/vcode')
def vcode():
    code, bstring = ImageCode().draw_verify_code()
    session['vcode'] = code.lower()

    print(session.get('vcode'))
    # 将图像数据转换为文件并发送给客户端
    return send_file(
        bstring,
        mimetype='image/png'
    )



@toolssssss.route('/change_pwd', methods=['POST'])
@login_required

def change_pwd():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    new_password = data.get('new_password')
    code = data.get('code')
    print(username, email)
    cur = mysql.cursor()
    cur.execute("SELECT username, email FROM userdatabase WHERE username = %s", (username,))
    user_data = cur.fetchone()
    print("****", user_data)
    if redis_client.get(email).decode('utf-8') == code:

        if username == user_data['username'] and user_data['email'] == email:
            # 更新密码
            cur.execute("UPDATE userdatabase SET password = %s WHERE email = %s", (set_password(new_password), email))
            cur.close()
            mysql.commit()
            return jsonify({'success': True, 'message': '密码已重置'})
        else:
            cur.close()
            return jsonify({'success': False, 'message': '用户名和邮箱不匹配'})
    else:
        return jsonify({'success': False, 'message': '验证码错误'})


@toolssssss.route('/forget_pwd')

def forget_pwd():
    return render_template('forget_pwd.html')


@toolssssss.route('/get_data')
@login_required

def get_data111():
    # 从消息队列中获取数据
    task_type = request.args.get('type')
    data_list = ""

    if task_type == "音乐":
        data_list = redis_client.lrange('music_data_list', 0, -1)
    elif task_type == "电影":
        data_list = redis_client.lrange('movie_data_list', 0, -1)
    elif task_type == "新闻":
        data_list = redis_client.lrange('new_data_list', 0, -1)

    if not data_list:
        return jsonify({'data': "", 'state': 'False'})

    data = [json.loads(data) for data in data_list]

    state = redis_client.get('state')
    state = state.decode('utf-8').lower()
    print(state)
    if state:
        return jsonify({'data': data, 'state': 'True'})
    else:
        return jsonify({'data': data, 'state': 'False'})


@toolssssss.route('/del_data', methods=['POST'])
@login_required
def del_data():
    data_id = request.form['data_id']
    type = request.form['type']
    print("-----------------------------", data_id)
    cur = mysql.cursor()

    if type == 'movie':
        print("11111")
        # 删除记录
        cur.execute("DELETE FROM moviedatabase WHERE id = %s", data_id)
        # 重新配置自增字段的值
        cur.execute("SET @auto_id = 0;")
        cur.execute("UPDATE moviedatabase SET id = ( @auto_id := @auto_id + 1 );")
        cur.execute("ALTER TABLE moviedatabase AUTO_INCREMENT = 1;")

    elif type == 'music':
        print("22222")
        # 删除记录
        cur.execute("DELETE FROM musicdatabase WHERE id = %s", data_id)
        # 重新配置自增字段的值
        cur.execute("SET @auto_id = 0;")
        cur.execute("UPDATE musicdatabase SET id = ( @auto_id := @auto_id + 1 );")
        cur.execute("ALTER TABLE musicdatabase AUTO_INCREMENT = 1;")

    elif type == 'new':
        print("33333")
        # 删除记录
        cur.execute("DELETE FROM newdatabase WHERE id = %s", data_id)
        # 重新配置自增字段的值
        cur.execute("SET @auto_id = 0;")
        cur.execute("UPDATE newdatabase SET id = ( @auto_id := @auto_id + 1 );")
        cur.execute("ALTER TABLE newdatabase AUTO_INCREMENT = 1;")

    cur.close()

    # 提交数据库更改
    mysql.commit()

    return jsonify({'code': 0, 'message': 'success'}), 200
