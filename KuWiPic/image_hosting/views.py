# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from image_hosting.models import Image as Image_model
from django.conf import settings as django_settings
import os
import string
import random
from PIL import Image
import datetime
from django.core.files import File


def index(request):
    return HttpResponseRedirect('/i/')


def upload_image(request):

    if request.method == 'POST':

        return redirect(save_image(request.FILES.get('img')))

    else:
        return render(request, 'image_hosting/index.html')


def show_image(request, slug):

    img = get_object_or_404(Image_model, slug=slug)
    img.views += 1
    img.save()
    img_size = round(img.image.size / 1024, 1)
    return render(request, 'image_hosting/picture.html', context={'image': img, 'img_size': img_size})


def last_images(request):

    ims = Image_model.objects.get_latest(to=15)
    return render(request, 'image_hosting/last.html', {'images': ims})


def about(request):
    return render(request, 'image_hosting/about.html')


def save_image(img, alb=None):

    try:
        uploaded_img = img
        uploaded_img_ext = uploaded_img.name.split('.')[1]
        uploaded_img_ext = uploaded_img_ext.lower()
        valid_extensions = ['gif', 'png', 'jpg', 'jpeg', 'bmp']

        if uploaded_img_ext not in valid_extensions:
            return HttpResponse('invalid file extension!')

        random_slug = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase +

                                            string.digits) for x in range(4))  # random generate slug

        im = Image_model(image=uploaded_img, slug=random_slug, album=alb)
        im.save()

        return im

    except Exception as e:

        print(e)
        return HttpResponseServerError('server error(', str(e))
