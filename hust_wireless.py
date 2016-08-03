#!/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals  # noqa

import re
import sys
import argparse
import getpass
import requests


parser = argparse.ArgumentParser(
    description='Login in HUST_WIRELESS without web browsers')

# a list of (args, kwargs)
options = [
    (('-u', '--username'), {'metavar': 'username'}),
    (('-p', '--password'), {'metavar': 'password'}),
    (('-q', '--quiet'), {
        'action': 'store_true',
        'help': "don't print to stdout"}),
]
for args, kwargs in options:
    parser.add_argument(*args, **kwargs)
args = parser.parse_args()


try:
    result = requests.get('http://www.baidu.com')
except Exception:
    print('Failed to connecte test webside!')
    sys.exit()

if result.text.find('eportal') != -1:
    try:
        input = raw_input
    except NameError:
        pass
    username = args.username if args.username else input('Username: ')
    password = args.password if args.password else getpass.getpass()

    pattarn = re.compile(r"href=.*?\?(.*?)'")
    query_str = pattarn.findall(result.text)

    url = 'http://192.168.50.3:8080/eportal/InterFace.do?method=login'
    post_data = {
        'userId': username,
        'password': password,
        'queryString': query_str,
        'service': '',
        'operatorPwd': '',
        'validcode': '',
    }
    responce = requests.request('POST', url, data=post_data)
    responce.encoding = 'UTF-8'
    res_json = responce.json()

    if res_json['result'] == 'fail':
        print(res_json['message'])
    else:
        print('认证成功')

elif result.text.find('baidu') != -1:
    print('已在线')
else:
    print("Opps, something goes wrong!")
