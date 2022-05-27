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


class CheckoutForm(forms.ModelForm):
    firstname = forms.CharField(label='First name', widget=forms.TextInput(attrs={'class': 'checkout_input'}))
    lastname = forms.CharField(label='Last name', widget=forms.TextInput(attrs={'class': 'checkout_input'}))
    address = forms.CharField(label="Address", widget=forms.TextInput(attrs={'class': 'checkout_input'}))
    phone = forms.CharField(label='Phone No', widget=forms.TextInput(attrs={'class': 'checkout_input'}))
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'checkout_input'}))

    class Meta:
        model = User
        fields = [
            'firstname',
            'lastname',
            'address',
            'phone',
            'email',
        ]
