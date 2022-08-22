from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    global placeDetailed    # Для отображения подробного прогноза

    appid = 'f1f3ef0d3c6e32864b2a7b0dc23d4993'
    url ="https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + appid

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm

    cities = City.objects.all()
    all_cities = []
    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'id': city.id,
            'city': city.name,
            'lat': str(res['coord']['lat']),
            'lon': str(res['coord']['lon']),
            'temp': res['main']['temp'],
            'temp_fl': res['main']['feels_like'],
            'temp_max': res['main']['temp_max'],
            'icon': res['weather'][0]['icon'],
            'pressure': res['main']['pressure'],
            'humidity': res['main']['humidity'],
            'wind_s': res['wind']['speed'],
        }

        all_cities.insert(0, city_info)

        placeDetailed = city_info


    parameters = {'title': 'Прогноз погоды', 'all_info': all_cities, 'form': form}
    return render(request, 'weather/index.html', parameters)

def delete(request, id):
    try:
        form = City.objects.get(id=id)
        form.delete()
        return HttpResponseRedirect("/")
    except:
        return HttpResponseNotFound("<h2>Not found</h2>")



def about(request):
    parameters = {'title': 'О проекте'}
    return render(request, 'weather/about.html', parameters)

def page1(request):    # Подробный прогноз

    parameters = {'title': 'Подробно', 'd_info': placeDetailed}
    return render(request, 'weather/page1.html', parameters)

def page2(request):
    parameters = {'title': 'Страница 2'}
    return render(request, 'weather/page2.html', parameters)

