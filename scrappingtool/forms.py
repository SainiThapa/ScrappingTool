from django import forms
from .models import Webportal, Newsheadline

class WebportalForm(forms.ModelForm):
    class Meta:
        model=Webportal
        fields=['page_title','page_url']

        