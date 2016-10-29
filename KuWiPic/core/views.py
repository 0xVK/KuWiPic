# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from core.forms import FilterSortingInProfileForm, CreateAlbumForm, AddImagesToAlbumForm, EditAlbumForm
from image_hosting.models import Album, Image


class SignIn(FormView):

    form_class = AuthenticationForm
    template_name = 'core/signin.html'
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(SignIn, self).form_valid(form)


def log_out(request):

    logout(request)
    return HttpResponseRedirect('/')


def profile(request, username):

    u = get_object_or_404(User, username=username)
    is_page_ow = request.user == u

    if request.method == 'GET':

        add_ims_to_alb_fm = AddImagesToAlbumForm()
        create_albm_fm = CreateAlbumForm()

        filter_sort_fm = FilterSortingInProfileForm(u, request.GET)

        if filter_sort_fm.is_valid():

            filter_album_id = filter_sort_fm.cleaned_data['filter_albums']
            if filter_album_id:
                albms = Album.objects.filter(owner=request.user, id=filter_album_id)
            else:
                albms = Album.objects.filter(owner=request.user)

        else:
            albms = Album.objects.filter(owner=request.user)

        ims = []
        for alb in albms:
            ims += alb.images_in_album.all()


        data = {
            'FilterSortForm': filter_sort_fm,
            'AddImsToAlbForm': add_ims_to_alb_fm,
            'CreateAlbmFm': create_albm_fm,
            'images': ims,
            'albums': albms,
            'is_page_owner': is_page_ow
                }

    return render(request, template_name='core/profile.html', context=data)


def create_alb(request):

    if request.method == 'POST':
        CreateAlbmFm = CreateAlbumForm(request.POST)

        if CreateAlbmFm.is_valid():
            name = CreateAlbmFm.cleaned_data['name']
            owner = request.user
            private_policy = CreateAlbmFm.cleaned_data['private_policy']

            al = Album.objects.create(name=name, owner=owner, private_policy=private_policy)
            al.save()

            return redirect(al)
        else:
            return HttpResponseBadRequest('Errors:' + str(CreateAlbmFm.errors))

    else:
        return HttpResponseBadRequest('invalid method(GET)')


def alb_show(request, a_id):

    al = get_object_or_404(Album, id=a_id)
    ims = al.images_in_album.all()

    data = {
        'album': al,
        'images': ims,
    }

    return render(request, 'core/album.html', data)


def alb_edit(request, a_id):

    if request.method == 'GET':

        al = get_object_or_404(Album, id=a_id)
        ims = al.images_in_album.all()

        edit_alb_fm = EditAlbumForm(instance=al)

        data = {
            'album': al,
            'images': ims,
            'EditAlbFm': edit_alb_fm,
        }

        return render(request, 'core/album_edit.html', data)