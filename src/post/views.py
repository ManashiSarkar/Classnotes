# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import attrgetter
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import time

from .models import Post, Message, State, Talks, Settings, Topics, Comment
from .forms import NewPost, ContactForm, MessageForm, SettingsForm_general, SettingsForm_topics
from .forms import CommentForm
# Create your views here.

def landing_page(request):
	template = None
	if not request.user.is_authenticated():
		template = 'landing-page.html'
	else:
		template = 'landing-page-authenticated.html'

	return render( request, template, {} )

def about(request):
	template = 'about.html'
	return render( request, template, {} )

def contact(request):
	form = ContactForm(request.POST or None)

	if form.is_valid():
		print form.cleaned_data['email']
		name = form.cleaned_data['name']
		comment = form.cleaned_data['comment']
		subject = 'Message from Mysite.com'
		emailFrom = form.cleaned_data['email']
		message = '%s : %s\n\n%s' %( name, emailFrom, comment )
		emailTo = [settings.EMAIL_HOST_USER]
		
		send_mail(subject, message, emailFrom, emailTo, fail_silently=False)
		sent = True

	if request.user.is_authenticated():
		base = 'landing-page-authenticated.html'
	else:
		base = 'landing-page.html'
	context = locals()
	template = 'contact.html'
	return render(request,template,context)

def starter_guide(request):
	template = 'starter-guide.html'
	return render( request, template, {} )

def secret_hash(pk):
	return str(pk)

@login_required
def messages_all(request): # all messages
	# synchronous
	context = []

	all_talks = Talks.objects.filter(person1=request.user) | Talks.objects.filter(person2=request.user).exclude(person1=request.user)

	for message in all_talks:
		message.talk.pk = secret_hash( message.talk.pk )
		context.append( message.talk )

	context = sorted( context, key=attrgetter('sent_time'), reverse=True )

	try:
		state = request.user.state
	except ObjectDoesNotExist:
		state = State(user=request.user)

	state.message_list = ''
	state.save()

	return render( request, 'message.html', {'talks':context} )

@login_required
def messages_with(request,friend): # message_with
	# synchronous
	try:
		buddy = User.objects.get(username=friend)
	except:
		return redirect('landing_page')

	if request.POST:
		form = MessageForm(request.POST or None)

		# save message in database
		if form.is_valid():
			print 'form is valid'
			message = form.save(commit=False)
			message.author = request.user
			message.recipient = buddy
			message.sent_time = timezone.now()
			message.read_time = None
			message.is_read = False
			message.save()

			# mark new message for recipient
			try:
				message_list = message.recipient.state.message_list
			except ObjectDoesNotExist:
				message_list = State(user=message.recipient).message_list

			message_list = 'yes'
			#message_list += request.user.username[:20] + ' '
			message.recipient.state.message_list = message_list
			message.recipient.state.save()

			talk = Talks.objects.filter(person1=request.user,person2=buddy) | Talks.objects.filter(person2=request.user,person1=buddy)
			if not talk:
				talk = Talks.objects.create(person1=request.user,person2=buddy,talk=message)
			else:
				talk[0].talk = message
				talk[0].save();

			talk = Talks.objects.filter(person1=request.user,person2=buddy) | Talks.objects.filter(person2=request.user,person1=buddy)
			
	# asynchronously return all talks with friend
	talks = sorted( Message.objects.filter(author=request.user).filter(recipient=buddy) |
					Message.objects.filter(recipient=request.user).filter(author=buddy).exclude(author=request.user), 
					key=attrgetter('sent_time'), reverse=True )[:30]

	# ways to use less load content : slicing [:30]->first 30 objects, [5:10]->5th to 10th, django-endless-pagination

	for message in talks:
		message.pk = secret_hash( message.pk )

	form = MessageForm()

	return render( request, 'messages-with.html', {'talks':talks,'form':form} )

@login_required
def async_messages(request): # new messages
	user = request.user

	if request.POST:
		try:
			if request.POST['username'] != user.username:
				talk = Message.objects.get(pk=request.POST['id'])
				print 'after post ' + talk.content

				if not talk.is_read:
					# un-strong Messages in navbar, if at least one new message is seen
					try:
						state = user.state
					except ObjectDoesNotExist:
						state = State(user=user)
					state.message_list = ''
					state.save()

					# set read_time
					talk.is_read = True
					talk.read_time = timezone.now()
					talk.save()
			print 'pop'
			return JsonResponse( {} ) # 'redirect':'/'

		except:
			# if request.POST['redirect']:
			print request.POST['child3']
			print request.POST['child5']
			if user.username == request.POST['child3']:
				return JsonResponse( {'redirect':request.POST['child5']} )
			else:
				return JsonResponse( {'redirect':request.POST['child3']} )
	
	else: # to strengthen Messages in navbar
		print 'are we here?'
		try:
			state = user.state
		except ObjectDoesNotExist:
			state = State(user=user)

		new_message = state.message_list

		return JsonResponse( {'new_message':new_message} )

