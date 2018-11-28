import requests
import json
import time
from lxml import etree
from threading import Thread
from queue import Queue



def spider(url):
    print(url)
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

    thread_spiders = []
    for i in range(10):
        url = base_url + str(i * 25)
        thread_spider = Thread(target=spider,args=[url])
        thread_spiders.append(thread_spider)
        thread_spider.start()

    for item in thread_spiders:
        item.join()

    end_time = time.time()

    while not movie_list.empty():
        print(movie_list.get())


    print('爬取时间总结：%s' % (end_time - start_time))
