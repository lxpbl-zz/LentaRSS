from django import forms
from rss_app.models import Category


def get_categories():
    cats = Category.objects.all()
    return tuple(map(lambda x: (x.id, x.name), cats))


class GetNewsForm(forms.Form):
    cats_choices = get_categories()
    cats_init = (x[0] for x in cats_choices)

    email = forms.EmailField(label='',
                             widget=forms.TextInput(attrs={
                                 'placeholder': 'E-mail получателя',
                                 'class': 'text-center'
                             }))
    date_beg = forms.DateField(label='',
                               widget=forms.DateInput(attrs={
                                   'placeholder': 'Начальная дата',
                                   'class': 'datepicker text-center'
                               }))
    date_end = forms.DateField(label='',
                               widget=forms.DateInput(attrs={
                                   'placeholder': 'Конечная дата',
                                   'class': 'datepicker text-center'
                               }))
    cats = forms.MultipleChoiceField(label='',
                                     choices=cats_choices,
                                     initial=cats_init,
                                     widget=forms.SelectMultiple(attrs={
                                         'size': '15'
                                     }))
