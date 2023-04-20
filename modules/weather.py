import datetime
import requests
from datetime import *

class Weather():
    def __init__(self, lat, lon):
        self.base_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&temperature_unit=fahrenheit&" \
                        f"windspeed_unit=mph&precipitation_unit=inch&timezone=America%2FNew_York&forecast_days=2"
        url = self.base_url + "&hourly=temperature_2m"
        self.temperature = requests.get(url).json()
        url = self.base_url + "&hourly=weathercode"
        self.weather_code = requests.get(url).json()
        url = self.base_url + "&daily=temperature_2m_max,temperature_2m_min"
        response = requests.get(url).json()
        self.max_min = [response["daily"]["temperature_2m_max"][0], response["daily"]["temperature_2m_min"][0]]
        url = self.base_url + "&daily=sunrise,sunset"
        response = requests.get(url).json()
        self.sunrise_sunset_values = [response["daily"]["sunrise"][0],response["daily"]["sunset"][0]]
        url = self.base_url + "&current_weather=true"
        self.current = requests.get(url).json()['current_weather']

        self.now = datetime.now()

    def get_temperature(self):
        return self.temperature

    def feels_like_temp(self):
        """ Not currently a functional module """
        url = self.base_url + "&hourly=apparent_temperature"
        response = requests.get(url).json()

    def humidity(self):
        """ Not currently a functional module """
        url = self.base_url + "&humidity=relativehumidity_2m"
        response = requests.get(url)

    def weathercode(self):
        return self.weather_code

    def windspeed(self):
        """ Not currently functional """
        url = self.base_url + "&hourly=windspeed_10m"
        response = requests.get(url)

    def uv(self):
        """ Not currently functional """
        url = self.base_url + "&hourly=uv_index"
        response = requests.get(url)

    def dailytemp(self):
        # add ,apparent_temperature_max,apparent_temperature_min for feels_like as well
        return self.max_min

    def sunrise_sunset(self):
        return self.sunrise_sunset_values

    def currentweather(self):
        return self.current