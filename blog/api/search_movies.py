# coding:utf-8
import requests
import urllib
from bs4 import BeautifulSoup
import re
import base64


def search(keyword):
    links = []

    url = 'https://www.baidu.com/s?ie=UTF-8&wd={keyword}'.format(keyword=urllib.quote(keyword + ' 720P/1080P/BD/HD'))

    headers = {u'Accept-Language': u'zh-CN,zh;q=0.9,en;q=0.8',
               u'Accept-Encoding': u'gzip, deflate, br',
               u'Host': u'www.baidu.com',
               u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               u'Upgrade-Insecure-Requests': u'1',
               u'Connection': u'keep-alive',
               u'Referer': u'https://www.baidu.com/',
               u'User-Agent': u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

    response = requests.get(url=url, headers=headers)

    for row in BeautifulSoup(response.text, 'lxml').find_all(class_='c-container'):
        link = row.a['href']
        try:
            text = requests.get(url=link, timeout=5).content

            thunders = re.findall('"((ftp|ed2k|thunder)s?://.*?)"', text)
            magnets = re.findall('"((magnet):\?xt=.*?)"', text)
            seed = set(thunders + magnets)

            for t, type_ in seed:
                if type_ == 'thunder':
                    ret = base64.b64decode(t.replace('thunder://', ''))[2:-2]
                elif type_ in ['ed2k', 'magnet']:
                    ret = urllib.unquote(t)
                else:
                    ret = t
                links.append(ret)

        except Exception as e:
            pass

    return links


if __name__ == '__main__':
    print search(keyword='杀破狼')
