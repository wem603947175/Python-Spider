import re

# 用来操作mongodb数据库的类
import pymongo


class MongodbCommand(object):
    #  类的初始化
    def __init__(self):
        self.client = pymongo.MongoClient(host="192.168.12.188", port=27017)["1807a"]

    # 插入数据
    def insert_one_doc(self):
        # 选择集合
        coll = self.client['movies']
        i = 1
        while i < 11:
            with open('../爬豆瓣250/movie_%s.html' % i, 'r', encoding="utf-8") as file:

                content = file.read()

            lis = re.findall(r'<li>.*?<div class="pic">.*?</div>.*?</li>', content, re.S)

            for li in lis:
                movie = {}
                movie["movie_name"] = re.search(r'<span class="title">(.*?)</span>', li).group(1)
                # print('movie["movie_name"]', movie["movie_name"])

                movie["movie_url"] = re.search(r'<a href="(.+?)" class="">', li).group(1)
                # print('movie["url"]', movie["url"])
                try:
                    movie["movie_instro"] = re.search(r'<span class="inq">([\u4e00-\u9fa5]*?.*?)</span>', li).group(1)
                # print('movie["instro"]', movie["instro"])
                except Exception as ex:
                    movie["movie_instro"] = re.search(r'<span class="inq">([\u4e00-\u9fa5]*?.*?)</span>', li)

                    print(ex)

                movie["movie_score"] = re.search(r'<span class="rating_num" property="v:average">(.*?)</span>',
                                                 li).group(1)
                # print('movie["score"]', movie["score"])

                # 传过去 的是json 数去 去掉 【】 后 的  一个{   } 数据
                a = str(movie)
                with open("./250.txt", 'a', encoding="utf-8") as file:
                    file.write(a + '\n')

                # print(movie["movie_name"])
                # print(coll.find({'movie_name': movie["movie_name"]}))

                # 判断是否有重复的 
                if coll.find_one({'movie_name': movie["movie_name"]}) == None:
                    information_id = coll.insert(movie)
                    print("插入成功")
                else:
                    print("插入失败")
                print(movie)
            i += 1


if __name__ == '__main__':
    # 实例化类
    mongo = MongodbCommand()

    # 插入数据
    mongo.insert_one_doc()

