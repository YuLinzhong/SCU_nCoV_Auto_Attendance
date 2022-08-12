# -*- coding: utf-8 -*-
import datetime
import getpass
import os
import time

import json
import re
import requests
import urllib3
import argparse
from apscheduler.schedulers.blocking import BlockingScheduler
from halo import Halo

sfzxDict={'1':'是','0':'否'}
bzxyyDict={'境外交流学习':'境外交流学习','实习':'实习','回家':'回家','出差':'出差','生病住院':'生病住院','其他事假':'其他事假'}
szxqmcDict={'华西校区':'华西校区','江安校区':'江安校区','望江校区':'望江校区'}
zgfxdqDict={'1':'是','0':'否'}
bztcyyDict={'2':'探亲','3':'旅游','4':'回家','5':'出差','1':'其他'}
twDict={'1':'35℃以下','2':'35℃-36.5℃','3':'36.6℃-36.9℃','4':'37℃-37.3℃','5':'37.4℃-38℃','6':'38.1℃-38.5℃','7':'38.6℃-39℃','8':'39.1℃-40℃','9':'40.1℃以上'}
sfcxtzDict={'1':'是','0':'否'}
sfyyjcDict={'1':'是','0':'否'}
jcjgqrDict={'1':'疑似感染','2':'确诊感染','3':'其他'}
sfjcbhDict={'1':'是','0':'否'}
jcbhlxDict={'疑似':'疑似','确诊':'确诊'}
mjryDict={'1':'是','0':'否'}
csmjryDict={'1':'是','0':'否'}
sfcyglqDict={'1':'是','0':'否'}
gllxDict={'学校家属院':'学校家属院','学校集中隔离点':'学校集中隔离点','成都校外居住地':'成都校外居住地','蓉外地区集中隔离点':'蓉外地区集中隔离点'}
sfjzxgymDict={'1':'是','0':'否'}
sfjzdezxgymDict={'1':'是','0':'否'}
sfjzdszxgymDict={'1':'是','0':'否'}
sfcxzysxDict={'1':'是','0':'否'}

class DaKa(object):
    def __init__(self, username, password, eai_sess, UUkey):
        self.username = username
        self.password = password
        self.login_url = "https://ua.scu.edu.cn/login"
        self.redirect_url = "https://ua.scu.edu.cn/login?service=https%3A%2F%2Fwfw.scu.edu.cn%2Fa_scu%2Fapi%2Fsso%2Fcas-index%3Fredirect%3Dhttps%253A%252F%252Fwfw.scu.edu.cn%252Fncov%252Fwap%252Fdefault%252Findex"
        self.base_url = "https://wfw.scu.edu.cn/ncov/wap/default/index"
        self.save_url = "https://wfw.scu.edu.cn/ncov/wap/default/save"
        self.eai_sess = eai_sess
        self.UUkey = UUkey
        self.cookie1 = None
        self.cookie2 = None
        self.header = None
        self.info = None
        self.sess = requests.Session()

    def login(self):
        """Login to CSU platform"""
        res1 = self.sess.get(self.login_url)
        self.cookie1 = res1.headers['Set-Cookie'].split(";")[0]
        # header1 = {'Cookie': self.cookie1}
        # data = {
        #     "userName": self.username,
        #     "passWord": self.password,
        #     "enter": 'true',
        # }
        # res2 = self.sess.post(url=self.login_url, headers=header1, data=data, allow_redirects=False)
        # self.cookie2 = res2.headers['Set-Cookie'].split(";")[0]
        self.header = {
            'Cookie': "eai-sess=" + self.eai_sess + ";" + "UUkey=" + self.UUkey + ";" + self.cookie1}
        return self.sess

    def get_info(self, html=None):
        """Get hitcard info, which is the old info with updated new time."""
        if not html:
            urllib3.disable_warnings()
            res = self.sess.get(self.base_url, headers=self.header, verify=False)
            html = res.content.decode()

        jsontext = re.findall(r'def = {[\s\S]*?};', html)[0]
        jsontext = eval(jsontext[jsontext.find("{"):jsontext.rfind(";")].replace(" ", ""))

        geo_text = jsontext['geo_api_info']
        geo_text = geo_text.replace("false", "False").replace("true", "True")
        geo_obj = eval(geo_text)['addressComponent']
        area = geo_obj['province'] + " " + geo_obj['city'] + " " + geo_obj['district']
        name = re.findall(r'realname: "([^\"]+)",', html)[0]
        number = re.findall(r"number: '([^\']+)',", html)[0]

        new_info = jsontext.copy()
        new_info['name'] = name
        new_info['number'] = number
        new_info['area'] = area
        new_info["date"] = self.get_date()
        new_info["created"] = round(time.time())
        self.info = new_info
        return new_info

    def get_date(self):
        today = datetime.date.today()
        return "%4d%02d%02d" % (today.year, today.month, today.day)

    def post(self):
        """Post the hitcard info"""
        print(self.info)
        res = self.sess.post(self.save_url, data=self.info, headers=self.header)
        return json.loads(res.text)


def main(username, password, eai_sess, UUkey):
    print("\n[Time] %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("🚌 打卡任务启动")
    spinner = Halo(text='Loading', spinner='dots')
    spinner.start('正在新建打卡实例...')
    dk = DaKa(username, password, eai_sess, UUkey)
    spinner.succeed('已新建打卡实例')

    spinner.start(text='登录到中南大学信息门户...')
    dk.login()
    spinner.succeed('已登录到中南大学信息门户')

    spinner.start(text='正在获取个人信息...')
    dk.get_info()
    spinner.succeed('%s %s同学, 你好~' % (dk.info['number'], dk.info['name']))

    spinner.start(text='正在为您打卡打卡打卡')
    res = dk.post()
    if str(res['e']) == '0':
        spinner.stop_and_persist(symbol='🦄 '.encode('utf-8'), text='已为您打卡成功！')
    else:
        spinner.stop_and_persist(symbol='🦄 '.encode('utf-8'), text=res['m'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--username', type=str, default=None)
    parser.add_argument('--password', type=str, default=None)
    parser.add_argument('--eai-sess', type=str, default=None)
    parser.add_argument('--UUkey', type=str, default=None)
    args = parser.parse_args()
    print("用户信息：", args)
    main(args.username, args.password, args.eai_sess, args.UUkey)
