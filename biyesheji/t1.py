from biyesheji.route.auth import redis_client


if __name__ == '__main__':
    redis_client.set('state', 'False')