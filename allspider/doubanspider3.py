# 用来操作数据库的类
import re
from redis import *


class RedisCommand(object):
    # #  类的初始化
    def __init__(self):
        self.client = StrictRedis(host='192.168.12.188', port=6379, db=0)

    def insert_one_doc(self):
        # 插入数据
        i = 1
        while i < 11:
            with open('../爬豆瓣250/movie_%s.html' % i, 'r', encoding="utf-8") as file:

                content = file.read()

            lis = re.findall(r'<li>.*?<div class="pic">.*?</div>.*?</li>', content, re.S)

            for li in lis:
                movie = {}
                movie["movie_name"] = re.search(r'<span class="title">(.*?)</span>', li).group(1)
                movie["movie_url"] = re.search(r'<a href="(.+?)" class="">', li).group(1)
                try:
                    movie["movie_instro"] = re.search(r'<span class="inq">([\u4e00-\u9fa5]*?.*?)</span>', li).group(1)

                except Exception as ex:
                    movie["movie_instro"] = re.search(r'<span class="inq">([\u4e00-\u9fa5]*?.*?)</span>', li)
                    print(ex)
                movie["movie_score"] = re.search(r'<span class="rating_num" property="v:average">(.*?)</span>',
                                                 li).group(1)

                a = str(movie)
                with open("./250.txt", 'a', encoding="utf-8") as file:
                    file.write(a + '\n')

                try:
                    self.client.set("movie", a)
                    print("插入成功")

                except Exception as e:

                    print(e)
                    print("插入失败")

            i += 1


if __name__ == "__main__":
    try:
        # 实例化类
        redis = RedisCommand()
        # 插入数据
        result = redis.insert_one_doc()

    except Exception as ex:

        print(ex)
