from functools import wraps

import jwt
import datetime

import redis
from flask import request, jsonify, app, redirect, url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash

# 示例数据，通常需要根据实际情况调整

secret_key = "like666"  # 密钥，需要保密
redis_client = redis.Redis(host='8.134.56.160', port=6379, db=0, password=123456)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # 从请求的 headers 中获取 JWT
        id = current_user.get_id()
        print(id)

        token = redis_client.get(id)
        print(token)
        if not token:
            return redirect(url_for('auth.login'))

        try:
            # 解码 JWT
            jwt.decode(token, secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return redirect(url_for('auth.login'))
        except jwt.InvalidTokenError as a:
            return redirect(url_for('auth.login'))

        # 检查 Redis 中是否存在该 token，如果不存在，说明已经过期或无效

        # 将解码后的信息传递给被装饰的路由
        return f(*args, **kwargs)

    return decorated


def creat_token(user_id, user_name):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        "user_id": user_id,
        "user_name": user_name,
        "exp": expiration_time
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def check(token1):
    try:
        decoded_payload = jwt.decode(token1, secret_key, algorithms=["HS256"])
        print("Token is valid")
        print(decoded_payload)
    except jwt.ExpiredSignatureError:
        print("Token 过期")
    except jwt.DecodeError:
        print("Token 无效")


def set_password(password):
    '''
    :param password: 带加密的密码，如123456
    :return: 加密的密码：pbkdf2:sha256:150000$0koyI6Eb$cff6e1b193381f5891fc1cf7b87b1b4dab33869aa5490a7f935579e47c7666cf
    '''
    password = generate_password_hash(password)
    return password


def check_password(password, pwhash):
    '''
    :param password: 字符串密码，如123456
    :param pwhash: 加密后的密码，存在用户表中的hash值
    :return: Ture or False
    '''
    return check_password_hash(password=password, pwhash=pwhash)
