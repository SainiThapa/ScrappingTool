from django import forms

from .models import Newsheadline, Webportal


class WebportalForm(forms.ModelForm):
    class Meta:
        model=Webportal
        fields=['page_title','page_url']

        