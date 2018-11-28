from yundama import discern
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
import time

class Douban:

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument("--proxy-server=https://202.101.13.68:8080")
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)

    def simulate_login(self):
        # 模拟登录豆瓣
        self.driver.get("https://www.douban.com/")
        # 模拟输入账号密码
        self.driver.find_element_by_name("form_email").send_keys("需要修改")
        self.driver.find_element_by_name("form_password").send_keys("需要修改")



    def get_valicode(self,Img_id,Input_id):
        # 模拟登录豆瓣
        valicode_url = self.driver.find_element_by_id(Img_id).get_attribute("src")
        # 获取图片url
        print("图片url",valicode_url)
        resp = requests.get(valicode_url)
        file_path = "./captcha.jpeg"
        print("file_path",file_path)

        with open(file_path,"wb")  as file:
            file.write(resp.content)

        # 调用云打码
        valicode = discern(filepath=file_path,codetype = 3000)

        print("valicode",valicode)
        # 输入验证码
        self.driver.find_element_by_id(Input_id).send_keys(valicode)
        
        time.sleep(3)

        
    def login(self,loginbtn_class_name):
        # 模拟点击登录
        self.driver.find_element_by_class_name(loginbtn_class_name).click()
        time.sleep(8)
        print("登录中。。。。")
        # self.driver.find_element_by_xpath('//*[@id="lzform"]/fieldset/div[4]/input').click()

        # 生成登陆后快照
        # driver.save_screenshot("douban.png")
        # print('driver.page_source',driver.page_source)
    def get_dource(self,filepath1):
        # 保存源码"./douban.html"
        with open(filepath1, "w",encoding="utf-8") as file:
            file.write(self.driver.page_source)

    def close(self):
        # 关闭
        time.sleep(3)
        self.driver.quit()

    def run(self):
        # 总的运行逻辑
        self.simulate_login()
        self.get_valicode("captcha_image", "captcha_field")
        self.get_dource("./douban1.html")

        self.login("bn-submit")

        if self.driver.current_url == "https://www.douban.com/accounts/login":
            self.get_valicode("captcha_image", "captcha_field")
            self.login("btn-submit")
        self.get_dource("./douban2.html")
        self.close()


if __name__ == '__main__':

    douban = Douban()
    douban.run()
