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

import sys
reload(sys)
sys.setdefaultencoding('utf8')

#新建BosClient
bos_client = BosClient(bos_sample_conf.config)

response = bos_client.list_buckets()
for bucket in response.buckets:
    print(bucket.name)

bucket_name = 'looken-stars'

def send(data, path, name):
    print(path, name)
    with open("../data/" + name, "w") as fp:
        try:
            fp.write(data)
        except Exception as e:
            return

    file_name = '../data/' + name

    #从文件中上传冷存储类型的Object
    ret = bos_client.put_object_from_file(bucket=bucket_name,
            key = path + '/' + name, file_name = file_name, storage_class=storage_class.STANDARD)
