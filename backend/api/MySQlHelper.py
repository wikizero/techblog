# coding:utf-8
import MySQLdb
import re
import pandas as pd
from collections import OrderedDict


class MySQLHelper:
    def __init__(self):
        """
        batch operation for mysql

        """
        pass

    @staticmethod
    def create_engine(connect, charset='utf8'):
        user, password, host, port, db_name = re.split(r':|@|/', connect)
        db_connect = MySQLdb.connect(user=user, host=host, passwd=password, db=db_name, charset=charset)
        return db_name, db_connect, db_connect.cursor()

    @staticmethod
    def source_analysis(source):
        if isinstance(source, list):
            return source
        elif isinstance(source, pd.DataFrame):
            return source.to_dict(orient='records')
        else:
            raise Exception('Data type is not supported')

    @staticmethod
    def execute_query(sql, engine):
        db_name, con, cur = engine
        cur.execute(sql)
        result = cur.fetchall()
        return result

    @staticmethod
    def execute_not_query(sql, engine):
        db_name, con, cur = engine
        cur.execute(sql)
        con.commit()
        return True

    @staticmethod
    def insert_many(table, source, engine, conflict=None, limit=10000, field_status=None):
        db_name, con, cur = engine

        if conflict == 'replace':
            prefix = 'replace into ' + table
        elif conflict == 'ignore':
            prefix = 'insert ignore into ' + table
        elif not conflict:
            prefix = 'insert into ' + table
        else:
            raise Exception('conflict is not supported, It just can be replace or ignore')

        source = MySQLHelper.source_analysis(source)
        fields = source[0].keys()
        values = [one.values() for one in source]

        if field_status:
            fields = map(field_status, fields)

        fields_str = ' (' + ','.join(fields) + ') '
        values_str = ' (' + ','.join(['%s']*len(fields)) + ') '

        sql = prefix + fields_str + 'values' + values_str
        print sql

        for index in xrange(0, len(values), limit):
            insert_values = values[index:index+limit]
            cur.executemany(sql, insert_values)
            con.commit()
            print len(insert_values), ' rows affected'

        return True

    @staticmethod
    def update_many(table, source, engine, condition=[], limit=10000):
        """
        :param table: table name
        :param source: dict-list
        :param engine: call create_engine() will return an engine
        :param condition: list, eg: ['id']
               update table set fields = %s where condition = %s

        """
        db_name, con, cur = engine

        # sort the columns
        columns = source[0].keys()
        set_columns = list(set(columns) - set(condition))
        columns = set_columns + condition

        set_str = ','.join([c+'=%s' for c in set_columns])
        condition_str = ','.join([c+'=%s' for c in condition])

        _source = [[dct[column] for column in columns] for dct in source]
        
        sql = 'UPDATE ' + table + ' SET ' + set_str + ' where ' + condition_str
        print sql

        for index in xrange(0, len(_source), limit):
            insert_values = _source[index:index+limit]
            cur.executemany(sql, insert_values)
            con.commit()
            print len(insert_values), ' rows affected'

        return True
        
if __name__ == '__main__':
    # how to use it in your work
    from datetime import datetime
    now = datetime.now()
    source = [
        {
            'id': 10,
            'task': 'taa',
            'reason': now,
        },
        {
            'id': 11,
            'task': 'task',
            'reason': now,
        },
        {
            'id': 13,
            'task': 'tasa',
            'reason': now,
        },
    ]
    engine = MySQLHelper.create_engine('root:root@127.0.0.1:3306/Jobs')
    # MySQLHelper.insert_many('blog_task', source, engine, conflict='replace')
    # MySQLHelper.update_many('blog_task', source, engine, condition=['id'], limit=1)
    print MySQLHelper.execute_query('select count(*) from job', engine)[0][0]