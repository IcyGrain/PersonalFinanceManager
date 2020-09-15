from django import forms
from .models import *


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = "__all__"
