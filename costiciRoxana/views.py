import requests
from django.shortcuts import render
from .models import WeatherForecast
from datetime import datetime

# task1.1
def get_weather(request):
    weather_data = None
    city_name = None

    if request.method == 'POST':
        city_name = request.POST['city_name']
        api_key = '7f8db97ba1074ce08aa120837242908'  
        url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city_name}&days=3"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = data['forecast']['forecastday']
#end task1.1

#task1.2
            for day in weather_data:
                date = datetime.strptime(day['date'], '%Y-%m-%d').date()
                max_temp = day['day']['maxtemp_c']
                min_temp = day['day']['mintemp_c']
                total_precipitation = day['day']['totalprecip_mm']
                sunrise_hour = datetime.strptime(day['astro']['sunrise'], '%I:%M %p').time()
                sunset_hour = datetime.strptime(day['astro']['sunset'], '%I:%M %p').time()

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
# end task1.2
    return render(request, 'index.html', {'weather_data': weather_data, 'city_name': city_name})
