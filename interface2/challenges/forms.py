from django import forms

from .models import Challenge

class FlagForm(forms.Form):
    flag = forms.CharField(label='Flag', max_length=256)
