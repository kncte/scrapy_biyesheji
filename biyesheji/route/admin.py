from datetime import datetime

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from biyesheji.route.auth import mysql

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/admin_route')
# @login_required  # 保证只有登录用户可以注销
def ho():
    return render_template('admin.html')


@admin_blueprint.route('/admin_work')
@login_required  # 保证只有登录用户可以注销
def work():
    return render_template('admin_work.html')


@admin_blueprint.route('/admin_data')
@login_required  # 保证只有登录用户可以注销
def data():
    return render_template('admin_data.html')


@admin_blueprint.route('/admin_getmsg')
@login_required
def admin_getmsg():
    try:
        user_id = current_user.id
        cur = mysql.cursor()
        cur.execute("SELECT * FROM complaintdatabase")
        message_data = cur.fetchall()

        cur.close()
        table_data = []

        for message in message_data:
            table_data.append({
                'id': message['id'],
                'content': message['content'],
                'user_id': message['user_id'],
                'submit_time': message['submit_time'],
                'is_handle': int(message['is_handle']),
                'handle_time': message['handle_time'],
                'return_content': message['return_content']
            })

        print("zzzzzzzz", table_data)
        return {'code': 0, 'msg': 'success', 'count': len(table_data), 'data': table_data}

    except Exception as e:
        print("Error in admin_getmsg:", str(e))
        return {'code': 1, 'msg': 'error'}


@admin_blueprint.route('/admin_message')
@login_required
def message__():
    try:
        admin_getmsg_data = admin_getmsg()
        return render_template('admin_message.html', d=admin_getmsg_data)
    except Exception as e:
        print("Error in message__:", str(e))
        # 处理错误，返回一个错误页面或者其他适当的响应
        return render_template('1.html', error_message='An error occurred.')


@admin_blueprint.route('/handle_message', methods=['POST'])
def handle_message():
    data = request.get_json()
    message_id = data.get('id')
    return_content = data.get('return_content')
    #
    # for message in messages:
    #     if message['id'] == message_id:
    #         message['is_handle'] = 1
    #         message['handle_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         message['return_content'] = return_content
    #         break

    return jsonify({'status': 'success'})


@admin_blueprint.route('/reply_message', methods=['POST'])
@login_required  # 保证只有登录用户可以注销
def reply_message():
    message_id = request.form.get('id')
    reply_content = request.form.get('reply_content')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur = mysql.cursor()
    cur.execute("UPDATE complaintdatabase SET return_content = %s, handle_time = %s ,is_handle = %s WHERE id = %s",
                (reply_content, time, 1, message_id))
    # 使用你的 ORM 或数据库 API 更新数据库中的回复内容
    cur.close()
    mysql.commit()

    # 返回一个响应（你可能想返回一个带有成功状态的 JSON 响应）
    return jsonify({'success': True})
