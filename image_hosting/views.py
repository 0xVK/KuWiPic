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

        try:
            uploaded_img = request.FILES.get('img')  # take uploaded picture
            uploaded_img_ext = uploaded_img.name.split('.')[1]

            valid_extensions = ['gif', 'png', 'jpg', 'jpeg', 'bmp']

            if uploaded_img_ext not in valid_extensions:
                return HttpResponse('invalid file extension!')

            random_slug = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase +

                                                string.digits) for x in range(4))  # random generate slug

            im = Image_model(image=uploaded_img, slug=random_slug)
            im.save()

            return redirect(im)

        except Exception as e:

            print(e)
            return HttpResponseServerError('server error(')

        return redirect('/')

    else:
        return render(request, 'image_hosting/index.html')


def show_image(request, slug):

    img = get_object_or_404(Image_model, slug=slug)

    return render(request, 'image_hosting/picture.html', context={'image': img})


def last_images(request):

    ims = Image_model.objects.all().order_by('upload_date')

    return render(request, 'image_hosting/last.html', {'images': ims})


