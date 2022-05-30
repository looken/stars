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

prefix = ""

isTruncated = True
max_keys = 500
marker = None
num = 0
while isTruncated:
    response = bos_client.list_objects(bucket_name, max_keys = max_keys, marker=marker)
    for obj in response.contents:
        try:
            num += 1
            if num % 100 == 0:
                print('delete %d' % (num))
            bos_client.delete_object(bucket_name, obj.key)
        except Exception as e:
            print(e)
    isTruncated = response.is_truncated
    marker = getattr(response,'next_marker',None)



