# coding:utf-8
from django.shortcuts import render, redirect, HttpResponse, render_to_response
from models import *
import random
import json
import re
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from algorithm.UserCF import *
from datetime import datetime


# Create your views here.

@csrf_exempt
def sign_in(request):
	if request.method == 'POST':
		username = request.POST.get('username', False)
		pw = request.POST.get('pw', False)
		user = authenticate(username=username, password=pw)
		if user:
			login(request, user)
			return redirect('/hall')
	elif request.method == 'GET':
		username = request.GET.get('username', False)
		pw = request.GET.get('pw', False)
		if not username or not pw:
			return render(request, 'login.html')
		user = authenticate(username=username, password=pw)
		msg = {
			'msg': u'登录成功，正在前往电影大厅！',
			'type': 'success'
		}
		if not user:
			msg['msg'] = u'账号或密码错误,请检查后重新登录!'
			msg['type'] = 'danger'
		return HttpResponse(json.dumps(msg), content_type='application/json')


@csrf_exempt
def register(request):
	if request.method == 'POST':
		username = request.POST.get('username', False)
		pw = request.POST.get('pw', False)
		rpw = request.POST.get('rpw', False)

		# 生成随机编号
		number = random.randint(1000000, 9999999)
		if not ExtUser.objects.filter(number=number):
			user = User.objects.create_user(username=username, password=pw)
			ExtUser.objects.create(user=user, number=number)
			user = authenticate(username=username, password=pw)
			login(request, user)
			return redirect('/sort/label')
	elif request.method == 'GET':
		username = request.GET.get('username', False)
		pw = request.GET.get('pw', False)
		rpw = request.GET.get('rpw', False)
		if not username or not pw:
			return render(request, 'register.html')
		msg = {
			'msg': u'账号注册成功, 请继续完善个人信息!',
			'type': 'success'
		}
		if not pw.isalnum():
			msg['msg'] = u'密码只能由数字字母组成！'
			msg['type'] = 'danger'
		if pw != rpw:
			msg['msg'] = u'两次输入的密码不一致！'
			msg['type'] = 'danger'
		if len(pw) < 6:
			msg['msg'] = u'密码至少需要6个字符！'
			msg['type'] = 'danger'
		if User.objects.filter(username=username):
			msg['msg'] = u'用户名已经存在！'
			msg['type'] = 'danger'

		return HttpResponse(json.dumps(msg), content_type='application/json')


def sign_out(request):
	logout(request)
	return redirect('/hall')


def sort_label(request):
	if request.method == 'GET':
		labels = request.GET.get('text', False)
		if labels:
			labels = labels.replace(' ', '/')
			ext = ExtUser.objects.get(user=request.user)
			labels = labels.encode('utf-8')
			ext.labels = labels
			ext.save()
			return redirect('/personal/rec')

	u_labels = []
	ext = ExtUser.objects.get(user=request.user)
	if ext.labels:
		u_labels = ext.labels.split('/')
	return render(request, 'sort-label.html', {'labels': u_labels})


def find(request):
	if request.method == 'GET':
		text = request.GET.get('text', False)
		movies = None
		if text:
			movies = Movie.objects.filter(Q(film_name__contains=text) | Q(actors__contains=text)).order_by('year')[::-1]

		return render(request, 'find.html', {'movies': movies, 'text': text})


@csrf_exempt
def movie_detail(request):
	if request.method == 'GET':
		douban_id = request.GET.get('id', False)
		movie = Movie.objects.filter(douban_id=douban_id)
		movies = Movie.objects.all().order_by('year')[::-1][:20]

		all_label = movie[0].labels.split('/')
		l_movies = []
		for l in all_label:
			if request.user.is_authenticated:
				plst = Movie.objects.filter(Q(labels__contains=l.strip()) & ~Q(love__user=request.user) & ~Q(
					douban_id=movie[0].douban_id))
			else:
				plst = Movie.objects.filter(Q(labels__contains=l.strip()) & ~Q(douban_id=movie[0].douban_id))
			l_movies.append(plst)  # 还可以在这里过滤喜欢／不喜欢的电影

		movies_lst = []
		for movies in l_movies:
			temp = []
			for m in movies:
				m = model_to_dict(m)
				label_lst = m['labels'].split('/')
				map(lambda x: x.strip(), label_lst)
				m['labels'] = label_lst
				m['point'] = m['douban_rate'] + m['douban_comment_num'] * 1.0 / 10000
				if m not in temp and m not in movies_lst:
					temp.append(m)
			temp = sorted(temp, key=lambda x: x['point'], reverse=True)[:2]
			movies_lst.extend(temp)
		comments = Comment.objects.filter(movie=movie[0]).order_by('comment_date')[::-1]
		comment_lst = []
		love_dct = {
			'like': u'喜欢',
			'dislike': u'不喜欢',
			'want': u'想看'
		}
		for comment in comments:
			love = Love.objects.filter(movie=comment.movie, user=comment.user)
			com = model_to_dict(comment)
			com['username'] = comment.user.username
			com['date'] = comment.comment_date
			if love:
				com['type'] = love_dct.get(love[0].type, u'未知')
			else:
				com['type'] = u'未知'
			comment_lst.append(com)

		if movie:
			return render(request, 'movie_detail.html', {'movie': movie[0], 'movies': movies_lst, 'comments': comment_lst})
	elif request.method == 'POST':
		text = request.POST.get('text', False)
		m_id = request.POST.get('id', False)
		if not m_id:
			return HttpResponse('error')
		movie = Movie.objects.get(douban_id=int(m_id))
		msg = {
			'msg': u'天了噜 ，发生未知错误',
			'type': 'danger'
		}
		if not request.user.is_authenticated:
			msg['msg'] = u'请先登录，再提交评论!'
			msg['type'] = 'danger'
			return HttpResponse(json.dumps(msg), content_type='application/json')
		if text:
			Comment.objects.create(user=request.user, movie=movie, comment=text)
			msg['msg'] = u'评论提交成功，页面即将刷新!'
			msg['type'] = 'success'

		return HttpResponse(json.dumps(msg), content_type='application/json')

	return HttpResponse('You have to commit the id!!!')


