from django.conf.urls import url

from . import views

app_name = 'results'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^vote/$', views.vote, name='vote'),
    url(r'^vote_script/$', views.vote_script, name='vote_script'),
    url(r'^delete_votes/$', views.delete_votes, name='delete_votes'),
    url(r'^outcome/$', views.outcome, name='outcome')
]
