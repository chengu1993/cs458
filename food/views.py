from django.shortcuts import render
from forms.usrForms import LoginForm
from django.http import HttpResponseRedirect, HttpResponse


def getMainPage(request):
    return render(request, 'index.html', locals())


def sign(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            userData = login_form.cleaned_data
        return HttpResponseRedirect('/index/')
    else:
        login_form = LoginForm()
    return render(request, 'signin.html', locals())
