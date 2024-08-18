#https://www.pluralsight.com/guides/work-with-ajax-django

from .models import Model
from django import forms
import datetime

class ModelsForm(forms.ModelForm):
    class Meta:
        model= Model
        fields = ('description', 'image')
        widgets = {'description': forms.HiddenInput()} 