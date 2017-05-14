# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()


class Movie(models.Model):
    douban_id = models.IntegerField(primary_key=True)
    film_name = models.CharField(max_length=100)
    release_date = models.CharField(max_length=100)
    film_length = models.IntegerField()
    area = models.CharField(max_length=30)
    language = models.CharField(max_length=100)
    actors = models.TextField()
    labels = models.CharField(max_length=30)
    douban_rate = models.FloatField()
    douban_comment_num = models.IntegerField()
    detail_info = models.TextField()
    img_name = models.CharField(max_length=15)
    year = models.IntegerField()

    def __unicode__(self):
        return self.film_name


class Love(models.Model):
    user = models.ForeignKey(User)
    movie = models.ForeignKey(Movie)
    type = models.CharField(max_length=255)

    def __unicode__(self):
        return self.user.username + '-' + self.movie.film_name + '-' + self.type


class Comment(models.Model):
    user = models.ForeignKey(User)
    movie = models.ForeignKey(Movie)
    comment = models.CharField(max_length=255, blank=True)
    comment_date = models.DateField(blank=True, auto_now=True)
    like = models.IntegerField(default=0)
    unlike = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class ExtUser(models.Model):
    user = models.OneToOneField(User)
    number = models.IntegerField(primary_key=True)
    sex = models.CharField(max_length=2, blank=True, null=True)
    autograph = models.CharField(max_length=50, blank=True, null=True)
    greet = models.CharField(max_length=50, blank=True, null=True)
    labels = models.CharField(max_length=50, blank=True, null=True)
    register_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.user.username

