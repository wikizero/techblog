# coding:utf-8

table = 'TestTable'
lst = [
	{
		'name': 'Alice',
		'age': 18,
		'profession': 'English'
	},
	{
		'name': 'Tom',
		'age': 19,
		'profession': 'Computer'
	},
	{
		'name': 'Bob',
		'age': 19,
		'profession': 'AI'
	}
]
# 字典key 默认按字母排序，所以不用考虑字典结构数据的散列问题（数据无序存储）
# 此模式一定必须保持每个字典的key的值与数量是一致的，否则可能会导致数据混乱
# insert into mytb values(%s, %s)

"""
Replace:
key: ID, unique字段
(1)当没有key时，replace相当于普通的insert.
(2)当有key时，可以理解为删除重复key的记录，在保持key不变的情况下，delete原有记录，再insert新的记录，
新纪录的值只会录入replace语句中字段的值，其余没有在replace语句中的字段，会自动填充默认值。

"""
print lst
columns = lst[0].keys()
values = [one.values() for one in lst]
print values

prefix = 'insert ignore into'  # replace into
columns_str = '(' + ','.join(columns) + ')'
values_str = '(' + ','.join(['%s']*len(columns)) + ')'
values_word = 'values'
sql = ' '.join([prefix, table, columns_str, values_word, values_str])
print sql