@login_required(login_url='/login')
def personal_rec(request):

	# 站内推荐
	site_rec = Movie.objects.all().order_by('year')[::-1][:15]

	# 我的标签
	ext = ExtUser.objects.get(user=request.user)
	if not ext.labels:
		return redirect('/sort/label')
	all_label = ext.labels.split('/')  # 获取用户喜爱标签
	print all_label
	l_movies = []
	for l in all_label:
		l_movies.append(Movie.objects.filter(Q(labels__contains=l) & ~Q(love__user=request.user)))

	movies_lst = []
	for movies in l_movies:
		temp = []
		for m in movies:
			m = model_to_dict(m)
			label_lst = m['labels'].split('/')
			map(lambda x: x.strip(), label_lst)
			m['labels'] = label_lst
			m['point'] = m['douban_rate'] + m['douban_comment_num'] * 1.0 / 10000  # 推荐指数计算
			if m not in temp and m not in movies_lst:
				temp.append(m)
		temp = sorted(temp, key=lambda x: x['point'], reverse=True)[:5]  # 按照推荐指数排序
		movies_lst.extend(temp)

	# 猜你喜欢
	my_like = Movie.objects.filter(Q(love__type='like') & Q(love__user=request.user))
	my_like_id = [m.douban_id for m in my_like]

	all_data = {}
	all_user = User.objects.all()  # 获取所有用户信息
	for u in all_user:
		if u != request.user:
			movie = Movie.objects.filter(Q(love__type='like') & Q(love__user=u))
			all_data[u.id] = [m.douban_id for m in movie]

	rec_movie = None
	final_rec_movie = []
	sim_data = getSimilarity(my_like_id, all_data).items()  # 调用基于用户的协同过滤算法
	for user_id, sim_rate in sim_data:
		user = User.objects.get(id=user_id)
		rec_movie = Movie.objects.filter(Q(love__type='like') & Q(love__user=user)).filter(
			~Q(love__user=request.user))  # 将除目标用户以外用户所有喜爱电影取出并过滤掉与目标用户的接触过的电影
		if rec_movie.count() >= 5:
			break  # 推荐电影的数量大于等于5时才可以
	if not rec_movie or rec_movie.count() < 5:
		final_rec_movie = movies_lst[:5]
		for m in final_rec_movie:
			m['labels'] = '/'.join(m['labels'])
	else:  # 当推荐电影不足时，可以通过标签与推荐指数结合的方法进行推荐（冷启动处理方法）
		for m in rec_movie:
			m = model_to_dict(m)
			point = m['douban_rate'] * 0.6 / 2 + m['douban_comment_num'] * 0.4 / 10000  # 计算推荐指数
			m['point'] = point
			point = 5 if int(point) > 5 else int(point)
			m['point_lst'] = list(''.join(['1' for i in range(point)]).zfill(5)[::-1])
			if m not in final_rec_movie:
				final_rec_movie.append(m)
	final_rec_movie = sorted(final_rec_movie, key=lambda x: x['point'], reverse=True)[:5]  # 排序 取前五个

	data = {
		'site_rec': site_rec,
		'movies': movies_lst,
		'labels': all_label,
		'guess_like': final_rec_movie
	}

	return render(request, 'personal-rec.html', data)


