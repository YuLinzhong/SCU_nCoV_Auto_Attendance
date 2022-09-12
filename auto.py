# -*- coding: utf-8 -*-
import datetime
import getpass
import os
import time
import random 
import json
import re
import requests
import urllib3
import argparse
from apscheduler.schedulers.blocking import BlockingScheduler
from halo import Halo



time.sleep(random.randint(1, 10)*60) 


primary={'zgfxdq':'今日是否在中高风险地区？',
        'mjry':'今日是否接触密接人员？',
        'csmjry':'近14日内本人/共同居住者是否去过疫情发生场所（市场、单位、小区等）或与场所人员有过密切接触？',
        'szxqmc':'所在校区',
        'sfjzxgym':'是否接种过新冠疫苗？',
        'jzxgymrq':'……接种第一剂新冠疫苗时间',
        'sfjzdezxgym':'是否接种第二剂新冠疫苗？',
        'jzdezxgymrq':'……接种第二剂新冠疫苗时间',
        'sfjzdszxgym':'是否接种第三剂新冠疫苗？',
        'jzdszxgymrq':'……接种第三剂新冠疫苗时间',
        'tw':'今日体温范围',
        'sfcxtz':'今日是否出现发热、乏力、干咳、呼吸困难等症状？',
        'sfjcbh':'今日是否接触无症状感染/疑似/确诊人群？',
        'sfcxzysx':'是否有任何与疫情相关的， 值得注意的情况？',
        'qksm':'……情况说明',
        'sfyyjc':'是否到相关医院或门诊检查？',
        'jcjgqr':'检查结果属于以下哪种情况',
        'remark':'其他信息',
        'address':'🌏api:详细地址',
        'geo_api_info':'🌏api:原始数据',
        'area':'🌏api:简单地址',
        'province':'🌏api:省份',
        'city':'🌏api:城市',
        'sfzx':'今日是否在校？',
        'sfcyglq':'是否处于观察期？',
        'gllx':'观察场所',
        'glksrq':'隔离开始日期',
        'jcbhlx':'接触人群类型',
        'jcbhrq':'……接触时间',
        'bztcyy':'当前地点与上次不在同一城市，原因如下',
        'szcs':'所在城市',
        'bzxyy':'不在校原因：',
        'jcjg':'检查结果属于以下哪种情况',
        'fxyy':'返校原因'}






secondary=dict(
                sfzx={'1':'是','0':'否'},
                bzxyy={'境外交流学习':'境外交流学习','实习':'实习','回家':'回家','出差':'出差','生病住院':'生病住院','其他事假':'其他事假'},
                szxqmc={'华西校区':'华西校区','江安校区':'江安校区','望江校区':'望江校区'},
                zgfxdq={'1':'是','0':'否'},
                bztcyy={'2':'探亲','3':'旅游','4':'回家','5':'出差','1':'其他'},
                tw={'1':'35℃以下','2':'35℃-36.5℃','3':'36.6℃-36.9℃','4':'37℃-37.3℃','5':'37.4℃-38℃','6':'38.1℃-38.5℃','7':'38.6℃-39℃','8':'39.1℃-40℃','9':'40.1℃以上'},
                sfcxtz={'1':'是','0':'否'},
                sfyyjc={'1':'是','0':'否'},
                jcjgqr={'0':'无需检查','1':'疑似感染','2':'确诊感染','3':'其他'},
                sfjcbh={'1':'是','0':'否'},
                jcbhlx={'疑似':'疑似','确诊':'确诊'},
                mjry={'1':'是','0':'否'},
                csmjry={'1':'是','0':'否'},
                sfcyglq={'1':'是','0':'否'},
                gllx={'学校家属院':'学校家属院','学校集中隔离点':'学校集中隔离点','成都校外居住地':'成都校外居住地','蓉外地区集中隔离点':'蓉外地区集中隔离点'},
                sfjzxgym={'1':'是','0':'否'},
                sfjzdezxgym={'1':'是','0':'否'},
                sfjzdszxgym={'1':'是','0':'否'},
                sfcxzysx={'1':'是','0':'否'})

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
        # feedback before posting, for last-minute verifying
        for currentKey in self.info:
            if self.info[currentKey] != '' and currentKey in primary:
                if currentKey in secondary:
                    print(primary[currentKey]+'：'+secondary[currentKey][self.info[currentKey]])
                elif currentKey=='geo_api_info':
                    print(primary[currentKey]+'：'+json.dumps(json.loads(self.info[currentKey].replace('true','"True"')),ensure_ascii=False,sort_keys=True, indent=6, separators=(',', ': ')))#不加ensure_ascii=False输出的会是‘中国’ 中的ascii字符码，而不是真正的中文。这是因为json.dumps序列化时对中文默认使用的ascii编码想输出真正的中文需要指定ensure_ascii=False：
                else:
                    print(primary[currentKey]+'：'+self.info[currentKey])

        # Post the hitcard info
        res = self.sess.post(self.save_url, data=self.info, headers=self.header)
        return json.loads(res.text)


def main(username, password, eai_sess, UUkey):
    print("\n[Time] %s" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("🚌 打卡任务启动")
    spinner = Halo(text='Loading', spinner='dots')
    spinner.start('正在新建打卡实例...')
    dk = DaKa(username, password, eai_sess, UUkey)
    spinner.succeed('已新建打卡实例')

    spinner.start(text='登录到四川大学信息门户...')
    dk.login()
    spinner.succeed('已登录到四川大学信息门户')

    spinner.start(text='正在获取个人信息...')
    dk.get_info()
    spinner.succeed('%s %s同学, 你好~' % (dk.info['number'], dk.info['name']))

    spinner.start(text='正在为您打卡打卡打卡')
    res = dk.post()
    if str(res['e']) == '0':
        spinner.stop_and_persist(symbol='🦄 '.encode('utf-8'), text='已为您打卡成功！')
    else:
        spinner.stop_and_persist(symbol='🦄 '.encode('utf-8'), text=res['m'])
        raise RuntimeError(res['m'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--username', type=str, default=None)
    parser.add_argument('--password', type=str, default=None)
    parser.add_argument('--eai-sess', type=str, default=None)
    parser.add_argument('--UUkey', type=str, default=None)
    args = parser.parse_args()
    print("用户信息：", args)
    main(args.username, args.password, args.eai_sess, args.UUkey)
