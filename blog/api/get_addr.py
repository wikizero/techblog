# coding:utf-8
import requests


def addr(ip):
    url = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip='+ip
    try:
        rep = requests.get(url).json()
    except Exception, e:
        print '----Get addr catch exception----', e
        rep = False

    if not rep:
        return False
    return rep


# print addr('113.12.99.199')
# print addr('159.106.121.75')['country']
# print addr('52.209.36.7')['country']


