# coding:utf-8
import requests
import re, uniout


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


def ip_info():
    url = 'http://2017.ip138.com/ic.asp'
    try:
        ret = requests.get(url)
        ret.encoding = 'gb2312'
        text = ret.text
        ip = re.findall(r'\[(.*)\]', text)[0]
        address = re.findall(u'<center>.*：(.*)</center>', text)[0]

    except Exception as e:
        print('Get ip info catch exception:'), e
        return False

    return ip, address


if __name__ == '__main__':
    # print addr('113.12.99.199')
    # print addr('159.106.121.75')['country']
    # print addr('52.209.36.7')['country']
    print ip_info()

