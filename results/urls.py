from django.conf.urls import url

from . import views

app_name = 'results'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^vote/$', views.vote, name='vote'),
    url(r'^outcome/$', views.outcome, name='outcome')
]
