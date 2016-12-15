from django.shortcuts import render
from forms.usrForms import LoginForm, RegistForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, Group
from food.models import ExtraInfo, Geoplace, Hours, Parking, Cuisine
from django.contrib.auth import authenticate, login, logout
import datetime


def getMainPage(request):
    if not request.user.is_authenticated():
        restaurants = Geoplace.objects.all()
        recent = restaurants[0:15]
        for res in recent:
            res.price = getBudgetSymbol(res.price)
    else:
        # TODO: replace this part with the result of clustering
        restaurants = Geoplace.objects.all()
        recent = restaurants[0:15]
        for res in recent:
            res.price = getBudgetSymbol(res.price)
    return render(request, 'index.html', locals())


def register(request):
    if request.method == "POST":
        register_form = RegistForm(request.POST)
        if register_form.is_valid():
            userInfo = register_form.cleaned_data
            user = User.objects.create_user(
                username=userInfo['username'],
                password=userInfo['password'],
                email=userInfo.get('email', 'noreply@example.com'),
                first_name=userInfo.get('first_name', 'default_first_name'),
                last_name=userInfo.get('last_name', 'default_last_name'),
            )
            now = datetime.datetime.now()
            newUser = ExtraInfo()
            newUser.userID = user
            newUser.activity = userInfo['activity']
            newUser.birth_year = str(int(now.year) - int(userInfo['age']))
            newUser.drink_level = userInfo['drink_level']
            newUser.hijos = userInfo['hijos']
            newUser.interest = userInfo['interest']
            newUser.marital_status = userInfo['marital_status']
            newUser.personality = userInfo['personality']
            newUser.religion = userInfo['religion']
            newUser.smoker = userInfo['smoker']
            newUser.save()
            logged = authenticate(username=userInfo['username'], password=userInfo['password'])
            login(request, logged)
            return render(request, 'index.html', locals())
    else:
        register_form = RegistForm()
        return render(request, 'signup.html', locals())


def sign(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            userData = login_form.cleaned_data
            user = authenticate(username=userData['username'], password=userData['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/index/')
            else:
                fails = True
                return render(request, 'signin.html', locals())
    else:
        login_form = LoginForm()
    return render(request, 'signin.html', locals())


def getRestaurants(request):
    restaurantId = request.GET["id"]
    restaurant = Geoplace.objects.filter(id=restaurantId)[0]
    open_time = Hours.objects.filter(placeID=restaurant.placeID)
    if open_time is None or len(open_time) == 0:
        open_time = Hours()
        open_time.days = "not available"
        open_time.hours = "not available"
    else:
        open_time = open_time[0]
    parking = Parking.objects.filter(placeID=restaurant.placeID)
    if parking is None or len(parking) == 0:
        parking = Parking()
        parking.parking_lot = "not available"
    else:
        parking = parking[0]
    description = getDescription(restaurant)
    # TODO: replace this part with the result of kNN
    restaurants = Geoplace.objects.all()
    related = restaurants[0:3]
    return render(request, 'res.html', locals())


def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/index/')


def getBudgetSymbol(price):
    if price == 'low':
        res = '$'
    elif price == 'medium':
        res = '$$'
    else:
        res = '$$$'
    return res


def getDescription(res):
    cuisine = Cuisine.objects.filter(placeID=res.placeID)
    des = res.name + " "
    if cuisine is not None or len(cuisine) != 0:
        des += "provides " + cuisine[0].Rcuisine + ' and '
    if res.alcohol == 'No_Alcohol_Served':
        des += "do not provide alcohols. "
    elif res.alcohol =='Wine_Beer':
        des += "provides wines and beers. "
    else:
        des += "is a full bar, a variety of alcohol is provided. "
    if res.smoking_area == "permitted":
        des += "there is smoking area in this restaurant. "
    else:
        des += "smoking is prohibited anywhere in this restaurant. "
    des += 'the dress code of this restaurant is ' + res.dress_code + '. '
    if res.accessibility == 'no_accessibility':
        des += 'It provides no accessibility for handicapped'
    else:
        des += 'handicapped accessibility is ' + res.accessibility + ' provided. '
    des += 'This restaurant is a ' + res.area + ' area, ' + 'and has ' + res.Rambience + ' rambience. '
    if res.other_services == 'variety':
        des += 'variety of other service is offered here. '
    elif res.other_services == 'Internet':
        des += 'Internet service is provided'
    des += 'Welcome to ' + res.name + '!'
    return des
