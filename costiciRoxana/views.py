import requests
from django.shortcuts import render
from django.db import DatabaseError
from .models import WeatherForecast
import datetime

def get_weather(request):
    weather_data = None
    city_name = None
    error_message = None  

    if request.method == 'POST':
        city_name = request.POST['city_name']
        api_key = '7f8db97ba1074ce08aa120837242908'  
        url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city_name}&days=3"

        try:
            response = requests.get(url)
            response.raise_for_status()  

            data = response.json()
            weather_data = data['forecast']['forecastday']

            for day in weather_data:
                date = datetime.datetime.strptime(day['date'], '%Y-%m-%d').date()
                max_temp = day['day']['maxtemp_c']
                min_temp = day['day']['mintemp_c']
                total_precipitation = day['day']['totalprecip_mm']
                sunrise_hour = datetime.datetime.strptime(day['astro']['sunrise'], '%I:%M %p').time()
                sunset_hour = datetime.datetime.strptime(day['astro']['sunset'], '%I:%M %p').time()

                try:
                    WeatherForecast.objects.update_or_create(
                        date=date,
                        city=city_name,
                        defaults={
                            'max_temp': max_temp,
                            'min_temp': min_temp,
                            'total_precipitation': total_precipitation,
                            'sunrise_hour': sunrise_hour,
                            'sunset_hour': sunset_hour
                        }
                    )
                except DatabaseError as e:
                    error_message = "A apărut o eroare la salvarea datelor în baza de date."
                    print(f"Eroare baza de date: {e}") 

        except requests.exceptions.RequestException as e:
            error_message = "Nu am putut obține datele meteo. Verifică conexiunea la internet sau orașul introdus."
            print(f"Eroare cerere API: {e}")  

    return render(request, 'index.html', {
        'weather_data': weather_data,
        'city_name': city_name,
        'error_message': error_message
    })