@csrf_exempt
@login_required(login_url='/login')
def person_center(request):
	if request.method == 'GET':
		want_movies = Movie.objects.filter(love__type='want', love__user=request.user)
		like_movies = Movie.objects.filter(love__type='like', love__user=request.user)
		dislike_movies = Movie.objects.filter(love__type='dislike', love__user=request.user)
		data = {
			'like': like_movies,
			'want': want_movies,
			'dislike':dislike_movies
		}
		return render(request, 'person-center.html', data)

	elif request.method == 'POST':
		douban_id = request.POST.get('m_id', False)
		msg = {
			'msg': u'未知错误，请刷新后重试！',
			'type': 'danger'
		}
		if douban_id:
			love = Love.objects.filter(user=request.user, movie__douban_id=int(douban_id))
			if love:
				love.delete()
				msg['msg'] = u'电影已从列表移除成功, 页面将要刷新!'
				msg['type'] = 'success'

		return HttpResponse(json.dumps(msg), content_type='application/json')


@csrf_exempt
@login_required(login_url='/login')
def operate(request):
	if request.method == 'POST':
		op_type = request.POST.get('type', False)
		douban_id = request.POST.get('id', False)
		dct = {
			'like': u'<喜欢>',
			'dislike': u'<黑名单>',
			'want': u'<想看>'
		}
		if op_type not in ['like', 'dislike', 'want']:
			return HttpResponse('type error')
		movie = Movie.objects.get(douban_id=int(douban_id))
		if not movie:
			return HttpResponse('can find the movie maybe: douban id is error!!!')
		love = Love.objects.filter(user=request.user, movie=movie)
		if love:
			love[0].type = op_type
			love[0].save()
		else:
			Love.objects.create(user=request.user, movie=movie, type=op_type)
		msg = {
			'msg': u'已加入我的' + dct[op_type] + u'列表',
			'type': 'success'  # type: success, info, danger, warning
		}
		return HttpResponse(json.dumps(msg), content_type='application/json')


def hall(request):
	select_area = request.GET.get('area', False)
	select_type = request.GET.get('type', False)
	select_time = request.GET.get('time', False)
	select_filter = request.GET.get('filter', False)
	if not select_area:
		select_area = u'全部'
	if not select_type:
		select_type = u'全部'
	if not select_time:
		select_time = u'全部'
	if not select_filter:
		select_filter = u'全部'

	area_lst = [u'全部', u'大陆', u'香港', u'台湾', u'美国', u'韩国', u'日本', u'英国', u'法国', u'泰国', u'俄罗斯', u'印度']
	type_lst = [u'全部', u'武侠', u'警匪', u'犯罪', u'动作', u'战争', u'恐怖', u'惊悚', u'纪录片', u'冒险', u'悬疑', u'动画', u'喜剧',
				u'爱情', u'短片']
	time_lst = [u'全部', '2017', '2016', '2015', '2014', '2013', '2012', '2010', u'00年代', u'90年代', u'80年代', u'更早']
	filter_lst = [u'全部', u'评分最高', u'评论最多', u'收藏最多', u'最新上映']

	# 安全处理
	if select_area not in area_lst or select_type not in type_lst or select_time not in time_lst or \
					select_filter not in filter_lst:
		return HttpResponse('sorry, search key error!!!')

	# 查看所有标签／演员／地区
	# all_labels = []
	# for m in Movie.objects.all():
	# 	labels = m.labels.split('/')
	# 	all_labels.extend(map(lambda x: x.strip(), labels))
	#
	# for i in set(all_labels):
	# 	print i
	# TODO 时间 收藏最多
	area = '' if select_area == u'全部' else select_area
	type = '' if select_type == u'全部' else select_type
	movies = Movie.objects.filter(Q(area__contains=area) & Q(labels__contains=type)).order_by('year')

	# time
	# notes: gte >=   lte <=   lt <   gt >
	if select_time.isdigit():
		movies = movies.filter(year=int(select_time))
	elif select_time == u'00年代':
		movies = movies.filter(Q(year__lt=2010) & Q(year__gt=2000))
	elif select_time == u'90年代':
		movies = movies.filter(Q(year__lt=2000) & Q(year__gt=1990))
	elif select_time == u'80年代':
		movies = movies.filter(Q(year__lt=1990) & Q(year__gt=1980))
	elif select_time == u'更早':
		movies = movies.filter(Q(year__lt=1980))

	# filter
	if select_filter == u'评分最高':
		movies = movies.order_by('douban_rate')
	if select_filter == u'评论最多':
		movies = movies.order_by('douban_comment_num')

	data = {
		'movies': movies[::-1][:30],
		'area_lst': area_lst,
		'type_lst': type_lst,
		'time_lst': time_lst,
		'filter_lst': filter_lst,
		'select_area': select_area,
		'select_type': select_type,
		'select_time': select_time,
		'select_filter': select_filter,
	}
	return render(request, 'hall.html', data)
