import pymysql
from biyesheji.route.auth import config


class search_music:
    def __init__(self):
        conn = pymysql.connect(
            host=config['mysql']['host'],
            user=config['mysql']['user'],
            password=config['mysql']['password'],
            db='mydatabase',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = conn.cursor()

    def search_music_by_keyword(self, keyword):
        sql = "SELECT * FROM musicdatabase WHERE music_name LIKE %s OR singer LIKE %s OR Album_Name LIKE %s"
        keyword = f"%{keyword}%"  # 在关键字前后添加 % 通配符，以实现模糊匹配
        print(keyword)
        self.cursor.execute(sql, (keyword, keyword))
        result = self.cursor.fetchall()
        print(result)
        return result
