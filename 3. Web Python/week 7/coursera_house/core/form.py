from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


class ControllerForm(forms.Form):
    bedroom_target_temperature = forms.IntegerField(
    	required=False, 
    	validators =[MaxValueValidator(50), MinValueValidator(16)]
    	)
    hot_water_target_temperature = forms.IntegerField(
    	required=False,
    	validators =[MaxValueValidator(90), MinValueValidator(24)]
    	)
    bedroom_light = forms.BooleanField(required=False)
    bathroom_light = forms.BooleanField(required=False)
