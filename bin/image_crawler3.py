#! /usr/bin/python
#coding=utf-8

#导入BosClient配置文件
import bos_sample_conf 

import io
import hashlib
import base64
import requests
import re

#导入BOS相关模块
from baidubce import exception
from baidubce.services import bos
from baidubce.services.bos import canned_acl
from baidubce.services.bos.bos_client import BosClient

from baidubce.services.bos import storage_class

#新建BosClient
bos_client = BosClient(bos_sample_conf.config)

response = bos_client.list_buckets()
for bucket in response.buckets:
    print(bucket.name)

bucket_name = 'looken-stars'

base_url = 'http://www.bbsnet.com/biaoqingbao/page/{id}'

sum = 0
for i in xrange(1, 14):
    url = base_url.format(id = i)
    ret = requests.get(url)
    if ret.status_code != 200:
        continue

    res = re.findall("<img src=\"(.*)\" wid.*alt=\"(.*)\"/>", ret.text)
    for item in res:
        try:
            response = requests.get(item[0])
            name = item[1]
            if not name:
                continue

            if name[0] == '\'':
                name = name[1:]

            if name[-1] == '\'':
                name = name[:-1]

            with open("../data/" + name + "." + item[0].split('.')[-1], "wb") as fp:
                for data in response.iter_content(128):
                    fp.write(data)

            sum += 1
            print("处理完成 %d" % (sum))

            file_name = '../data/' + name + "." + item[0].split('.')[-1]
  
            #从文件中上传冷存储类型的Object
            bos_client.put_object_from_file(bucket=bucket_name,
                    key = 'emoji/' + file_name.replace('../data/', ''), file_name = file_name, storage_class=storage_class.STANDARD)
        except Exception as e:
            print(e)
