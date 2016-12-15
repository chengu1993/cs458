from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class Geoplace(models.Model):
    placeID = models.IntegerField(verbose_name="place_id")
    latitude = models.FloatField(verbose_name="latitude")
    longitude = models.FloatField(verbose_name="longitude")
    the_geom_meter = models.CharField(max_length=50, verbose_name="geom_meter")
    name = models.CharField(max_length=50, verbose_name="name")
    address = models.CharField(max_length=50, verbose_name="address")
    city = models.CharField(max_length=10, verbose_name="city")
    state = models.CharField(max_length=10, verbose_name="state")
    country = models.CharField(max_length=10, verbose_name="country")
    fax = models.IntegerField(verbose_name="fax")
    zip = models.IntegerField(verbose_name="zip")
    alcohol = models.CharField(max_length=20, verbose_name="alcohol")
    smoking_area = models.CharField(max_length=30, verbose_name="smoking")
    dress_code = models.CharField(max_length=10, verbose_name="dress code")
    accessibility = models.CharField(max_length=30, verbose_name="accessibility")
    price = models.CharField(max_length=10, verbose_name="price")
    url = models.CharField(max_length=100, verbose_name="url")
    Rambience = models.CharField(max_length=10, verbose_name="rambience")
    franchise = models.CharField(max_length=1, verbose_name="franchise")
    area = models.CharField(max_length=10, verbose_name="area")
    other_services = models.CharField(max_length=10, verbose_name="otherservices")


class userProfile(models.Model):
    userID = models.CharField(max_length=50, verbose_name="user_id")
    latitude = models.FloatField(verbose_name="latitude")
    longitude = models.FloatField(verbose_name="longitude")
    smoker = models.BooleanField(verbose_name="smoker")
    drink_level = models.CharField(max_length=20, verbose_name="drink_level")
    dress_preference = models.CharField(max_length=30, verbose_name="dress_preference")
    ambience = models.CharField(max_length=20, verbose_name="ambience")
    transport = models.CharField(max_length=10, verbose_name="transport")
    marital_status = models.CharField(max_length=10, verbose_name="martial")
    hijos = models.CharField(max_length=10, verbose_name="hijos")
    birth_year = models.CharField(max_length=20, verbose_name="birth_year")
    interest = models.CharField(max_length=30, verbose_name="interest")
    personality = models.CharField(max_length=50, verbose_name="personality")
    religion = models.CharField(max_length=10, verbose_name="religion")
    activity = models.CharField(max_length=20, verbose_name="activity")
    color = models.CharField(max_length=10, verbose_name="color")
    weight = models.FloatField(verbose_name="weight")
    budget = models.CharField(max_length=10, verbose_name="budget")
    height = models.FloatField(verbose_name="height")


class Cuisine(models.Model):
    placeID = models.IntegerField(verbose_name="place_id")
    Rcuisine = models.CharField(max_length=30, verbose_name="cuisine")

    def __unicode__(self):
        return self.Rcuisine


class Hours(models.Model):
    placeID = models.IntegerField(verbose_name="place_id")
    hours = models.CharField(max_length=20, verbose_name="hours")
    days = models.CharField(max_length=5, verbose_name="days")


class Parking(models.Model):
    placeID = models.IntegerField(verbose_name="place_id")
    parking_lot = models.CharField(max_length=20, verbose_name="parking")


class ratingFinal(models.Model):
    userID = models.CharField(max_length=50, verbose_name="user_id")
    placeID = models.IntegerField(verbose_name="place_id")
    rating = models.IntegerField(verbose_name="rating")
    food_rating = models.IntegerField(verbose_name="food_rating")
    service_rating = models.IntegerField(verbose_name="service_rating")


class userCuisine(models.Model):
    userID = models.CharField(max_length=50, verbose_name="user_id")
    Rcuisine = models.CharField(max_length=30, verbose_name="cuisine")


class cuisinelabel(models.Model):
    placeID = models.IntegerField(verbose_name="place_id")
    labelID = models.IntegerField(verbose_name="label_id")


class ExtraInfo(models.Model):
    userID = models.ForeignKey(User, verbose_name="user_id")
    smoker = models.BooleanField(verbose_name="smoker", default=False)
    drink_level = models.CharField(max_length=20, verbose_name="drink_level", null=True)
    marital_status = models.CharField(max_length=10, verbose_name="martial", null=True)
    hijos = models.CharField(max_length=10, verbose_name="hijos", null=True)
    birth_year = models.CharField(max_length=20, verbose_name="birth_year", null=True)
    interest = models.CharField(max_length=30, verbose_name="interest", null=True)
    personality = models.CharField(max_length=50, verbose_name="personality", null=True)
    religion = models.CharField(max_length=10, verbose_name="religion", null=True)
    activity = models.CharField(max_length=20, verbose_name="activity", null=True)


