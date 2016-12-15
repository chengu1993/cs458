from django.shortcuts import render
from forms.usrForms import LoginForm, RegistForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, Group
from food.models import ExtraInfo, Geoplace, Hours, Parking, Cuisine, RestaurantLabel
from django.contrib.auth import authenticate, login, logout
from scripts.clustering import classify, rest_knn
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
    restaurant_label = RestaurantLabel.objects.filter(placeID=restaurant.placeID)
    if restaurant_label is not None and len(restaurant_label) >= 1:
        labels = restaurant_label[0]
        knn = [labels.latitude, labels.longitude, labels.alcohol,
               labels.smoking_area, labels.dress_code, labels.accessibility,
               labels.price, labels.Rambience, labels.franchise, labels.area, labels.cuisine, labels.parking_lot]
        IDList = rest_knn(knn)
        print(len(IDList))
        print(IDList)
        related_restaurant = Geoplace.objects.filter(placeID__in=IDList)
        related = related_restaurant[0:3]
        # appeared = set()
        # related = []
        # for rest in related_restaurant:
        #     if rest.placeID not in appeared:
        #         rest.delete()
        #         appeared.add(rest.placeID)
        # print(len(related_restaurant))
    else:
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


def extraValues(request):
    dress_preference = request.POST.get("dress_preference", "")
    ambience = request.POST.get("ambience", "")
    transport = request.POST.get("transport", "")
    budget = request.POST.get("budget", "")
    if ambience != "" and transport != "" and dress_preference != "" and budget != "":
        profile = []
        current_user = ExtraInfo.objects.filter(userID=request.user)[0]
        if current_user.smoker:
            profile.append("1")
        else:
            profile.append("0")
        profile.append(current_user.drink_level)
        profile.append(current_user.marital_status)
        profile.append(current_user.hijos)
        profile.append(current_user.birth_year)
        profile.append(current_user.interest)
        profile.append(current_user.personality)
        profile.append(current_user.religion)
        profile.append(current_user.activity)
        placeIDList = classify([profile])
        new_placeID_list = []
        if transport == 'car_owner':
            parkinglist = Parking.objects.filter(placeID__in=placeIDList). \
                filter(parking_lot__in=['public', 'yes', 'valet_parking', 'free', 'street', 'validated_parking'])
            for parking in parkinglist:
                new_placeID_list.append(parking.placeID)
        else:
            new_placeID_list = placeIDList
        restaurantList = Geoplace.objects.filter(placeID__in=new_placeID_list)\
            .filter(dress_code=dress_preference).filter(Rambience=ambience).filter(price=budget)
        if len(restaurantList) <= 30:
            recent = restaurantList
            for res in recent:
                res.price = getBudgetSymbol(res.price)
        else:
            recent = restaurantList[0:30]
            for res in recent:
                res.price = getBudgetSymbol(res.price)
    request.session['extra_mark'] = True
    return render(request, 'index.html', locals())


def userInfo(request):
    userId = request.user.id
    print(userId)
    current_user = User.objects.filter(id=userId)[0]
    smoker = [False, True]
    drink_level = ['abstemious', 'social drinker', 'casual drinker']
    marital_status = ['single', 'married', 'widow']
    hijos = ['independent', 'kids', 'dependent']
    interest = ['variety', 'technology', 'none', 'retro', 'eco-friendly']
    personality = ['thrifty-protector', 'hunter-ostentatious', 'hard-worker', 'conformist']
    religon = ['none', 'Catholic', 'Christian', 'Mormon', 'Jewish']
    activity = ['student', 'professional', 'working-class', 'unemployed']
    extraInfo = ExtraInfo.objects.filter(userID=current_user)[0]
    valueList = []
    extraInfo.smoker = smoker[int(extraInfo.smoker)]
    extraInfo.drink_level = drink_level[int(extraInfo.drink_level)]
    extraInfo.marital_status = marital_status[int(extraInfo.marital_status)]
    extraInfo.hijos = hijos[int(extraInfo.hijos)]
    extraInfo.interest = interest[int(extraInfo.interest)]
    extraInfo.personality = personality[int(extraInfo.personality)]
    extraInfo.religion = personality[int(extraInfo.religion)]
    extraInfo.activity = activity[int(extraInfo.activity)]
    return render(request, 'userProfile.html', locals())

def getAbout(request):
    return render(request, 'about.html', locals())
