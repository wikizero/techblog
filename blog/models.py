# coding:utf-8
from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Task(models.Model):
    task = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=50, blank=True)
    future = models.BooleanField(default=False)  # Task是未来安排，则为True

    def __unicode__(self):
        return self.task


class History(models.Model):
    date = models.DateTimeField(auto_now=True)
    more = models.TextField(blank=True)
    # weather = models.CharField()
    # mood = models.CharField()
    status = models.CharField(max_length=10)  # low middle high

    def __unicode__(self):
        return self.date.strftime('%Y-%m-%d')


class Old(models.Model):
    daily = models.ForeignKey(History)
    task = models.CharField(max_length=50)
    reason = models.CharField(max_length=50, blank=True)
    done = models.BooleanField(default=False)  # True 为完成

    def __unicode__(self):
        return self.daily.date.strftime('%Y-%m-%d')


# ----------------notes---------------------

class Notes(models.Model):
    type = models.CharField(max_length=25)
    title = models.CharField(max_length=25)
    content = models.TextField(blank=True)
    create = models.DateTimeField(auto_now_add=True)
    edit = models.DateTimeField(auto_now=True)
    desc = models.CharField(max_length=100)
    show = models.BooleanField(default=True)

    def __unicode__(self):
        return self.type+'-'+self.title
