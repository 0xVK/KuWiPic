# -*- coding: utf-8 -*-

from django import forms
from image_hosting.models import Album
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
import re


class FilterSortingInProfileForm(forms.Form):

    filter_albums = forms.ChoiceField(required=False)
    # sort_by = forms.ChoiceField(choices=(('upload_date', 'Час'), ('views', 'Перегляди')), required=False)

    def __init__(self, usr, *args, **kwargs):

        super(FilterSortingInProfileForm, self).__init__(*args, **kwargs)
        chs = [(al.id, al.name) for al in Album.objects.filter(owner=usr)]
        chs = [('', _('Все'))] + chs
        self.fields['filter_albums'] = forms.ChoiceField(choices=chs, required=False,
                                                         widget=forms.Select(attrs={'class': 'form-control'}))


class CreateAlbumForm(forms.ModelForm):

    PRIVATE = 'Private'
    PUBLIC = 'Public'
    UNLISTED = 'Unlisted'
    PRIVACY_TYPES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (UNLISTED, 'Unlisted'))

    name = forms.CharField(max_length=25, label=_('Название'))
    private_policy = forms.ChoiceField(choices=PRIVACY_TYPES, label=_('Тип'),
                                       widget=forms.Select(attrs={'class': 'form-control'}))

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
    name = forms.CharField(max_length=25, label=_('Имя'), required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    private_policy = forms.ChoiceField(choices=PRIVACY_TYPES, label=_('Тип'),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    images = forms.ImageField(required=False)

    class Meta:
        model = Album
        fields = ['name', 'private_policy', 'images']


class SignUpForm(forms.ModelForm):

    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(unique_username_ignore_case_validator)
        self.fields['username'].validators.append(forbidden_usernames_validator)
        self.fields['username'].validators.append(correct_format_validator)

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            self._errors['password'] = self.error_class(
                [_('Пароли не совпадают!')])
        return self.cleaned_data


def forbidden_usernames_validator(value):

    forbidden_usernames = ['admin', ]

    if value.lower() in forbidden_usernames:
        raise ValidationError(_('Это зарезервированное слово'))


def unique_username_ignore_case_validator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError(_('Логин занят'))


def correct_format_validator(value):

    username_validator_regexp = '^[a-zA-Z][a-zA-Z0-9-_]{3,20}$'

    if not re.match(username_validator_regexp, value):
        raise ValidationError(_('Недопустимый формат'))
