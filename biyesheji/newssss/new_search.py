import configparser
import pymysql

from biyesheji.route.auth import config


# from ..mysqls import mysql_user, mysql_host, mysql_pwd


class search_new:
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

    def search_new_by_keyword(self):
        sql = "SELECT * FROM newdatabase WHERE title LIKE %s OR content LIKE %s"
        keyword = f"%{self.keyword}%"  # 在关键字前后添加 % 通配符，以实现模糊匹配
        self.cursor.execute(sql, (keyword, keyword))
        result = self.cursor.fetchall()
        print(result)
        return result
