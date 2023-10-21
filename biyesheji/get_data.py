import pymysql
import json

from datetime import datetime

from biyesheji.route.auth import config


class NewsDatabaseManager:
    def __init__(self, config_path='config.ini'):
        self.config = config

    class DateTimeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            return super().default(obj)

    def get_data(self, page, page_size):
        connection = pymysql.connect(
            host='121.196.205.18',
            user='mydatabase',
            password='111119',
            db='mydatabase',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        cursor = connection.cursor()

        # Number of items per page
        offset = (page - 1) * page_size

        query = f"SELECT id, title, content, urls, news_time, from_source FROM newdatabase LIMIT {page_size} OFFSET {offset}"
        query_count = "SELECT COUNT(*) as count FROM newdatabase"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.execute(query_count)
        data_size = cursor.fetchone()
        cursor.close()
        connection.close()

        return data, data_size

    def get_json_data(self, page, page_size):
        data, data_size = self.get_data(page, page_size)
        json_data = json.dumps({"code": 0, "data": data, "count": data_size['count']}, ensure_ascii=False, indent=4,
                               cls=self.DateTimeEncoder)
        return json_data


class MusicDatabaseManager:
    def __init__(self, config_path='config.ini'):
        self.config = config


    class DateTimeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            return super().default(obj)

    def get_data(self, page, page_size):
        connection = pymysql.connect(
            host='121.196.205.18',
            user='mydatabase',
            password='111119',
            db='mydatabase',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        cursor = connection.cursor()

        # Number of items per page
        offset = (page - 1) * page_size

        query = f"SELECT id, music_name, music_id, singer, Album_Name, Album_pic,mp3_url FROM musicdatabase LIMIT {page_size} OFFSET {offset}"
        query_count = "SELECT COUNT(*) as count FROM musicdatabase"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.execute(query_count)
        data_size = cursor.fetchone()
        cursor.close()
        connection.close()

        return data, data_size

    def get_json_data(self, page, page_size):
        data, data_size = self.get_data(page, page_size)
        json_data = json.dumps({"code": 0, "data": data, "count": data_size['count']}, ensure_ascii=False, indent=4,
                               cls=self.DateTimeEncoder)
        return json_data


class MovieDatabaseManager:
    def __init__(self, config_path='config.ini'):
        self.config = config

    class DateTimeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            return super().default(obj)

    def get_data(self, page, page_size):
        connection = pymysql.connect(
            host='121.196.205.18',
            user='mydatabase',
            password='111119',
            db='mydatabase',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        cursor = connection.cursor()

        # Number of items per page
        offset = (page - 1) * page_size

        query = f"SELECT id, title, rating, country, address FROM moviedatabase LIMIT {page_size} OFFSET {offset}"
        query_count = "SELECT COUNT(*) as count FROM moviedatabase"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.execute(query_count)
        data_size = cursor.fetchone()
        cursor.close()
        connection.close()

        return data, data_size

    def get_json_data(self, page, page_size):
        data, data_size = self.get_data(page, page_size)
        json_data = json.dumps({"code": 0, "data": data, "count": data_size['count']}, ensure_ascii=False, indent=4,
                               cls=self.DateTimeEncoder)
        return json_data

# if __name__ == '__main__':
#     db_manager = DatabaseManager()
#     page_number = 1  # Replace this with the desired page number
#     json_data = db_manager.get_json_data(page_number)
#     print(json_data)
