#! /usr/bin/python
#coding=utf-8

#导入BosClient配置文件
import bos_sample_conf 

import io
import hashlib
import base64
import requests
import re
import json

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

base_url = 'http://wufazhuce.com/'

url = base_url
ret = requests.get(url)

content = ret.text.split('<div class="carousel-inner">')[1].split('<a class="left carousel-control"')[0].split('<div class="item')[1:]

ret = []
for item in content:
    tmp = item.replace('\n', '').replace(' ', '')
    img = tmp.split('imgclass="fp-one-imagen"src="')[1].split('"alt=""/>')[0]
    title = tmp.split('<divclass="fp-one-imagen-footer">')[1].split('</div><divclass="fp-one-cita-wra')[0]
    top = tmp.split('pclass="titulo">')[1].split('</p><pclass="dom"')[0]
    mid = tmp.split('<pclass="dom">')[1].split('</p><pclass="')[0]
    bottom = tmp.split('</p></div><divclass="fp-on')[0].split('">')[-1]
    txt = tmp.split('</a></div><divclass="clearfi')[0].split('">')[-1]

    response = requests.get(img)
    name = img.split('/')[-1]
    with open("../data/" + name + ".png", "wb") as fp:
        for data in response.iter_content(128):
            fp.write(data)

    file_name = '../data/' + name + ".png"

    #从文件中上传冷存储类型的Object
    bos_client.put_object_from_file(bucket=bucket_name,
            key = 'one/images/' + file_name.replace('../data/', ''), file_name = file_name, storage_class=storage_class.STANDARD)

    res = {}
    res['img'] = 'https://looken-stars.bj.bcebos.com/one/images/' + file_name.replace('../data/', '')
    res['title'] = title
    res['top'] = top
    res['mid'] = mid
    res['bottom'] = bottom
    res['desc'] = txt.replace('<br/>', '')

    print(res)
    ret.append(res)

    with open('../data/one2.txt', 'w') as fp:
        fp.write(json.dumps(ret))

    bos_client.put_object_from_file(bucket=bucket_name,
            key = 'one/meta/one2.txt', file_name = '../data/one2.txt', storage_class=storage_class.STANDARD)
    

