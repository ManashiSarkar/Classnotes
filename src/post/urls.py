from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.landing_page, name='landing_page'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^starter_guide/$', views.starter_guide, name='starter_guide'),

    url(r'^messages/$', views.messages_all, name='messages_all'),
    url(r'^messages/with/(?P<friend>[\w]+)/$', views.messages_with, name='messages_with'),
    url(r'^async_messages/$', views.async_messages, name='async_messages'),

    url(r'^post/new/$', views.new_post, name='new_post'),
    url(r'^post/(?P<post_id>[\d]+)/$', views.post, name='post'),
    url(r'^post_redirect/(?P<post_id>[\d]+)/$', views.post_redirect, name='post_redirect'),
    url(r'^post/(?P<post_id>[\d]+)/edit/$', views.post_edit, name='post_edit'),
    
    url(r'^profile/(?P<username>[\w]+)/$', views.profile, name='profile'),
    url(r'^topic/(?P<username>[\w]+)/$', views.topic, name='topic'),

    url(r'^settings/$', views.settings, name='settings'),
    url(r'^general_form/$', views.general_form, name='general_form'),
    url(r'^topics_form/$', views.topics_form, name='topics_form'),
]

'''
    url(r'^async_notifications/$', views.async_notifications, name='async_notifications'),    
    
    
'''