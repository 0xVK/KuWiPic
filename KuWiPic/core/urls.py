from django.conf.urls import url, include
from .views import log_out, SignIn, profile, create_alb, alb_show, alb_edit, delete_album, sign_up, show_users

urlpatterns = [

    url(r'^signin/$', SignIn.as_view(), name='sign_in'),
    url(r'^signup/$', sign_up, name='reg'),
    url(r'^logout/$', log_out, name='logout'),
    url(r'^users/$', show_users, name='users'),
    url(r'^a/create_alb/$', create_alb, name='create_album'),
    url(r'^a/(?P<al_slug>[-\w]+)/$', alb_show, name='album_show'),
    url(r'^a/(?P<al_slug>[-\w]+)/edit/$', alb_edit, name='album_edit'),
    url(r'^a/(?P<al_slug>[-\w]+)/del/$', delete_album, name='album_delete'),
    url(r'^u/(?P<username>[-\w]+)/$', profile, name='profile'),
]


