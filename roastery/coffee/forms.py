from django import forms

from .models import Roast


class RoastForm(forms.ModelForm):
    class Meta:
        model = Roast
        fields = ["green_bean", "degree", "roast_date"]

    roast_date = forms.DateField(widget=forms.SelectDateWidget())
