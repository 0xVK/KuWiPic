from django.conf.urls import url, i18n
from .views import upload_image, show_image, last_images, comment_image, show_image_comments
from core.views import delete_photo


urlpatterns = (
    url(r'^$', upload_image, name='index'),
    url(r'^last/', last_images, name='last_images'),
    url(r'^i/(?P<slug>[-\w]+)/del/$', delete_photo, name='delete_image'),
    url(r'^i/(?P<slug>[-\w]+)/comment/$', comment_image, name='comment_image'),
    url(r'^i/(?P<slug>[-\w]+)/$', show_image, name='show_image'),
    url(r'^i/(?P<slug>[-\w]+)/getcomments/$', show_image_comments, name='show_image_comments'),

)
