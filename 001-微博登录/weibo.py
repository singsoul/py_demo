import requests
import json
import random
import time
from pyquery import PyQuery as jq
import pandas as pd
from selenium import webdriver as wb


datacol = {0:'id',1:'头像',2:'名字',3:'微博内容',4:'发布时间'}

class wb_demo():
    def __init__(self):
        self.session = requests.Session()
        self.list = []
        self.auth = ["18395996541", "asdfg159"]
        self.login_url = "https://passport.weibo.cn/signin/login"

    def update_cookie_chrome(self, headless=None):
        options = wb.ChromeOptions()
        if headless:
            options.add_argument('headless')
        self.driver = wb.Chrome(chrome_options=options)
        self.driver.set_page_load_timeout(30)
        self.driver.get(self.login_url)
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id("loginName").send_keys(self.auth[0])
        self.driver.find_element_by_id("loginPassword").send_keys(self.auth[1])
        loginbtn = self.driver.find_element_by_id("loginAction")
        loginbtn.click()
        while True:
            time.sleep(7)
            if "verifycode_box" in self.driver.page_source:
                input("waiting for checkcode>>>")
                # loginbtn.click()
            else:
                break
        self.driver.implicitly_wait(30)
        self.driver.implicitly_wait(30)
        self.session.cookies.update(
            {i["name"]: i["value"] for i in self.driver.get_cookies()})

#获取关注总数
    def getGuanzhuList(self,uid):
        url = f"https://weibo.cn/{uid}/follow?page=1"
        resp = self.session.get(url)
        bbb = jq(resp.content)('.tc').text()
        max_num = bbb.split('[')[1].split(']')[0]
        print('关注数：' + str(max_num))
        for i in range(1,int(max_num) //10 + 2):
            print("正在获取第{}页的关注列表:".format(i))
            self.getGuanzhu(uid,i)
            t = random.randint(1,8)
            print("休眠时间为:{}s".format(t))
            time.sleep(t)
    def getGuanzhu(self,containerid,page):
        url = f"https://weibo.cn/{containerid}/follow?page={page}"
        resp = self.session.get(url)
        for aa in jq(resp.content)('table').items():
            url = aa('tr > td:nth-child(1) > a').attr('href')
            ids = ""
            for bb in url.split('/'):
                ids = bb
            img = aa('tr > td:nth-child(1) > a > img').attr('src')

            name = aa('tr > td:nth-child(2) > a:nth-child(1)').text()
            lists = [ids,img,name]
            self.list.append(lists)
            self.getContentList(ids)

#获取总数
    def getContentList(self,uid):
        resp = self.session.get(f'https://weibo.cn/{uid}?filter=0&page=0')
        # bbb = jq(resp.content)('.pa > form > div').html()
        max_num = jq(resp.content)('[name=mp]').attr('value')
        if int(max_num) > 5:
            max_num = 5
        print('总页数：' + str(max_num))
        for i in range(1,max_num):
            self.getContent(i,uid)
            t = random.randint(1,6)
            print("休眠时间为:{}s".format(t))
            time.sleep(t)
        
    def getContent(self,page,uid):
        resp = self.session.get(f'https://weibo.cn/{uid}?filter=0&page={page}')
        for aa in jq(resp.content)('.c').items():
            content = aa('.ctt').text()
            time = aa('.ct').text()
            if content != "":
                lists = ['','','',content,time]
                self.list.append(lists)




if __name__ == '__main__':
    wbs = wb_demo()
    wbs.update_cookie_chrome()
    wbs.getGuanzhuList('5404506563')

    df = pd.DataFrame(wbs.list)
    df.rename(columns=datacol,inplace=True)
    df.to_excel('weibo.xlsx')