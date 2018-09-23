# -*- encoding:utf8 -*-

__author__ = 'luke'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^index/$', views.index, name='index'),
    url(r'^contact/$', views.user_contact_list, name='user_contact_list'),
    url(r'^inbox/(?P<contact_id>\d+)/$', views.user_inbox, name='user_inbox'),
    url(r'^send_message/$', views.send_message, name='send_message'),
    url(r'^delete/contact/$', views.delete_contact, name='delete_contact'),
    url(r'^delete/message/$', views.delete_message, name='delete_message'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),

]
