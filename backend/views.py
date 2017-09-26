# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from sqlalchemy import create_engine
import json
from api.CJson import CJsonEncoder


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
    engine = create_engine("mysql://root:root@39.108.141.110:3306/world", encoding="utf-8")
    sql = 'select * from ' + table + ' limit ' + str(num) + ' , ' + limit
    df = pd.read_sql_query(sql, engine)
    lst_dct = df.to_dict(orient='records')

    _json = {
        'code': 0,
        'msg': "",
        'count': 400,
        'data': lst_dct
    }
    return HttpResponse(json.dumps(_json, cls=CJsonEncoder), content_type="application/json")
