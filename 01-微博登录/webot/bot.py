# encoding=utf8

from extra import *
from data import *
from PIL import Image
from pyquery import PyQuery as jq
from json import dumps

from io import BytesIO
import re
import time
import logging
import threading
import pickle
import requests
import execjs
import chardet
from retry import retry

logging.basicConfig(format=Webot_logger_format, level=logging.INFO)


class Webot(object):
    """docstring for Webot"""

    def __init__(self, hotreload=False):
        super(Webot, self).__init__()
        self.hotreload = hotreload
        self.logger = logging.getLogger(type(self).__name__)
        self.crawler = Anticrawler(source=API_target, cookies={
            "MM_WX_NOTIFY_STATE": "1",
            "MM_WX_SOUND_STATE": "1",
            "mm_lang": "zh_CN",
            "login_frequency": "1"
        })
        self.session = self.crawler.session
        self.appid = "wx782c26e4c19acffb"
        self.thread_pool = {}
        self.QR_code_uuid = None
        self.QR_code_check_times = 0
        self.get_ticket_url = None
        self.auth_data = None
        self.person_data = None

    def set_mail_worker(self, usr, pwd, host):
        """
            邮件客户端
        """
        self.mail_client = yagmail.SMTP(
            user=usr, password=pwd, host=host)

    def resp_check(self, resp, extracode=None):
        """
            响应检查
        """
        netcode = resp.status_code
        if netcode == 200 and resp.content:
            return True

    def error_exit(self, e):
        """
            打印错误并退出
        """
        self.logger.error(e)
        exit()

    def data_report(self, data, format_word=None):
        """
            打印结果并返回
        """
        format_word = format_word if format_word else "{}"
        self.logger.info(format_word.format(data))
        return data

    def save_worker(self, data, filename="res.pkl"):
        """
            会话保存
        """
        with open(filename, "wb") as f:
            pickle.dump((data), f)

    def load_worker(self, filename="res.pkl"):
        """
            会话还原
        """
        with open(filename, "rb") as f:
            return pickle.load(f)

    def raw_data_save(self, data, filename="res.json"):
        """
            部分源数据存取
        """
        with open(filename, "w", encoding="utf8") as f:
            f.write(dumps(data, indent=4, ensure_ascii=False))
            # self.logger.info("Rawdata File Saved")

##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################

    def create_deviceid(self):
        """
            创建随机设备指纹
        """
        self.deviceid = f"e{str(random)[2:17]}"
        return self.deviceid

    def create_clientmsgid(self):
        """
            创建客户端信息指纹
        """
        self.cilentmsgid = int(time.time() * 1E3) + random.randint(1, 1000)
        return self.cilentmsgid

    def get_timestamp(self, reverse=False):
        """
            获取时间戳,支持取反
        """
        if not reverse:
            return int(time.time() * 1E3)
        else:
            return execjs.eval("~new Date")

    def get_BaseRequest(self):
        """
            生成基础payload
        """
        return {"BaseRequest": {
            "Uin": self.auth_data['wxuin'],
            "Sid": self.auth_data['wxsid'],
            "Skey": self.auth_data['skey'],
            "DeviceID": self.create_deviceid()
        }}

    def get_lang(self):
        """
            获取语言
        """
        return self.session.cookies.get("mm_lang")

    def word_decode(word):
        """
            微信数据解码
        """
        return word.encode(self.encoding).decode("utf8")

