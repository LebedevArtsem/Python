from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Name', widget=forms.TextInput())
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
        ]


class SignInForm(AuthenticationForm):
    username = forms.CharField(label='Name', widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
