import scrapy
import pymysql
import configparser
import logging

config = configparser.ConfigParser()
config.read('biyesheji/config.ini')

# 共享数据库连接
conn = pymysql.connect(
    host='8.134.56.160',
    user='mydatabase',
    password='111119',
    db='mydatabase',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


class BasePipeline:
    def __init__(self):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # Subclasses should override this method
        pass

    def close_spider(self, spider):
        self.conn.close()


class MoviePipeline(BasePipeline):
    def process_item(self, item, spider):
        sql = ("INSERT INTO moviedatabase (title, rating, country, address,type,duration) VALUES (%s, %s, %s, %s, %s, "
               "%s)")
        title = str(item['title'])
        rating = float(item['rating']) if item['rating'] else None

        values = (title, rating, item['country'], item['address'], item['type'], item['duration'])
        print("啊啊啊啊啊啊啊啊啊啊-----------", values)

        select_sql = "SELECT title FROM moviedatabase WHERE title = %s"
        self.cursor.execute(select_sql, (title,))
        result = self.cursor.fetchone()

        if not result:
            try:
                self.cursor.execute(sql, values)
                self.conn.commit()
                print("成功插入数据：", values)
            except Exception as e:
                print("插入数据时出现异常：", str(e))
                self.conn.rollback()  # 回滚事务
        else:
            print("数据已存在：", title)
        return item


class MusicPipeline(BasePipeline):
    def process_item(self, item, spider):
        sql = "INSERT INTO musicdatabase (music_name, music_id, singer,Album_Name,Album_pic,mp3_url) VALUES (%s,%s, %s,%s,%s,%s)"
        name = str(item['name'])
        music_id = str(item['music_id'])
        singer = str(item['singer'])
        Album_Name = str(item['Album_Name'])
        Album_pic = str(item['Album_pic'])
        mp3_url = str(item['mp3_url'])
        values = (name, music_id, singer, Album_Name, Album_pic, mp3_url)
        print("啊啊啊啊啊啊啊啊啊啊-----------", values)
        select_sql = "SELECT music_name FROM musicdatabase WHERE music_name = %s"
        self.cursor.execute(select_sql, name)
        result = self.cursor.fetchone()
        if not result:
            try:
                self.cursor.execute(sql, values)
                self.conn.commit()
                print("成功插入数据：", values)
            except Exception as e:
                print("插入数据时出现异常：", str(e))
                self.conn.rollback()  # 回滚事务
        else:
            print("数据已存在：", name)
        return item


class NewPipeline(BasePipeline):
    def process_item(self, item, spider):
        sql = "INSERT INTO newdatabase (title, content, urls,news_time,from_source) VALUES (%s, %s,%s,%s,%s)"
        title = str(item['title'])
        content = str(item['content'])
        urls = str(item['urls'])
        news_time = str(item['time'])
        from_source = str(item['new_from'])
        values = (title, content, urls, news_time, from_source)
        print("啊啊啊啊啊啊啊啊啊啊-----------", values)
        select_sql = "SELECT urls FROM newdatabase WHERE urls = %s"
        self.cursor.execute(select_sql, urls)
        result = self.cursor.fetchone()
        if not result:
            try:
                self.cursor.execute(sql, values)
                self.conn.commit()
                print("成功插入数据：", values)
            except Exception as e:
                print("插入数据时出现异常：", str(e))
                self.conn.rollback()  # 回滚事务
        else:
            print("数据已存在：", urls)
        return item
