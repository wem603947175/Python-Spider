import requests
import re
import json
from lxml import etree


def f1():
    num = 1
    kw = input(">")
    url = "http://tieba.baidu.com/f?kw={}".format(kw)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }

    while True:
        print(url)

        resp = requests.get(url=url, headers=headers)
        content = resp.content.decode("utf-8")

        content = re.sub(r"<script>.*?</script>",r"",content,flags=re.DOTALL)

        # content = content.replace('id="pagelet_html_frs-list/pagelet/content" style="display:none;"><!--', 'id="pagelet_html_frs-list/pagelet/content" style="display:none;">')
        # content = content.replace('--></code><script>Bigpipe.register("frs-list/pagelet/thread_list", {', '</code><script>Bigpipe.register("frs-list/pagelet/thread_list", {')

        with open("./tieba_{}.html".format(num), "w", encoding="utf-8") as file:
            file.write(content)

        url = re.findall(r'<a href="(.*?)" class="next pagination-item " >下一页&gt;</a>', content)
        if url:
            url = "http:" + url[0]
        else:
            break

        num += 1

def f2():
    num = 1
    kw = input(">")
    url = "http://tieba.baidu.com/f?kw={}".format(kw)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }

    tiebas = []

    while True:
        print(url)

        resp = requests.get(url=url, headers=headers)
        html_content = resp.content.decode("utf-8")

        html_content = re.sub(r"<script>.*?</script>", r"", html_content, flags=re.DOTALL)

        html_content = re.sub(r"<!--", r"", html_content)
        html_content = re.sub(r"-->", r"", html_content)

        with open("./tieba_{}.html".format(num), "w", encoding="utf-8") as file:
            file.write(html_content)

        html = etree.HTML(html_content)
        j_th_tits = html.xpath('//a[@class="j_th_tit "]')
        for j_th_tit in j_th_tits:
            tieba = {}
            tieba["title"] = j_th_tit.xpath("./text()")[0]
            tieba["href"] = "https://tieba.baidu.com"+j_th_tit.xpath("./@href")[0]
            tiebas.append(tieba)

            resp2 = requests.get(url=tieba["href"], headers=headers)
            html_content2 = resp2.content.decode("utf-8")
            html2 = etree.HTML(html_content2)
            print(tieba)

            img_srcs = html2.xpath('//img[@class="BDE_Image"]/@src')
            print(img_srcs)

            # for img_src in img_srcs:
            #     resp = requests.get(url=img_src, headers=headers)
            #     img_content = resp.content
            #     with open("./images/{}".format(img_src[img_src.rfind("/")+1:] ),"wb") as file:
            #         file.write(img_content)


        url = re.findall(r'<a href="(.*?)" class="next pagination-item " >下一页&gt;</a>', html_content)
        if url:
            url = "http:" + url[0]
        else:
            break

        num += 1

        if  input("是否继续(yes/no)")=="no":
            break

    with open("./tieba.json","w",encoding="utf-8") as file:
        json.dump(tiebas,file,ensure_ascii=False,indent=4)

if __name__ == '__main__':
    # f1()
    f2()

