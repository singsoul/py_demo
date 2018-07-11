import os
import random
import requests
import logging
import ctypes
from data import *
from string import Template
from markupsafe import escape
from PIL import Image
from http import cookiejar


logging.basicConfig(format=Webot_logger_format, level=logging.INFO)


def ABpath(_path):
    return os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), _path))


def tmp(word, dicts, safe=True, clear=False):
    """模板填充"""
    dicts = {k: escape(v) if safe else v for k, v in dicts.items()}
    words = Template(word).safesubstitute(dicts).split('$[')
    pkgsql = (
        words[0] + ''.join([x.replace(x.split("]")[0], '')[1:] for x in words]))
    if clear:
        pkgsql = pkgsql.replace("''", "NULL")
    return pkgsql


def Dict_update(dicts, adds):
    """字典更新"""
    dicts.update(adds)
    return dicts


def image_array(path):
    img_raw = []
    img_pixdata = [" ", "="]
    img = Image.open(path)
    width, height = img.size
    # img.thumbnail((width // 1.5, height // 1.5))
    img.convert("L")
    for wi, w in enumerate(range(width)):
        img_raw.append([])
        for h in range(height):
            img_raw.append(img_pixdata[0] if img.getpixel(
                (w, h)) == 0 else img_pixdata[1])
    return img_raw


class Anticrawler(object):
    """反防护爬虫Session"""

    def __init__(self, session=None, proxy=None, source=None, cookies={}):
        super(Anticrawler, self).__init__()
        self.session = self.default_session(session, proxy, source, cookies)
        self.logger = logging.getLogger(type(self).__name__)

    def default_session(self, session, proxy, source, cookies):
        if session:
            return session
        else:
            s = requests.Session()
            s.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
                "Upgrade-Insecure-Requests": "1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Referer": source,
                "Accept-Encoding": "gzip, deflate, sdch",
                "Accept-Language": "zh-CN,zh;q=0.8"
            }
            s.timeout = 5
            s.allowredirects = False
            s.proxies = proxy
            s.cookies = requests.utils.cookiejar_from_dict(
                Dict_update({}, cookies))
            return s

    def updatecookie(self, dict_data):
        self.session.cookies = requests.utils.add_dict_to_cookiejar(
            self.session.cookies, dict_data)

    def random_user_agent(self):
        """随机UA"""
        UserAgentList = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; InfoPath.2; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; 360SE)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
            "Mozilla/5.0 (X11; U; Linux i686; rv:1.7.3) Gecko/20040913 Firefox/0.10",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; ja) Presto/2.10.289 Version/12.00",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36"
        ]
        self.session.headers.update(
            {"User-Agent": random.choice(UserAgentList)})
