# coding:utf-8
import re
from datetime import datetime
import pprint
import random
import pymysql as mysql
from pandas import read_sql
from compiler.ast import flatten
import jieba
import re
from collections import Counter


class forData:
	def __init__(self):
		self.engine = mysql.connect(host="localhost", user="root", passwd="root", db="Jobs", charset='utf8')

	def job_python(self, field, position_type):
		sql = "SELECT {field} FROM jobanalysis WHERE type = '{position_type}'".format(field=field,
		                                                                              position_type=position_type)
		df = read_sql(sql, self.engine)
		pos_type = df[field].tolist()
		pos_type = flatten([re.split(u';|,|，|、| ', t) for t in pos_type])
		field_type, field_num = [], []
		for k, v in sorted(Counter(pos_type).items(), key=lambda x: x[1], reverse=True):
			field_type.append(k)
			field_num.append(int(v))
		return field_type, field_num

	def job_query(self, field):
		sql = "SELECT {field}, count(*) AS count FROM jobanalysis WHERE type = 'Python' GROUP BY {field} ORDER BY " \
		      "COUNT(*) desc;".format(field=field)
		df = read_sql(sql, self.engine)
		return df[field].tolist(), df['count'].tolist()


if __name__ == '__main__':
	# label, num = forData().job_python('label', 'Python')
	# for k, v in zip(label, num):
	# 	print k, ' : ', v
	engine = mysql.connect(host="localhost", user="root", passwd="root", db="Jobs", charset='utf8')
	sql = "SELECT `desc` FROM jobanalysis WHERE type = 'Python'"
	df = read_sql(sql, engine)
	desc = ' '.join(df['desc'].tolist())
	word_lst = jieba.cut(desc)
	words = [re.sub('\s', '', w).lower() for w in word_lst if re.sub('\s', '', w) and len(w) > 1 and re.findall(r'[0-9a-zA-Z]+', w)]
	ret = Counter(words)
	for k, v in ret.most_common(50):
		print k.capitalize(), v
	print dict(ret.most_common(50))

