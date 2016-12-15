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
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
    email = forms.CharField(label='e-mail', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email address'}))
    password = forms.CharField(label='password', max_length=25,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))
    confirmPassword = forms.CharField(label='confirm password', max_length=25,
                                      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'confirm password'}))
    drink_level = forms.ChoiceField(widget=forms.Select, choices=[('0', 'abstemious'), ('1', 'social drinker'), ('2', 'casual drinker')])
    smoker = forms.ChoiceField(widget=forms.RadioSelect, choices=[('0', 'FALSE'), ('1', 'TRUE')])
    age = forms.IntegerField(label='age', widget=forms.NumberInput)
    marital_status = forms.ChoiceField(widget=forms.RadioSelect, choices=[('0', 'single'), ('1', 'married'), ('2', 'widow')])
    hijos = forms.ChoiceField(widget=forms.RadioSelect, choices=[('0', 'independent'), ('1', 'kids'), ('2', 'dependent')])
    interest = forms.ChoiceField(widget=forms.RadioSelect, choices=[('0', 'variety'), ('1', 'technology'),
                                          ('2', 'none'), ('3', 'retro'), ('4', 'eco-friendly')])
    personality = forms.ChoiceField(widget=forms.RadioSelect, choices=[('0', 'thrifty-protector'), ('1', 'hunter-ostentatious'),
                                             ('2', 'hard-worker'), ('3', 'conformist')])
    religion = forms.ChoiceField(widget=forms.RadioSelect, choices=[('0', 'none'), ('1', 'Catholic'),
                                          ('2', 'Christian'), ('3', 'Mormon'), ('4', 'Jewish')])
    activity = forms.ChoiceField(widget=forms.RadioSelect, choices=[('0', 'student'), ('1', 'professional'),
                                          ('2', 'unemployed'), ('3', 'working-class')])

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

