#! /usr/bin/python
#coding=utf-8

#导入BosClient配置文件
import bos_sample_conf 

import json
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

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#新建BosClient
bos_client = BosClient(bos_sample_conf.config)

response = bos_client.list_buckets()
for bucket in response.buckets:
    print(bucket.name)

bucket_name = 'looken-stars'

isTruncated = True

# 用户可设置每页最多500条记录
max_keys = 500
marker = None
data = []
chunk = []
while isTruncated:
    response = bos_client.list_objects(bucket_name, prefix = 'emoji', max_keys = max_keys, marker=marker)
    for obj in response.contents:
        if 'emoji' not in obj.key or obj.key == 'emoji/':
            continue

        url = 'https://looken-stars.bj.bcebos.com/' + obj.key
        chunk.append(url)
        if len(chunk) == 20:
            data.append(chunk)
            chunk = []

        isTruncated = response.is_truncated
        marker = getattr(response,'next_marker',None)

if chunk:
    data.append(chunk)

for i in xrange(len(data)):
    with open('../data/emoji-' + str(i) + '.txt', 'w') as writer:
        for url in data[i]:
            try:
                writer.write('%s\n' % (url))
            except Exception as e:
                print(e)
                pass

    #从文件中上传冷存储类型的object
    bos_client.put_object_from_file(bucket=bucket_name,
            key = 'meta-info/emoji-' + str(i) + '.txt', file_name = '../data/emoji-' + str(i) + '.txt', storage_class=storage_class.STANDARD)

