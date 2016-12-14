from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import re


class LoginForm(forms.Form):
    username = forms.CharField(label='user name', max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField(label='password', max_length=25, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'password'}))


class RegistForm(forms.Form):
    username = forms.CharField(label='user name', max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'username'}))
    email = forms.CharField(label='e-mail', required=False,
                             widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email address'}))
    password = forms.CharField(label='password', max_length=25,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))
    confirmPassword = forms.CharField(label='confirm password', max_length=25,
                                      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'confirm password'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Username can only contains number, letter , _ and space")
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            return username
        else:
            raise forms.ValidationError("username already exist")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email = email)
        except ObjectDoesNotExist:
            return email
        else:
            raise forms.ValidationError("this e-mail is already in use")

    def clean_confirmPassword(self):
        if self.cleaned_data['password']:
            confirmPassword = self.cleaned_data['confirmPassword']
            password = self.cleaned_data['password']
            if confirmPassword == password:
                return confirmPassword
        raise forms.ValidationError("password does not match")

