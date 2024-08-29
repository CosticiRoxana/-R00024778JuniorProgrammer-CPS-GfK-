from django.db import models

class WeatherForecast(models.Model):
    date = models.DateField()
    city = models.CharField(max_length=100)
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    total_precipitation = models.FloatField()
    sunrise_hour = models.TimeField()
    sunset_hour = models.TimeField()

    

   
