from django.conf.urls import url, include
from .views import log_out, SignIn, profile, create_alb, alb_show, alb_edit, delete_album, sign_up

urlpatterns = [

    url(r'signin/$', SignIn.as_view()),
    url(r'signup/$', sign_up, name='reg'),
    url(r'logout/$', log_out, name='logout'),
    url(r'create_alb/$', create_alb, name='create_album'),
    url(r'a/(?P<a_id>\d+)/$', alb_show, name='album_show'),
    url(r'a/(?P<a_id>\d+)/edit/$', alb_edit, name='album_edit'),
    url(r'a/(?P<a_id>\d+)/del/$', delete_album, name='album_delete'),
    url(r'u/(?P<username>[-\w]+)/$', profile, name='profile'),
]


