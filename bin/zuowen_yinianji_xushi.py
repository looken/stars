#! /usr/bin/python
#coding=utf-8

import requests
import re

import sys
reload(sys)
sys.setdefaultencoding('gb2312')

import send_data

grade = {
    'yinianji': ['xushi', 'xiejing', 'shuxin', 'riji', 'xieren', 'xiangxiang', 'kantuxiehua'],
    'ernianji': ['xushi', 'xiejing', 'shuxin', 'riji', 'duhougan', 'xieren', 'xiangxiang'],
    'sannianji': ['xushi', 'xiejing', 'shuxin', 'riji', 'duhougan', 'xieren', 'xiangxiang', 'zhuangwu'],
    'sinianji': ['xushi', 'xiejing', 'shuxin', 'riji', 'duhougan', 'xieren', 'xiangxiang'],
    'wunianji': ['xushi', 'xiejing', 'shuxin', 'riji', 'duhougan', 'xieren', 'xiangxiang', 'huati'],
    'liunianji': ['xushi', 'xiejing', 'shuxin', 'riji', 'duhougan', 'xieren', 'xiangxiang', 'shige'],
    'chuyi': ['xushi', 'xiejing', 'shuomingwen', 'shuxin', 'riji', 'yilunwen', 'duhougan', 'xieren', 'xiangxiang', 'zhuangwu'],
    'chuer': ['xushi', 'xiejing', 'shuomingwen', 'shuxin', 'riji', 'yilunwen', 'duhougan', 'xieren', 'xiangxiang', 'zhuangwu', 'shige'],
    'chusan': ['xushi', 'xiejing', 'shuomingwen', 'shuxin', 'riji', 'yilunwen', 'duhougan', 'xieren', 'xiangxiang', 'zhuangwu', 'shige'],
    'gaoyi': ['xushi', 'xiejing', 'shuomingwen', 'shuxin', 'riji', 'yilunwen', 'duhougan', 'xieren', 'xiangxiang', 'zhuangwu'],
    'gaoer': ['xushi', 'xiejing', 'shuomingwen', 'shuxin', 'riji', 'yilunwen', 'duhougan', 'xieren', 'xiangxiang', 'zhuangwu', 'shige', 'huati'],
    'gaosan': ['xushi', 'xiejing', 'shuomingwen', 'shuxin', 'riji', 'yilunwen', 'duhougan', 'xieren', 'xiangxiang', 'zhuangwu', 'shige', 'huati']
}


m = {
    'gaozhong': '高中',
    'xiaoxue': '小学',
    'chuzhong': '初中',

    'zhuangwu': '状物',
    'xushi': '叙事',
    'xiejing': '写景',
    'shuxin': '书信',
    'riji': '日记',
    'xieren': '写人',
    'xiangxiang': '想象',
    'kantuxiehua': '看图写话',
    'duhougan': '读后感',
    'huati': '话题',
    'shige': '诗歌',
    'shuomingwen': '说明文',
    'yilunwen': '议论文',

    'yinianji': '一年级',
    'ernianji': '二年级',
    'sannianji': '三年级',
    'sinianji': '四年级',
    'wunianji': '五年级',
    'liunianji': '六年级',
    'chuyi': '初一',
    'chuer': '初二',
    'chusan': '初三',
    'gaoyi': '高一',
    'gaoer': '高二',
    'gaosan': '高三'
}

qq = {
    'yinianji': 'xiaoxue',
    'ernianji': 'xiaoxue',
    'sannianji': 'xiaoxue',
    'sinianji': 'xiaoxue',
    'wunianji': 'xiaoxue',
    'liunianji': 'xiaoxue',
    'chuyi': 'chuzhong',
    'chuer': 'chuzhong',
    'chusan': 'chuzhong',
    'gaoyi': 'gaozhong',
    'gaoer': 'gaozhong',
    'gaosan': 'gaozhong'
}

for a in grade.keys():
    for b in grade[a]:
        base_url = 'https://www.zuowen3.com/%s/%s/%s/' % (qq[a], a, b)

        url = base_url
        ret = requests.get(url)
        ret.encoding = "utf-8"

        p = base_url.split('/')[-4:-1]
        for i in xrange(len(p)):
            print(p[i])
            p[i] = m[p[i]]

        print(p)

        res = ret.text.split('<ul><li><span>')
        res = res[1:-1]

        for item in res:
            item = re.findall("newDate\">(.*)</em></span> <a href=\"(.*)\" target=\"_blank\"  title=\"(.*)\">.*</a></li></ul>", item)

            newurl = 'https://www.zuowen3.com%s' % (item[0][1])
            ret = requests.get(newurl)
            ret.encoding = "utf-8"

            result = []
            result.append(ret.text.split('<div class="newstitle">')[1].split('<body oncopy = "noCopy()">')[0])

            if not result:
                print(ret.text)

            send_data.send('\n'.join(result), 'learn/' + '/'.join(p), item[0][2].replace('<b>', '').replace('</b>', '') + '.txt')
