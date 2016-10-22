from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect, HttpResponse


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


def profile(request):

    return HttpResponse('Hello ' + request.user.username)


