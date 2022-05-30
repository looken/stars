#! /usr/bin/python
#coding=utf-8

#导入BosClient配置文件
import bos_sample_conf 

import io
import hashlib
import base64

#导入BOS相关模块
from baidubce import exception
from baidubce.services import bos
from baidubce.services.bos import canned_acl
from baidubce.services.bos.bos_client import BosClient

#新建BosClient
bos_client = BosClient(bos_sample_conf.config)

response = bos_client.list_buckets()
for bucket in response.buckets:
    print(bucket.name)

bucket_name = 'looken-stars'
file_name = '../data/a.txt'

from baidubce.services.bos import storage_class

#从文件中上传冷存储类型的Object
bos_client.put_object_from_file(bucket=bucket_name,
        key = file_name.replace('../data/', ''), file_name = file_name, storage_class=storage_class.STANDARD)

