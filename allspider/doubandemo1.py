
import requests

# 模拟浏览器   爬取豆瓣250
class DoubanSpider:
    def __init__(self):
        # 初始化
        self.num = 0
        self.i = 0
        self.url = 'https://movie.douban.com/top250?start=%s&filter='

        self.headers = {
            "Cookie": "bid=n6gVHWTvRtU; ap_v=0,6.0; __utma=30149280.1193045255.1541235808.1541235808.1541235808.1; __utmb=30149280.0.10.1541235808; __utmc=30149280; __utmz=30149280.1541235808.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=223695111.1738858886.1541235808.1541235808.1541235808.1; __utmb=223695111.0.10.1541235808; __utmc=223695111; __utmz=223695111.1541235808.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1541235810%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D1ZYb28SaNegVWkwEwmMNOo_ggp8jl1LkKqYxboVl_30cTXX_W63ZUKamPfuAzquM%26wd%3D%26eqid%3Dcce89c410001f2a8000000045bdd645c%22%5D; _pk_ses.100001.4cf6=*; __yadk_uid=XSfIqcj0K8yUGDIg5vkJK0HovWgrXnmM; _pk_id.100001.4cf6=5e87b0187a791c73.1541235810.1.1541238424.1541235810.",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        }
        # 代理ip  过期了的话需要更换
        self.proxies = {
            "https": "https://103.102.144.145:43406",
        }

    def run(self):
        # 请求数据
        html = requests.get(url=self.url % self.num, headers=self.headers, proxies=self.proxies)
        self.num += 25
        print('self.num', self.num)
        content = html.content

        return content

    def writeHtml(self):
        # 保存静态网页
        self.i += 1
        with open("movie_%s.html" % self.i, "wb") as file:
            content = self.run()
            file.write(content)


if __name__ == '__main__':
    # 实例化类
    douban = DoubanSpider()
    k = 0
    while k < 10:
        douban.writeHtml()
        print('k', k)
        k += 1

