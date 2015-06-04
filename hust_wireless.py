#!/bin/env python
import argparse
import getpass
import requests
import re


parser = argparse.ArgumentParser(
        description='a cli tool to login in HUST_WIRELESS without Web Browsers')
# options
parser.add_argument(
        '-u', '--username', metavar='username', help='specify a username')
parser.add_argument(
        '-p', '--password', metavar='password', help='specify a password')
parser.add_argument(
        '-q', '--quiet', action='store_true', help='do not print the result')
args = parser.parse_args()


result = requests.get('http://www.baidu.com')

if result.text.find('eportal') != -1:
    username = args.username if args.username else input('username: ')
    password = args.password if args.password else getpass.getpass('password:')

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
