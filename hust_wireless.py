#!/bin/env python
# -*- coding: UTF-8 -*-
import argparse
import getpass
import requests
import sys
import re
# import keyword


description = 'Login in HUST_WIRELESS without web browsers'

# a list of (args, kwargs)
options = (
    (('-u', '--username'), {'metavar': 'username'}),
    (('-p', '--password'), {'metavar': 'password'}),
    (('-q', '--quiet'), {
        'action': 'store_true',
        'help': "don't print to stdout"}),
)

parser = argparse.ArgumentParser(description=description)
for opt in options:
    parser.add_argument(*opt[0], **opt[1])
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
    params = pattarn.findall(result.text)

    url = (
            'http://192.168.50.3:8080/eportal/userV2.do?'
            'method=login&param=true&' + params[0])

    post_data = {
            'username': username,
            'pwd': password
            }

    result = requests.request('POST', url, data=post_data)
    if result.text.find('认证失败') != -1:
        pattarn = re.compile(r"(认证失败.*?)(?:'|\")")
        login_res = pattarn.findall(result.text)
        print(login_res[0])
    else:
        print('Successfully Login In')

elif result.text.find('baidu') != -1:
    print('You are already logged in')

else:
    print("Opps, something goes wrong!")
