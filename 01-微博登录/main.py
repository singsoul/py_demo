# coding=utf-8

import itchat
import re
import moment
from itchat.content import TEXT
from pprint import pprint



NickNameList = [
    # "学院春晓11-3-602"
]

RuleList = [
    # "电话",
    r"\d{3}-+\d{6}"
]

def loginWechat():
    itchat.auto_login(hotReload=True)
    itchat.run(blockThread=True)

@itchat.msg_register([TEXT],isGroupChat=False)
def check_msg(msg):
    pprint(msg)
    if NickNameList and not msg['User']['NickName'] in NickNameList:
        return
    Phone = data_parser(msg)
    if Phone:
        data = {
            "phones":Phone,
            "content":msg['Content'],
            "group":msg['User']['NickName'],
            "name":msg['User']['Self']['NickName'],
            "date":moment.date(str(msg['CreateTime'])).format("YYYY-MM-DD hh:mm:ss")
        }
        pprint(data)


def data_parser(msg):
    for item in RuleList:
        return re.findall(item,msg['Content'])


loginWechat()