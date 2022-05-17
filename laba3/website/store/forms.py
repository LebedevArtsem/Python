from django import forms
from .models import User


class NewUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'password']
