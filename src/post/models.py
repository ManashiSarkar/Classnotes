# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=250,null=False,blank=False)
	content = models.TextField()
	author = models.ForeignKey(User,null=False)
	publish_date = models.DateTimeField(null=True)
	create_time = models.DateTimeField(default=timezone.now)
	stars = models.IntegerField(default=0)
	is_draft = models.BooleanField(default=False)

	def publish(self):
		self.publish_date = timezone.now()
		self.is_draft = False
		self.save()

class Message(models.Model):
	author = models.ForeignKey(User,null=False,related_name='author_name')
	recipient = models.ForeignKey(User,null=False)
	sent_time= models.DateTimeField()
	read_time= models.DateTimeField(null=True)
	content = models.TextField(blank=False,null=False)
	is_read = models.BooleanField(default=False)

ACTIVITY_CHOICES = (
	('c','Commented on'),
	('p','Published'),
	('e','Extended'),
)

class Activity(models.Model):
	activity = models.CharField(max_length=20,null=False,
								choices=ACTIVITY_CHOICES)
	post = models.OneToOneField(Post,null=False)

USER_CHOICES = (
	('beginner','black'),
	('intermediate','purple'),
	('advanced','orange'),
	('master','red'),
)

class State(models.Model):
	user = models.OneToOneField(User,null=False,primary_key=True) # one state for each user
	message_list = models.CharField(max_length=10,default='',blank=True) # cocatenated list of friends' usernames
	user_type = models.CharField(default='beginner',
								choices=USER_CHOICES,
								max_length=10) # color
	user_since = models.DateTimeField(null=True,default=timezone.now)
	followers = models.IntegerField(default=0)
	stars = models.IntegerField(default=0)
	last_activity = models.ForeignKey(Activity,null=True)

class Talks(models.Model):
	person1 = models.ForeignKey(User,null=False,related_name='name1')
	person2 = models.ForeignKey(User,null=False)
	talk = models.ForeignKey(Message,null=False) # latest talk only

class Topics(models.Model):
	name = models.CharField(max_length=20,null=False)
	followers = models.IntegerField(default=0)
	summary = models.CharField(max_length=2000,null=False,default="")
	topContributors = models.ManyToManyField(User)

class Settings(models.Model):
	user = models.OneToOneField(User,null=False,primary_key=True) # one settings for each user
	topics = models.ManyToManyField(Topics)
	
class Comment(models.Model):
	post = models.ForeignKey(Post,null=False)
	author = models.ForeignKey(User,null=False,related_name='commentor_name')
	content = models.CharField(max_length=500,null=False)

@receiver(post_save, sender=User) # new instance, or update
def create_user_profile(sender, **kwargs):
    if kwargs.get('created', False): # 'created' is True when the User instance was there in database before the save()
        State.objects.get_or_create(user=kwargs.get('instance'))
        Settings.objects.get_or_create(user=kwargs.get('instance'))



	



