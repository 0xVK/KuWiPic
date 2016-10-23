from django.conf.urls import url, include
from .views import log_out, SignIn, profile

urlpatterns = [

    url(r'signin/$', SignIn.as_view()),
    url(r'logout/$', log_out),
    url(r'u/(?P<username>[-\w]+)/$', profile),
]


