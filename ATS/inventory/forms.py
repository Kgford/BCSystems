#https://www.pluralsight.com/guides/work-with-ajax-django

from .models import Inventory
from django import forms

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('serial_number', 'image')
        widgets = {'serial_number': forms.HiddenInput()}
        
