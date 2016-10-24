from django.conf.urls import url, include
from .views import log_out, SignIn, profile, create_alb, alb

urlpatterns = [

    url(r'signin/$', SignIn.as_view()),
    url(r'logout/$', log_out),
    url(r'create_alb/$', create_alb),
    url(r'a/(?P<a_id>\d+)/', alb),
    url(r'u/(?P<username>[-\w]+)/$', profile),
]