'''
@login_required
def async_notifications(request):
	user = request.user

	try:
		state = user.state
	except ObjectDoesNotExist:
		state = State(user=user)

	notifs = Notification.objects.all().order_by('-create_time')[:6]

	return JsonResponse( {'notifs':notifs} )
'''



def post_redirect(request,post_id):
	# prevents form resubmission on commenting

	template = 'post.html'
	try:
		post = Post.objects.get(id=post_id)
	except:
		post = none

	comments = Comment.objects.filter(post=post)

	form = CommentForm()

	context = locals()

	# return render( request, template, context )
	return redirect('post',post_id)


def post(request,post_id):
	template = 'post.html'
	try:
		post = Post.objects.get(id=post_id)
	except:
		post = none

	if request.POST:
		form = CommentForm(request.POST)
		if form.is_valid():
			Comment.objects.create(post=post,author=request.user,content=form.cleaned_data['content'])

		return redirect('post_redirect',post_id)

	comments = Comment.objects.filter(post=post)

	form = CommentForm()

	context = locals()

	return render( request, template, context )


@login_required
def post_edit(request,post_id):
	user = request.user

	if request.POST:
		form = NewPost(request.POST)
		updated = False
		if form.is_valid():
			with transaction.atomic():
				Post.objects.get(pk=post_id).delete()
				# if we don't delete, rich text just keeps adding html tags around textarea. 
				# So we get textarea within textarea, and so on, because content is actually textarea,
				# and form adds textarea tag around this textarea. see page source on browser
				post = form.save(commit=False)
				post.author = request.user
				post.is_draft = True
				post.pk = post_id
				post.save()
				updated = True
		
		return render( request, 'post-edit.html', {'form':form,'updated':updated} )	

	post = Post.objects.get(pk=post_id)
	form = NewPost(instance=post)
	return render( request, 'post-edit.html', {'form':form} )	


@login_required
def new_post(request):
	template = 'new-post.html'

	if request.POST:
		form = NewPost(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.is_draft = True
			post.create_time = timezone.now()
			post.save()
			print post.pk
			pk = post.pk
			return redirect( 'post', post_id=pk )

	form = NewPost()

	return render( request, template, {'form':form} )

def profile(request,username):
	profile = User.objects.get(username=username)
	#profile.state.user_type = 'purple' # purple

	posts = Post.objects.filter(author=profile).order_by('-create_time')
	return render( request, 'profile.html', {'profile':profile,'posts':posts} )

def async_profile(request):
	pass

@login_required
def settings(request):
	# prepopulates the form

	try:
		settings = Settings.objects.get(user=request.user)
	except ObjectDoesNotExist:
		settings = Settings.objects.create(user=request.user)

	generalForm = SettingsForm_general(instance=settings.user)
	# imageForm
	# aboutMeForm
	topicsForm = SettingsForm_topics()

	# get all topics followed by user
	topicsFollowing = settings.topics.all()

	context = locals()

	return render( request, 'settings.html', context )	


@login_required
def general_form(request):

	try:
		settings = Settings.objects.get(user=request.user)
	except ObjectDoesNotExist:
		settings = Settings.objects.create(user=request.user)

	if request.POST:
		form = SettingsForm_general(request.POST)
		if form.is_valid():
			settings.user.first_name = form.cleaned_data['first_name']
			settings.user.last_name = form.cleaned_data['last_name']
			settings.user.save()
			settings.save()

	return redirect( 'settings' )

@login_required
def topics_form(request):

	try:
		settings = Settings.objects.get(user=request.user)
	except ObjectDoesNotExist:
		settings = Settings.objects.create(user=request.user)

	if request.POST:
		form = SettingsForm_topics(request.POST)
		if form.is_valid():
			topic, created = Topics.objects.get_or_create(name=form.cleaned_data['topic'])
			settings.topics.add( topic )
			settings.save()

	return redirect( 'settings' )

def topic(request,topic_slug):
	pass



