from django.shortcuts import render
from forms.usrForms import LoginForm, RegistForm
from django.http import HttpResponseRedirect, HttpResponse


def getMainPage(request):
    return render(request, 'index.html', locals())

def register(request):
    if request.method == "POST":
        pass
    else:
        register_form = RegistForm()
    return render(request, 'signup.html', locals())


def sign(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            userData = login_form.cleaned_data
            print(userData['password'])
        return HttpResponseRedirect('/index/')
    else:
        login_form = LoginForm()
    return render(request, 'signin.html', locals())
