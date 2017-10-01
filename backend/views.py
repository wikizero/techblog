# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from sqlalchemy import create_engine
import json
from django.core.serializers.json import DjangoJSONEncoder
import pymongo

# Create your views here.


def index(request):
    return render(request, 'backend/index.html')


def get_sword_data(request):
    return render(request, 'backend/sword-data.html')


def get_world_data(request):
    return render(request, 'backend/my-world-data.html')


def get_raw_data(request):
    '''
    ① select * from table limit 2,1;
    //含义是跳过2条取出1条数据，limit后面是从第2条开始读，读取1条信息，即读取第3条数据
    
    ② select * from table limit 2 offset 1;
    //含义是从第1条（不包括）数据开始取出2条数据，limit后面跟的是2条数据，offset后面是从第1条开始读取，即读取第2,3条
    '''

    table = request.GET.get('t', False)
    page = request.GET.get('page', False)
    limit = request.GET.get('limit', False)
    num = (int(page) - 1)*int(limit)

    #engine = create_engine("mysql://root:root@39.108.141.110:3306/world", encoding="utf-8")
    import pymysql as mysql
    table = 'swordinfo' if table == 'sword' else table
    engine = mysql.connect(host="localhost",user="root",passwd="root",db="world",charset='utf8')
    sql = 'select * from ' + table + ' order by release_date desc limit ' + str(num) + ' , ' + limit
    df = pd.read_sql(sql, engine)
    count = pd.read_sql('select count(*) as sum from '+table, engine)
    lst_dct = df.to_dict(orient='records')
    count = count['sum'].tolist()[0]
    #client = pymongo.MongoClient('localhost', 27017)
    #db = client['world']
    #collection = db[table]
    #count = collection.find().count()
    #df = pd.DataFrame(list(collection.find({}, {'_id': 0}).sort([('release_date', -1)]).skip(num).limit(int(limit))))
    #lst_dct = df.to_dict(orient='records')
    
    _json = {
        'code': 0,
        'msg': "",
        'count': count,
        'data': lst_dct
    }
    return HttpResponse(json.dumps(_json, cls=DjangoJSONEncoder), content_type="application/json")
