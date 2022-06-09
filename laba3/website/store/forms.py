from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import re
from django.core import validators, exceptions
from django.core.exceptions import ValidationError


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


class CheckoutForm(forms.Form):
    firstname = forms.CharField(label='First name', widget=forms.TextInput(attrs={'class': 'checkout_input'}))
    lastname = forms.CharField(label='Last name', widget=forms.TextInput(attrs={'class': 'checkout_input'}))
    address = forms.CharField(label="Address", widget=forms.TextInput(attrs={'class': 'checkout_input'}))
    phone = forms.CharField(label='Phone No', widget=forms.TextInput(attrs={'class': 'checkout_input'}))
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'checkout_input'}))

    class Meta:
        fields = [
            'firstname',
            'lastname',
            'address',
            'phone',
            'email',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, email):
            return email
        else:
            raise forms.ValidationError("Invalid email")

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if re.match(r"[\d]{2}[\d]{2}[\d]{2}[\d]{3}", phone):
            return phone
        else:
            raise forms.ValidationError("Phone should be like this : 291234567")

    def clean_firstname(self):
        firstname = self.cleaned_data['firstname']
        if re.search(r'^[A-z][A-z|\.|\s]+$', firstname) is None:
            raise forms.ValidationError("Wrong name")
        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data['lastname']
        if re.search(r'^[A-z][A-z|\.|\s]+$', lastname) is None:
            raise forms.ValidationError("Wrong lastname")
        return lastname


class ProductForm(forms.ModelForm):
    size = forms.CharField(widget=forms.RadioSelect)
