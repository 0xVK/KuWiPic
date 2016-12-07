# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from guardian.shortcuts import assign_perm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.models import User
from core.forms import FilterSortingInProfileForm, CreateAlbumForm, AddImagesToAlbumForm, EditAlbumForm, SignUpForm
from image_hosting.models import Album, Image
from image_hosting.views import save_image
import datetime
from image_hosting.views import get_random_slug


class SignIn(FormView):

    form_class = AuthenticationForm
    template_name = 'core/signin.html'
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(SignIn, self).form_valid(form)


def sign_up(request):

    if request.method == 'GET':
        sign_up_fm = SignUpForm()
        return render(request, 'core/signup.html', {'form': sign_up_fm})

    if request.method == 'POST':

        sign_up_fm = SignUpForm(request.POST)

        if sign_up_fm.is_valid():

            username = sign_up_fm.cleaned_data.get('username')
            password = sign_up_fm.cleaned_data.get('password')

            User.objects.create_user(username=username, password=password)
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('/')

        else:
            return render(request, 'core/signup.html', {'form': sign_up_fm})


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
                albms = Album.objects.filter(owner=u, id=filter_album_id)
            else:
                albms = Album.objects.filter(owner=u)

        else:
            albms = Album.objects.filter(owner=u)

        ims = []
        ims_for_guest = []
        for alb in albms:
            ims += alb.images_in_album.all()
            if alb.private_policy == 'Public':
                ims_for_guest += alb.images_in_album.all()

        all_albms = Album.objects.filter(owner=u)
        all_albms_for_guest = []

        for a in all_albms:
            if a.private_policy == 'Public':
                all_albms_for_guest.append(a)

        data = {
            'FilterSortForm': filter_sort_fm,
            'AddImsToAlbForm': add_ims_to_alb_fm,
            'CreateAlbmFm': create_albm_fm,
            'images': ims,
            'albums': all_albms,
            'is_page_owner': is_page_ow,
            'images_count': len(ims),
            'all_albms_for_guest': all_albms_for_guest,
            'images_for_guest': ims_for_guest,
            'images_for_guest_count': len(ims_for_guest),
            'user': u,
                }

    return render(request, template_name='core/profile.html', context=data)


def create_alb(request):

    if request.method == 'POST':
        CreateAlbmFm = CreateAlbumForm(request.POST)

        if CreateAlbmFm.is_valid():
            name = CreateAlbmFm.cleaned_data['name']
            owner = request.user
            private_policy = CreateAlbmFm.cleaned_data['private_policy']
            random_slug = get_random_slug(Album)
            al = Album.objects.create(name=name, owner=owner, private_policy=private_policy, slug=random_slug)
            al.save()

            assign_perm('image_hosting.album_owner', request.user, al)

            return redirect(al)
        else:
            return HttpResponseBadRequest('Errors:' + str(CreateAlbmFm.errors))

    else:
        return HttpResponseBadRequest('invalid method(GET)')


def alb_show(request, al_slug):

    al = get_object_or_404(Album, slug=al_slug)

    is_alb_owner = al.owner == request.user

    if al.private_policy == 'Private' and not request.user.has_perm('image_hosting.album_owner', al):
        return HttpResponseForbidden('Http Response Forbidden for alb show')

    else:

        ims = al.images_in_album.all()

        data = {
            'album': al,
            'images': ims,
            'is_alb_owner': is_alb_owner,
        }

        return render(request, 'core/album.html', data)


def alb_edit(request, al_slug):

    al = get_object_or_404(Album, slug=al_slug)
    ims = al.images_in_album.all()

    if not request.user.has_perm('image_hosting.album_owner', al):
        return HttpResponseForbidden('Http Response Forbidden for edit')

    else:
        if request.method == 'GET':

            edit_alb_fm = EditAlbumForm(instance=al)

            data = {
                'album': al,
                'images': ims,
                'EditAlbFm': edit_alb_fm,
            }

        if request.method == 'POST':

            edit_alb_fm = EditAlbumForm(request.POST, request.FILES)

            data = {
                'album': al,
                'images': ims,
                'EditAlbFm': edit_alb_fm,
            }

            if edit_alb_fm.is_valid():
                al = Album.objects.get(slug=al_slug)
                ow = request.user
                if edit_alb_fm.cleaned_data['name']:
                    al.name = edit_alb_fm.cleaned_data['name']
                if edit_alb_fm.cleaned_data['private_policy']:
                    al.private_policy = edit_alb_fm.cleaned_data['private_policy']
                if edit_alb_fm.cleaned_data['images']:
                    im = edit_alb_fm.cleaned_data['images']
                    save_image(im, al)

                al.edit_date = datetime.datetime.now()
                al.save()
                return redirect(al)
            else:
                return HttpResponse(str(edit_alb_fm.errors))

        return render(request, 'core/album_edit.html', data)


def delete_photo(request, slug):

    im = get_object_or_404(Image, slug=slug)

    if not request.user.has_perm('image_hosting.album_owner', im.album):
        return HttpResponseForbidden('Http Response Forbidden for delete photo')
    else:
        im.delete()
        print(request.path)
        return redirect('/a/{}/edit'.format(im.album.slug))


def delete_album(request, al_slug):

    al = get_object_or_404(Album, slug=al_slug)

    if not request.user.has_perm('image_hosting.album_owner', al):
        return HttpResponseForbidden('Http Response Forbidden for delete album')
    else:
        al.delete()
        return redirect('/u/{}'.format(request.user.username))


def show_users(request):

    users = User.objects.all()

    return render(request, 'core/users.html', {'users': users})