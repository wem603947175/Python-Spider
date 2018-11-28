import requests
import json
import time
from lxml import etree
from threading import Thread
from queue import Queue
from gevent import  monkey
import gevent
import random

# gevent 让我们可以按同步的方式来写异步程序
# monkey.patch_all() 会在Python程序执行时动态的将网络库（socket,select,thread)
# 替换掉，变成异步的库，让我们的程序可以异步的方式处理网络相关的任务
monkey.patch_all()

def spider(url):
    response = requests.get(url=url)
    content = response.content
    content = content.decode('utf-8')

    '''数据处理'''
    html = etree.HTML(content)
    item_list = html.xpath('//div[@class="item"]')
    for item in item_list:
        movie = {}
        movie['编号'] = item.xpath('./div[1]/em/text()')[0]
        print(movie['编号'])
        movie['名称'] = item.xpath('./div[2]//a/span[1]/text()')[0]
        movie['评分'] = item.xpath('./div[2]//span[@class="rating_num"]/text()')[0]

        movie_list.put(movie)

if __name__ == '__main__':
    start_time = time.time()

    # 存储数据
    movie_list = Queue()

    '''发送请求'''
    base_url = 'https://movie.douban.com/top250?filter=&start='

    gevent_spiders = []
    for i in range(10):
        url = base_url + str(i * 25)
        print(url)
        gevent_spider = gevent.spawn(spider,url)
        gevent_spiders.append(gevent_spider)

    gevent.joinall(gevent_spiders)

    end_time = time.time()



    while not movie_list.empty():
        print(movie_list.get())

    print('爬取时间总结：%s' % (end_time - start_time))

