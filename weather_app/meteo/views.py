from datetime import datetime

import geocoder
import requests
from django.http import HttpResponse
from django.template import loader
from meteo.models import Worldcities
from django.core.cache import cache

def get_worldcities():
    worldcities = cache.get('worldcities')
    if worldcities is None:
        worldcities = Worldcities.objects.all()
        cache.set('worldcities', worldcities)
    return worldcities

def get_random_city():
    worldcities = get_worldcities()
    return worldcities.order_by('?').first()

def temp_here(request):
    geo = geocoder.ip('me')
    city = geo.city
    location = geo.latlng
    temp = get_temp(location)
    template = loader.get_template('index.html')
    context = {
        'city': city,
        'temp': temp,
    }
    return HttpResponse(template.render(context, request))


def get_temp(location):
    endpoint = "https://api.open-meteo.com/v1/forecast"
    api_request = f"{endpoint}?latitude={location[0]}&longitude={location[1]}&hourly=temperature_2m" \
                  f"&temperature_unit=fahrenheit"
    now = datetime.now()
    hour = now.hour
    meteo_data = requests.get(api_request).json()
    temp = meteo_data['hourly']['temperature_2m'][hour]
    return temp


def temp_somewhere(request):
    random_item = get_random_city()
    city = random_item.city
    location = [random_item.lat, random_item.lng]
    temp = get_temp(location)
    template = loader.get_template("index.html")
    context = {
        'city': city,
        'temp': temp
    }
    return HttpResponse(template.render(context, request))
