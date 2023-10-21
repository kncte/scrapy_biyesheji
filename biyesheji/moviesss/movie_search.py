import configparser
import pymysql

from biyesheji.route.auth import config


# from ..mysqls import mysql_user, mysql_host, mysql_pwd



class search_movie:
    def __init__(self, keyword):
        conn = pymysql.connect(
            host=config['mysql']['host'],
            user=config['mysql']['user'],
            password=config['mysql']['password'],
            db='mydatabase',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = conn.cursor()
        self.keyword = keyword

    def search_movies_by_keyword(self):

        sql = "SELECT * FROM moviedatabase WHERE title LIKE %s OR country LIKE %s"
        keyword = f"%{self.keyword}%"  # 在关键字前后添加 % 通配符，以实现模糊匹配
        self.cursor.execute(sql, (keyword,keyword))
        result = self.cursor.fetchall()
        print(result)
        return result
