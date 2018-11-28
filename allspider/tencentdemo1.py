import requests
import re
import json
from lxml import etree
from 爬腾讯招聘.MysqlComment import MySQLCommand

mysqlcommand = MySQLCommand()
mysqlcommand.connectMysql()


class TencentSpider:
    def __init__(self):
        self.page_url = "https://hr.tencent.com/position.php?keywords=%E8%AF%B7%E8%BE%93%E5%85%A5%E5%85%B3%E9%94%AE%E8%AF%8D&lid=0&tid=0"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": "PHPSESSID=nb459u0p1kde088ql43s0bf6g0; pgv_pvi=7459600384; pgv_si=s6296429568",
            "Host": "hr.tencent.com",
            "Referer": "https://hr.tencent.com/position.php?keywords=%E8%AF%B7%E8%BE%93%E5%85%A5%E5%85%B3%E9%94%AE%E8%AF%8D",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        }
        self.recruitments = []
        self.proxies = {
            # "https": "https://223.99.197.253:63000",
            "https": "https://183.237.185.209:46049",

        }

    def parse_url(self, url):
        resp = requests.get(url=url, headers=self.headers, proxies=self.proxies)

        return resp.content.decode("utf-8")

    def get_xpath(self, html_content, xpath_str):
        html = etree.HTML(html_content)
        return html.xpath(xpath_str)

    def get_data(self, url):
        html_content = self.parse_url(url)
        uls = self.get_xpath(html_content, '//ul[@class="squareli"]')

        return "".join(uls[0].xpath(".//text()")), "".join(uls[1].xpath(".//text()"))

    def run(self):
        html_content = self.parse_url(self.page_url)

        trs = self.get_xpath(html_content, '//tr[@class="even"]|//tr[@class="odd"]')

        for tr in trs:
            recruitment = {}
            recruitment["name"] = tr.xpath("./td/a/text()")[0]
            recruitment["type"] = tr.xpath("./td[2]/text()")[0]
            recruitment["num"] = tr.xpath("./td[3]/text()")[0]
            recruitment["addr"] = tr.xpath("./td[4]/text()")[0]
            recruitment["time"] = tr.xpath("./td[5]/text()")[0]
            recruitment["respo"], recruitment["requir"] = self.get_data(
                "https://hr.tencent.com/" + tr.xpath("./td/a/@href")[0])
            mysqlcommand.insertData(recruitment)
            self.recruitments.append(recruitment)

    def save_date(self):
        with open("./tecent.json", "w", encoding="utf-8") as file:
            json.dump(self.recruitments, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    spider = TencentSpider()
    spider.run()
    spider.save_date()
    with open("./tecent.json", "r", encoding="utf-8") as file:
        json_list = json.load(file)

    print('1', json_list)
    # print(json_list[0])
    # print(json_list[0]["rtype"])
    print("***********")
    # for i in json_list:
    #     print(i)
    mysqlcommand.closeMysql()

