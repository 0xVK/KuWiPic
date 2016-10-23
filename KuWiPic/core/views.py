from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from core.forms import FilterSortingInProfileForm
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

    if request.method == 'GET':
        FilterSortForm = FilterSortingInProfileForm(u, request.GET)

        if FilterSortForm.is_valid():

            albms = Album.objects.filter(owner=request.user)

            ims = []
            for alb in albms:
                ims += alb.images_in_album.all()

            data = {
                'FilterSortForm': FilterSortForm,
                'images': ims,
                    }

    return render(request, template_name='core/profile.html', context=data)


