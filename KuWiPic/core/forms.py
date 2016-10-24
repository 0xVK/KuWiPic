# -*- coding: utf-8 -*-

from django import forms
from image_hosting.models import Album


class FilterSortingInProfileForm(forms.Form):

    filter_albums = forms.ChoiceField(required=False)
    sort_by = forms.ChoiceField(choices=(('Time', 'Час'), ('Views', 'Перегляди')), required=False)

    def __init__(self, usr, *args, **kwargs):

        super(FilterSortingInProfileForm, self).__init__(*args, **kwargs)
        chs = [(al.id, al.name) for al in Album.objects.filter(owner=usr)]
        chs = [('999', 'Всі')] + chs
        self.fields['filter_albums'] = forms.ChoiceField(choices=chs, required=False)


class AddImagesToAlbumForm(forms.Form):

    images = forms.ImageField()
    to_album = forms.ChoiceField()


class CreateAlbumForm(forms.ModelForm):

    PRIVATE = 'PRT'
    PUBLIC = 'PBC'
    UNLISTED = 'ULS'
    ACTIVITY_TYPES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (UNLISTED, 'Unlisted'))

    name = forms.CharField(max_length=25, label='Ім`я')
    private_policy = forms.ChoiceField(choices=ACTIVITY_TYPES, label='Тип')

    class Meta:
        model = Album
        fields = ['name', 'private_policy']

