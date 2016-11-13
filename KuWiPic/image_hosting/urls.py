from django.conf.urls import url
from image_hosting.views import upload_image, show_image, last_images
from core.views import delete_photo

urlpatterns = [
    url(r'^$', upload_image, name='upload_image'),
    url(r'^last/', last_images, name='last_images'),
    url(r'(?P<slug>[-\w]+)/del/$', delete_photo, name='delete_image'),
    url(r'(?P<slug>[-\w]+)/$', show_image, name='show_image'),

]
