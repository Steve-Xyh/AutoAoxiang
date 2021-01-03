#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import getpass
from bs4 import BeautifulSoup
from . import formatString
from .getInfo import remove_cache


def login(user='', passwd='', urlLogin='https://uis.nwpu.edu.cn/cas/login'):
    '''
    使用POST方法登录

    #### Parameters::
        user - 用户名
        passwd - 密码
        urlLogin - 登录链接

    #### Returns::
        返回session, 登录状态status
        status = 1: 登录成功
        status = 0: 密码正确, 登录失败
        status = -1: 密码错误
    '''

    session = requests.Session()
    session.get(urlLogin)

    # 登录页请求头
    header = {
        'Origin': 'https://uis.nwpu.edu.cn',
        'Referer': urlLogin,
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # 登录信息
    loginData = {
        'username': user,
        'password': passwd,
        'currentMenu': 1,
        'execution': 'e1s1',
        '_eventId': 'submit',
    }

    res = session.post(url=urlLogin, data=loginData, headers=header).text

    if res.find('Log In Successful') != -1:
        print(f'用户:{user}'+formatString.setColor(string='登录成功√', color='greenFore'))
        status = 1
    else:
        if res.find('Invalid credentials.') != -1:
            print(f'用户:{user}'+formatString.setColor(string='密码错误, 请重试', color='redBack'))
            status = -1
        else:
            print(
                f'用户:{user}' +
                formatString.setColor(
                    string='密码正确, 登录失败, 准备重新登录...', color='redBack'
                ))
            status = 0

    return session, status


def login_check(user='', passwd=''):
    '''
    检查登录状态, 若登录失败则反复尝试
    '''

    session, status = login(user=user, passwd=passwd)
    while True:
        if status == 1:
            return session
        else:
            if status == -1:
                remove_cache()
                exit(-1)
            else:
                print('正在重新登录...')
                session, status = login(user=user, passwd=passwd)

    return session


# if __name__ == "__main__":
#     username = str(input('学号:'))
#     password = str(getpass.getpass('密码:'))

#     login(user = username, passwd = password)
