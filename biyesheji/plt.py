import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pymysql
from biyesheji.route.auth import config

# 加载配置文件

mysql = pymysql.connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    password=config['mysql']['password'],
    db='mydatabase',
    cursorclass=pymysql.cursors.DictCursor  # 设置游标类以返回字典格式的结果
)
# plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']


def create_pic():
    plt.clf()
    # 提取国家信息并计数
    cur = mysql.cursor()
    cur.execute("SELECT * FROM moviedatabase")
    movies = cur.fetchall()
    print(movies)
    country_count = {}
    for movie in movies:
        countries = movie["country"].split("、")
        for country in countries:
            if country in country_count:
                country_count[country] += 1
            else:
                country_count[country] = 1
    cur.close()
    # 排序国家信息
    sorted_countries = sorted(country_count.items(), key=lambda x: x[1], reverse=True)
    top_countries = sorted_countries[:5]  # 取前五个国家

    # 提取国家名称和计数
    country_names = [country[0] for country in top_countries]
    country_counts = [country[1] for country in top_countries]

    # 创建柱状图
    plt.figure(figsize=(10, 6))
    plt.bar(country_names, country_counts, color='skyblue')
    plt.title('最多电影的五个国家')
    plt.xlabel('国家')
    plt.ylabel('电影数量')

    # 在柱状图上添加数值标签
    for i, count in enumerate(country_counts):
        plt.text(i, count, str(count), ha='center', va='bottom')

    # 将图表保存到内存中
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_data = base64.b64encode(img_buffer.read()).decode()
    return img_data


# def create_news_pic():
def create_news_pic():
    plt.clf()
    # 假设你的数据库查询有类似的结构
    cur = mysql.cursor()
    cur.execute("SELECT from_source FROM newdatabase")
    news = cur.fetchall()
    cur.close()
    # 统计歌手数量
    news_count = {}
    for new in news:
        temp = new['from_source']
        if temp in news_count:
            news_count[temp] += 1
        else:
            news_count[temp] = 1

    sorted_news = sorted(news_count.items(), key=lambda x: x[1], reverse=True)[:10]
    top_news = dict(sorted_news)

    # 创建柱状图
    singers = list(top_news.keys())
    song_counts = list(top_news.values())

    plt.bar(singers, song_counts, color='skyblue')
    plt.xlabel('单位')
    plt.ylabel('发布数量')
    plt.title('发布最多的前10个单位')
    plt.xticks(rotation=45, ha='right')  # 防止歌手名称重叠

    # 在柱状图上添加文本标签
    for i, count in enumerate(song_counts):
        plt.text(i, count, str(count), ha='center', va='bottom')

    # 将图表保存到 BytesIO 对象中
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_data = base64.b64encode(img_buffer.read()).decode()

    # 返回图像数据
    return img_data

def create_music_pic():
    plt.clf()
    # 假设你的数据库查询有类似的结构
    cur = mysql.cursor()
    cur.execute("SELECT * FROM musicdatabase")
    songs = cur.fetchall()
    cur.close()
    # 统计歌手数量
    singer_count = {}
    for song in songs:
        singer = song['singer']
        if singer in singer_count:
            singer_count[singer] += 1
        else:
            singer_count[singer] = 1

    # 取歌曲数量最多的前 10 个歌手
    sorted_singers = sorted(singer_count.items(), key=lambda x: x[1], reverse=True)[:10]
    top_singers = dict(sorted_singers)

    # 创建柱状图
    singers = list(top_singers.keys())
    song_counts = list(top_singers.values())

    plt.bar(singers, song_counts, color='skyblue')
    plt.xlabel('歌手')
    plt.ylabel('歌曲数量')
    plt.title('歌曲数量最多的前10个歌手')
    plt.xticks(rotation=45, ha='right')  # 防止歌手名称重叠

    # 在柱状图上添加文本标签
    for i, count in enumerate(song_counts):
        plt.text(i, count, str(count), ha='center', va='bottom')

    # 将图表保存到 BytesIO 对象中
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_data = base64.b64encode(img_buffer.read()).decode()

    # 返回图像数据
    return img_data
