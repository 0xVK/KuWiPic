from django.conf.urls import url
from image_hosting.views import upload_image, show_image, last_images


urlpatterns = [
    url(r'^$', upload_image),
    url(r'^last/', last_images),
    url(r'(?P<slug>[-\w]+)/$', show_image),

]
