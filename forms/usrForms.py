from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='user name', max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField(label='password', max_length=25, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'password'}))

