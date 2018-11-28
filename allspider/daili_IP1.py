mport requests
import re


class DailiIPSpider:
    """代理ip爬虫"""

    def __init__(self):
        self.url = 'http://31f.cn/https-proxy/'

        self.headers = {

            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "Hm_lvt_c04918a39ff11e02096f3cd664c5ada6=1541074275; Hm_lpvt_c04918a39ff11e02096f3cd664c5ada6=1541075906",
            "Host": "31f.cn",
            "Pragma": "no-cache",
            "Referer": "http://31f.cn/https-proxy/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",

        }

        self.proxies = {"https": "https://202.101.13.68:8080",
                        }

    # 解析url, 获取响应内容
    def parse_url(self):
        ret = requests.get(url=self.url, headers=self.headers, proxies=self.proxies)

        content = ret.content

        with open(" 爬ip.html", "wb") as  file:
            file.write(content)
        # print(content)
        return content

    # 删选数据
    def get_data(self, content):

        pattern = re.compile(r'<td>[\d+\.+]*</td>', re.S)
        item_list = pattern.findall(r'%s' % content)

        def write_ip(num):
            with open('高匿ip.txt', 'a') as file:
                file.write(num)

        def sub_ip(i):
            des = re.sub(r'<td>(.*)</td>', r"\1", i)
            # print('{\n' + des + '\n}')
            return des

        j = 0
        for i in item_list:
            j += 1
            if j % 3 == 2:
                i = sub_ip(i)
                print('"https":"https://' + i + ':', end='')
                write_ip(i + ":")
            elif j % 3 == 0:
                i = sub_ip(i)
                print(i + '",', end='')
                write_ip(i)
            else:
                print()
                write_ip('\r\n')


if __name__ == '__main__':
    daili = DailiIPSpider()

    content = daili.parse_url()

    daili.get_data(content)