##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################

    def create_synckey(self):
        """
            组合生成synckey
        """
        synckey = "|".join(
            [f"{item['Key']}_{item['Val']}" for item in self.person_data['SyncKey']['List']])
        # self.logger.info(f"Synkey:[{synckey}]")
        return synckey

    def get_qrcode_uid(self):
        """
            获取二维码ID
        """
        try:
            resp = self.session.get(API_jsLogin)
            if self.resp_check(resp):
                self.QR_code_uuid = re.split(r'"|";', resp.text)[1]
                self.logger.warning(
                    f"Current Data's Encoding [{resp.encoding}]")
                self.encoding = resp.encoding
                self.logger.info(f"GET QRCODE_UUID --> [{self.QR_code_uuid}]")
        except Exception as e:
            self.error_exit(e)

    def get_qrcode_img(self):
        """
            获取二维码
        """
        try:
            resp = self.session.get(f"{API_qrcode}{self.QR_code_uuid}")
            if self.resp_check(resp):
                self.API_qrcode_buffer = BytesIO(resp.content)
        except Exception as e:
            self.error_exit(e)

    def print_qrcode(self):
        """
            打印二维码
        """
        def open():
            img = Image.open(self.API_qrcode_buffer)
            img.show()
        self.thread_pool['thread_openimg'] = threading.Thread(target=open)
        self.thread_pool['thread_openimg'].start()

    def login_wait(self, local=None):
        """
            登录过程
        """
        try:
            resp = self.session.get(API_login, params={
                "loginicon": "true",
                "uuid": self.QR_code_uuid,
                "tip": 1 if local else 0,
                "r": self.get_timestamp(True),
                "_": self.get_timestamp()
            }, timeout=API_checktimeout)
            if self.resp_check(resp):
                return resp
        except Exception as e:
            self.login_wait(local)

    def login_push_wait(self):
        """
            热启动
        """
        try:
            self.crawler.updatecookie({"login_frequency": "2"})
            resp = self.session.get(API_webwxpushloginurl, params={
                "uin": self.session.cookies.get("wxuin")
            })
            if self.resp_check(resp):
                self.QR_code_uuid = resp.json()["uuid"]
                self.logger.info(f"New UUID: [{self.QR_code_uuid}]")
                return True
        except Exception as e:
            self.logger.error(e)

    def login_localwait(self):
        """
            等待本地终端扫描
        """
        self.logger.info("Waiting for app scan")
        self.login_wait(True)
        # stop self.thread_pool["thread_openimg"]

    def login_appwait(self, get_ticket=True):
        """
            等待本地终端确认
        """
        self.logger.info("Waiting for app confirm")
        resp = self.login_wait(False)
        if self.resp_check(resp):
            if get_ticket:
                self.logger.info("Login Success")
                self.get_ticket_url = re.split(r'redirect_uri="|";', resp.text)[
                    1] + "&fun=new&version=v2"

    def get_ticket(self):
        """
            获取个人信息票据并更新部分cookie
        """
        try:
            self.logger.info(f"Redirect to --> {self.get_ticket_url}")
            resp = self.session.get(self.get_ticket_url, params={
                "fun": "new",
                "lang": "zh_CN",
                "_": self.get_timestamp()
            })
            if self.resp_check(resp):
                self.logger.info(
                    f"Get Ticket: { requests.utils.dict_from_cookiejar(resp.cookies)}")
                htmldata = jq(resp.text)
                self.auth_data = {key: htmldata(key).text() for key in [
                    "skey", "wxsid", "wxuin", "pass_ticket", "isgrayscale"]}
                self.crawler.updatecookie(
                    {"last_wxuin": self.auth_data["wxuin"]})
                if self.auth_data:
                    return True
        except Exception as e:
            exit(e)

    def login_success_init(self):
        """
            成功登陆并初始化wx
        """
        try:
            resp = self.session.post(API_webwxinit, params={
                "pass_ticket": self.auth_data['pass_ticket'],
                "lang": "zh_CN"
            }, json=self.get_BaseRequest())
            resp.encoding = "utf8"
            if self.resp_check(resp):
                self.person_data = resp.json()
                self.logger.info(
                    f"***Welcome***: [{self.person_data['User']['NickName']}]")
                self.save_worker((self.session, self.auth_data,
                                  self.person_data, self.get_ticket_url), API_hotreload_file)
        except Exception as e:
            self.logger.error(e)

    def get_msgid(self):
        """
            获取消息身份id
        """
        try:
            jsondata = self.get_BaseRequest()
            jsondata.update({
                "Code": 3,
                "FromUserName": self.person_data["User"]["UserName"],
                "ToUserName": self.person_data["User"]["UserName"],
                "ClientMsgId": self.create_clientmsgid()
            })
            resp = self.session.post(API_webwxstatusnotify, params={
                "lang": "zh_CN",
                "pass_ticket": self.auth_data["pass_ticket"]
            }, json=jsondata)
            if self.resp_check(resp):
                self.MsgID = resp.json()["MsgID"]
        except Exception as e:
            self.logger.error(e)

    @retry()
    def get_msg_signal(self):
        """
            消息信号检查
        """
        try:
            resp = self.session.get(API_synccheck, params={
                "r": self.get_timestamp(),
                "skey": self.auth_data['skey'],
                "sid": self.auth_data['wxsid'],
                "uin": self.auth_data['wxuin'],
                "deviceid": self.create_deviceid,
                "synckey": self.create_synckey(),
                "_": self.get_timestamp()
            }, timeout=API_checktimeout)
            if self.resp_check(resp):
                # self.logger.info(resp.text)
                return True
        except Exception as e:
            self.logger.error(e)
            raise
        finally:
            time.sleep(2)

    def get_msg_contents(self):
        """
            获取消息详情
        """
        try:
            jsondata = self.get_BaseRequest()
            jsondata.update({"rr": execjs.eval("~new Date"),
                             "SyncKey": self.person_data['SyncKey']
                             })
            resp = self.session.post(API_webwxsync, params={
                "lang": "zh_CN",
                "sid": self.auth_data['wxsid'],
                "skey": self.auth_data['skey'],
                "pass_ticket": self.auth_data["pass_ticket"]
            }, json=jsondata)
            resp.encoding = "utf8"
            if self.resp_check(resp):
                res = resp.json()
                self.person_data['SyncKey'] = res["SyncKey"]
                return res
        except Exception as e:
            self.error_exit(e)

    def get_contact(self):
        """获取联系人"""
        try:
            resp = self.session.get(API_webwxgetcontact, params={
                "lang": "zh_CN",
                "pass_ticket": self.auth_data["pass_ticket"],
                "r": self.get_timestamp(),
                "seq": 0,
                "skey": self.auth_data["skey"]})
            resp.encoding = "utf8"
            if self.resp_check(resp):
                self.contacts = resp.json()
                self.logger.info(
                    f"Get friends: [{self.contacts['MemberCount']}]")

        except Exception as e:
            self.error_exit(e)


