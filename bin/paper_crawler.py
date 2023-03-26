#! /usr/bin/python
#coding=utf-8

#导入BosClient配置文件
import bos_sample_conf 

import io
import hashlib
import base64
import requests
import re
import time
import json

#导入BOS相关模块
from baidubce import exception
from baidubce.services import bos
from baidubce.services.bos import canned_acl
from baidubce.services.bos.bos_client import BosClient

from baidubce.services.bos import storage_class
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#新建BosClient
bos_client = BosClient(bos_sample_conf.config)

response = bos_client.list_buckets()
for bucket in response.buckets:
    print(bucket.name)

bucket_name = 'looken-stars'

base_url = 'http://www.zuowen.com/xiaoxue/{grade}/{type}/'


sum = 0
for i in ['wunianji']:
    for j in ['xieren', 'xushi', 'xiejing', 'xiangxiang', 'zhuangwu', 'kantuxiehua', 'tonghuayuyan', 'duhougan', 'riji', 'shuxin', 'erge', 'guanhougan', 'xiaoshuo']:
        index = 1
        total_obj = []
        total_content = []
        ppp = 1
        qqq = 1
        while True:
            url = base_url.format(grade = i, type = j)
            if index != 1:
                url = url + 'index_' + str(index) + '.shtml'
            print(url)
            ret = requests.get(url)
            ret.encoding='gb2312'
            if '您要浏览的页面暂时无法访问或不存在' in ret.text:
                break

            con = ret.text.replace(' ', '')
            title = []
            res = re.findall("<ahref=\"(.*shtml)\"title=\"(.*)\"target=\"_blank\">.*</a>", con)
            for item in res:
                title.append([item[0], item[1]])

            
            desc = []
            res = re.findall("shtml\"rel=\"nofollow\">(.*)</a>", con)
            for item in res:
                desc.append(item[1])
            
            if len(desc) != len(title):
                break

            obj = []
            pos = 0
            for t in xrange(len(title)):
                q = requests.get(title[t][0])
                q.encoding='gb2312'
                if '您要浏览的页面暂时无法访问或不存在' in q.text:
                    continue


                con = q.text.replace(' ', '').replace('\n', '').replace('\r', '')
                #print(con)
                res = re.findall("\"con_content\">(.*)", con)
                try:
                    res = res[0]
                except Exception as e:
                    continue

                if '<pstyle=' in res:
                    res = res.split('<pstyle=')[0]
                elif '<p><br/>' in res:
                    res = res.split('<p><br/>')[0]
                else:
                    continue

                pos += 1
                tmp = {}
                tmp['title'] = title[t][1]
                tmp['url'] = title[t][0].split('/')[-1]
                tmp['desc'] = desc[t]
                obj.append(tmp)
                total_obj.append(tmp)
                total_content.append([res, title[t][0].split('/')[-1]])
                if len(total_obj) == 20:
                    with open('../data/paper_meta_%s_%s_%d' % (i, j, ppp), 'w') as writer:
                        writer.write(json.dumps(total_obj))

                    bos_client.put_object_from_file(bucket=bucket_name,
                            key = 'paper/meta/%s_%s_%d' % (i, j, ppp), file_name = '../data/paper_meta_%s_%s_%d' % (i, j, ppp), storage_class=storage_class.STANDARD)

                    ppp += 1
                    total_obj = []

                    for q in total_content:
                        with open('../data/paper_content_%s_%s_%s' % (i, j, q[1]), 'w') as writer:
                            writer.write(q[0])

                        bos_client.put_object_from_file(bucket=bucket_name,
                                key = 'paper/papers/%s_%s_%s' % (i, j, q[1]), file_name = '../data/paper_content_%s_%s_%s' % (i, j, q[1]), storage_class=storage_class.STANDARD)
                    total_content = []

            index += 1


