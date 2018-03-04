# coding: utf-8
import redis
import time

redis_con = redis.Redis()


def public(channel, msg):
    redis_con.publish(channel, msg)


def subscribe(channel):
    pub = redis_con.pubsub()
    pub.subscribe(channel)
    pub.parse_response()
    return pub.parse_response()


if __name__ == '__main__':
    # 订阅
    # while True:
    #     data = subscribe('default')
    #     print data

    # 发布
    # public('A', '啥东西嘛')

    import numpy as np
    array_ = np.array(range(12)).reshape(3, 4)
    print array_
    print array_[:, 0]  # python数组切片, 不一定需要[:, :]

    import pandas as pd
    df = pd.DataFrame(data=[['Alice', 'girl', 18, 171],
                            ['Bob', 'boy', 19, 172],
                            ['Tom', 'boy', 17, 173],
                            ['Lucy', 'girl', 18, 172]],
                      columns=['Name', 'Sex', 'Age', 'Class'],
                      index=['A', 'B', 'C', 'D'])
    print df.ix[:2, ['Age']]

    import string
    print dict(enumerate(string.ascii_uppercase, 1))

