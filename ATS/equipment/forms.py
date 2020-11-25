#https://www.pluralsight.com/guides/work-with-ajax-django

from .models import Model
from django import forms
import datetime

class ModelsForm(forms.ModelForm):
    class Meta:
        model= Model
        fields= ["photo", "model"]

class EquipmentForm(forms.ModelForm):
    ## change the widget of the date field.
    dob = forms.DateField(
        label='What is your birth date?', 
        # change the range of the years from 1980 to currentYear - 5
        widget=forms.SelectDateWidget(years=range(1980, datetime.date.today().year-5))
    )
    
    def __init__(self, *args, **kwargs):
        super(EquipmentForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Model
        fields = '__all__'
        
