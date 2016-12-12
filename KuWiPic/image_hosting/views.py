# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden
from image_hosting.models import Image as Image_model, Album
from .models import Comment
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
import string
import random


def upload_image(request):

    if request.method == 'POST':

        saved_img = save_image(request.FILES.get('img'))
        if saved_img:
            return redirect(saved_img)
        else:
            return HttpResponse('image type error')

    else:
        return render(request, 'image_hosting/index.html')


def show_image(request, slug):

    img = get_object_or_404(Image_model, slug=slug)

    if (img.album and img.album.private_policy == 'Private') and not request.user.has_perm('image_hosting.album_owner', img.album):
        return HttpResponseForbidden('Http Response Forbidden for show')

    else:
        img.views += 1
        img.save()
        img_size = round(img.image.size / 1024, 1)
        comments = Comment.objects.filter(image=img)

        data = {'image': img, 'img_size': img_size, 'comments': comments}
        return render(request, 'image_hosting/picture.html', context=data)


def last_images(request):

    ims = Image_model.objects.get_latest(to=15)

    return render(request, 'image_hosting/last.html', {'images': ims})


def about(request):

    count_users = User.objects.all().count()
    count_albums = Album.objects.all().count()
    count_images = Image_model.objects.all().count()

    data = {
        'count_users': count_users,
        'count_albums': count_albums,
        'count_images': count_images,
    }

    return render(request, 'image_hosting/about.html', data)


def save_image(img, alb=None):

    import imghdr

    # try:
    #     uploaded_img = img
    #     uploaded_img_ext = uploaded_img.name.split('.')[1].lower()
    #     valid_extensions = ['gif', 'png', 'jpg', 'jpeg', 'bmp']
    #
    #     if uploaded_img_ext not in valid_extensions:
    #         return None
    #
    #     else:
    #         random_slug = get_random_slug(Image_model)
    #         im = Image_model(image=uploaded_img, slug=random_slug, album=alb)
    #         im.save()
    #         return im

    try:
        if imghdr.what(img):
            random_slug = get_random_slug(Image_model)
            im = Image_model(image=img, slug=random_slug, album=alb)
            im.save()
            return im
        else:
            return None

    except Exception as e:

        print(e)
        return HttpResponseServerError('server error(', str(e))


def get_random_slug(model):

    while(True):

        rand_slug = ''.join(random.choice(string.ascii_lowercase +
                                          string.ascii_uppercase +
                                          string.digits)
                          for x in range(4))

        if not model.objects.filter(slug=rand_slug).exists():
            return rand_slug


def comment_image(request, slug):

    if request.method == 'POST':
        img = get_object_or_404(Image_model, slug=slug)
        comment_text = request.POST.get('comment_text')
        print(comment_text)
        Comment(text=comment_text, user=request.user, image=img).save()

        return redirect(img)

