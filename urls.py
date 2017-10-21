from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
)

urlpatterns = [
    url(r'^$', post_list, name='post_list'),
    url(r'^create/$', post_create),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^update/$', post_update),
    url(r'^delete/$', post_delete),

]