##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################

    def send_msg(self, target, msg):
        """
            消息发送
        """
        try:
            jsondata = self.get_BaseRequest()
            jsondata.update({"Msg": {
                "Type": 1,
                "Content": msg,
                "FromUserName": self.person_data["User"]["UserName"],
                "ToUserName": target,
                "LocalID": self.create_clientmsgid(),
                "ClientMsgId": self.MsgID
            },
                "Scene": 0})
            resp = self.session.get(API_webwxsendmsg, params={
                "lang": "zh_CN",
                "pass_ticket": self.auth_data["pass_ticket"]
            })
            if self.resp_check(resp):
                print(f">>>{resp.json()}")
        except Exception as e:
            self.logger.error(e)

    def search_friend(self, strs):
        """
            好友搜索
        """
        for index, value in enumerate(self.contacts["MemberList"]):
            if strs in value["NickName"]:
                print(
                    f"{value['NickName'].ljust(4)}{value['UserName'].rjust(10)}")

##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################

    def start(self):
        """
            启动webot
        """
        self.create_deviceid()
        self.get_auth_data()
        while not self.get_ticket():
            self.hotreload = False
            self.get_auth_data()
        self.login_success_init()
        self.get_msgid()
        self.get_contact()
        self.msg_worker()
        self.interaction()
        return self

    def get_auth_data(self):
        """
            获取认证数据
        """
        if self.hotreload and os.path.exists(API_hotreload_file):
            with open(API_hotreload_file, "rb") as f:
                try:
                    self.session, self.auth_data, self.person_data, self.get_ticket_url = pickle.load(
                        f)
                    self.crawler.session = self.session
                except Exception as e:
                    self.logger.error(e)
            self.login_push_wait()
            self.login_appwait(False)
        else:
            self.get_qrcode_uid()
            self.get_qrcode_img()
            self.print_qrcode()
            self.login_localwait()
        self.login_appwait()

    def interaction(self):
        """
            交互式面板
        """
        while True:
            try:
                cmd = input(">>>")
                if not cmd:
                    pass
                else:
                    print(eval(cmd))
            except Exception as e:
                self.logger.error(e)
            finally:
                time.sleep(0.1)

    def msg_worker(self):
        """
            消息处理
        """
        def worker():
            while True:
                if self.get_msg_signal():
                    msg = self.get_msg_contents()
                    self.data_ctrl(msg)
                    self.raw_data_save(msg)
        self.thread_pool['msg_hook'] = threading.Thread(target=worker)
        self.thread_pool['msg_hook'].start()

    def data_ctrl(self, msg):
        pass
