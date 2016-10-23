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


