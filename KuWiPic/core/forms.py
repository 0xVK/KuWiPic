# -*- coding: utf-8 -*-

from django import forms
from image_hosting.models import Album
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class FilterSortingInProfileForm(forms.Form):

    filter_albums = forms.ChoiceField(required=False)
    # sort_by = forms.ChoiceField(choices=(('upload_date', 'Час'), ('views', 'Перегляди')), required=False)

    def __init__(self, usr, *args, **kwargs):

        super(FilterSortingInProfileForm, self).__init__(*args, **kwargs)
        chs = [(al.id, al.name) for al in Album.objects.filter(owner=usr)]
        chs = [('', 'Всі')] + chs
        self.fields['filter_albums'] = forms.ChoiceField(choices=chs, required=False)


class AddImagesToAlbumForm(forms.Form):

    images = forms.ImageField()
    to_album = forms.ChoiceField()


class CreateAlbumForm(forms.ModelForm):

    PRIVATE = 'Private'
    PUBLIC = 'Public'
    UNLISTED = 'Unlisted'
    PRIVACY_TYPES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (UNLISTED, 'Unlisted'))

    name = forms.CharField(max_length=25, label='Ім`я')
    private_policy = forms.ChoiceField(choices=PRIVACY_TYPES, label='Тип')

    class Meta:
        model = Album
        fields = ['name', 'private_policy']


class EditAlbumForm(forms.ModelForm):

    PRIVATE = 'Private'
    PUBLIC = 'Public'
    UNLISTED = 'Unlisted'
    PRIVACY_TYPES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (UNLISTED, 'Unlisted'))
    name = forms.CharField(max_length=25, label='Ім`я', required=False)
    private_policy = forms.ChoiceField(choices=PRIVACY_TYPES, label='Тип')
    images = forms.ImageField(required=False)

    class Meta:
        model = Album
        fields = ['name', 'private_policy', 'images']


class SignUpForm(forms.ModelForm):

    username = forms.CharField(max_length=30, required=True)

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(forbidden_usernames_validator)
        self.fields['username'].validators.append(invalid_username_validator)
        self.fields['username'].validators.append(unique_username_ignore_case_validator)

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(
                ['Паролі не співпадають'])
        return self.cleaned_data


def forbidden_usernames_validator(value):
    forbidden_usernames = ['admin', 'settings', 'about', 'help']

    if value.lower() in forbidden_usernames:
        raise ValidationError(u'Це зарезервоване слово')


def invalid_username_validator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError(u'Введіть коректний логін')


def unique_username_ignore_case_validator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError(u'Користувач з таким логіном уже існує')