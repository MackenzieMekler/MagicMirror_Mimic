"""
This is the script that I hope to use to load all of the objects into the game loop to make it more customizable in
future and more easily integrated into the virtual assistant. This will be a class with individual modules that load
a function (with the animation) and others that maintain it in the running loop. This should allow for what I am hoping
if I can find a way to run it correctly.

This should take information both from the virtual assistant and the config file (im not sure if this should be put in
here or in the main.py folder)
"""
import pygame
from modules.clock import Time
from modules.Canvas import Canvas
from modules.weather import Weather
from modules.Important_Dates.Important_Dates import Important_Dates
import json
import datetime
import concurrent.futures


class Loader:
    def __init__(self):
        with open("config.json") as f:
            settings = json.load(f)
        dict = {}
        for item in settings["modules"]:
            dict[f"{item['module_name']}"] = item
        # initialize classes
        pygame.init()
        self.myTime = Time()
        self.canvas = Canvas(
            api_token= dict['Canvas']['module_information']['API_key'],
            url= dict['Canvas']['module_information']['url'],
            active_courses= dict['Canvas']['module_information']['active_courses']
        )
        self.weather = Weather(
            lat= dict['weather']['module_information']['latitude'],
            lon= dict['weather']['module_information']['longitude']
        )
        self.significant_dates = Important_Dates()
        self.week_bday, self.month_bday = self.significant_dates.getBirthdays()
        print(self.week_bday)
        print(self.month_bday)
        # stuff
        self.x_small = pygame.font.Font('fonts/Roboto/Roboto-Medium.ttf', 16)
        self.small = pygame.font.Font('fonts/Roboto/Roboto-Medium.ttf', 24)
        self.medium = pygame.font.Font('fonts/Roboto/Roboto-Medium.ttf', 32)
        self.large = pygame.font.Font('fonts/Roboto/Roboto-Medium.ttf', 62)
        self.x_large = pygame.font.Font('fonts/Roboto/Roboto-Medium.ttf', 86)
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.seconds_day = 24*60*60
        # canvas information
        self.assignments_list = self.canvas.getAsssignments()
        # weather information
        self.sunrise = self.weather.sunrise_sunset()[0]
        self.sunset = self.weather.sunrise_sunset()[1]
        self.sunrise_sec = self.time_to_seconds(self.sunrise)
        self.sunset_sec = self.time_to_seconds(self.sunset)
        self.current_weathercode = int(self.weather.currentweather()['weathercode'])
        self.temperature_list = self.weather.get_temperature()
        self.weathercode_list = self.weather.weathercode()
        print("loading APIs...")

    def load_clock(self, alpha):
        current_time = self.myTime.getTime()
        clock_text = self.large.render(current_time, True, self.white)
        clock_text.set_alpha(alpha)
        return clock_text

    def load_date(self, alpha):
        current_date = self.myTime.getDate()
        date_text = self.medium.render(current_date, True, self.white)
        date_text.set_alpha(alpha)
        return date_text

    def load_max_min(self, alpha):
        max_temp = self.weather.dailytemp()[0]
        min_temp = self.weather.dailytemp()[1]
        max_text = self.medium.render(str(max_temp), True, self.white)
        min_text = self.medium.render(str(min_temp), True, self.white)
        max_text.set_alpha(alpha)
        min_text.set_alpha(alpha)
        return max_text, min_text

    def load_current_temperature(self, alpha):
        current_temp = self.weather.currentweather()["temperature"]
        current_temp_text = self.x_large.render(str(current_temp), True, self.white)
        current_temp_text.set_alpha(alpha)
        return current_temp_text

    def load_icon(self, alpha):
        current_sec = self.time_to_seconds(self.myTime.getTime())
        is_day = (self.sunset_sec > current_sec > self.sunrise_sec)
        # select icon
        if self.current_weathercode == 0 or self.current_weathercode == 1:
            if is_day:
                weathericon = pygame.image.load("icons/weather_icons/clear-day.png")
            else:
                weathericon = pygame.image.load("icons/weather_icons/clear-night.png")
        elif self.current_weathercode == 2 or self.current_weathercode == 3:
            if is_day:
                weathericon = pygame.image.load("icons/weather_icons/partly-cloudy-day.png")
            else:
                weathericon = pygame.image.load("icons/weather_icons/partly-cloudy-night.png")
        elif self.current_weathercode == 45 or self.current_weathercode == 48:
            weathericon = pygame.image.load("icons/weather_icons/fog.png")
        elif (50 < self.current_weathercode < 66) or self.current_weathercode == 80 or self.current_weathercode == 81 or \
                self.current_weathercode == 82:
            weathericon = pygame.image.load("icons/weather_icons/rain.png")
        elif self.current_weathercode == 66 or self.current_weathercode == 67:
            weathericon = pygame.image.load("icons/weather_icons/sleet.png")
        elif (70 < self.current_weathercode < 80) or self.current_weathercode == 85 or self.current_weathercode == 86:
            weathericon = pygame.image.load("icons/weather_icons/snow.png")
        elif self.current_weathercode > 90:
            weathericon = pygame.image.load('icons/weather_icons/thunderstorm.png')
        else:
            weathericon = None

        weathericon = pygame.transform.scale(weathericon, (100, 100))
        weathericon.set_alpha(alpha)
        return weathericon

    def load_forecast(self):
        """
        in this module I will set the time and a loop for formatting in the main.py script
        this module will simply return the forecast at a requested time.
        """
        hours = self.temperature_list['hourly']['time']
        temperatures = self.temperature_list['hourly']['temperature_2m']
        weathercodes = self.weathercode_list['hourly']['weathercode']

        information = []
        weather_tile = []
        for i in range(len(hours)):
            forecast_properties = [
                datetime.datetime.strptime(hours[i], "%Y-%m-%dT%H:%M"),
                temperatures[i],
                weathercodes[i]
            ]
            information.append(forecast_properties)
        for item in information:
            if item[0].strftime("%H:%M") == "09:00" or item[0].strftime("%H:%M") == "14:00" or item[0].strftime("%H:%M") == "20:00":
                if item[0] >= datetime.datetime.now() and len(weather_tile) < 3:
                    weather_tile.append(item)

        """the problem is the time doesn't take into account the day"""

        temps = []
        codes = []
        times = []
        t = []
        for temperature in weather_tile:
            temp_text = self.small.render(str(temperature[1]), True, self.white)
            temps.append(temp_text)
            codes.append(temperature[2])
            if temperature[0].strftime("%H:%M") == "09:00":
                time_text = self.small.render("9 AM", True, self.white)
                ti = 9
            elif temperature[0].strftime("%H:%M") == "14:00":
                time_text = self.small.render("2 PM", True, self.white)
                ti = 14
            elif temperature[0].strftime("%H:%M") == "20:00":
                time_text = self.small.render("8 PM", True, self.white)
                ti = 20
            times.append(time_text)
            t.append(ti)

        return [times[::-1], temps[::-1], codes[::-1], t[::-1]]

    def load_sun_tracker(self, alpha):
        """
        this is the loader method for the sun tracker
        to be completely honest im not quite sure how to do this it was a miracle that i did it the first time
        """

    def load_assignments(self, alpha):
        """
        in this module I will return an ordered list of assignment_text that can be
        blited on the screen using screen.blits() or the regular screen.blit() and a loop
        within the main.py script
        """
        date_list = []
        assign_list = []
        longest_text = self.medium.render('', True, self.white)
        for i in range(len(self.assignments_list)):
            # properties
            name = self.assignments_list[f'Assignment_{i}']['name']
            _class = self.assignments_list[f'Assignment_{i}']['class']

            # final formatted text
            text = _class + ": " + name[0:18]
            if (len(name) > 18):
                text = text + "..."
            assignment_text = self.medium.render(text, True, self.white)
            assignment_text.set_alpha(alpha)
            if (assignment_text.get_width() > longest_text.get_width()):
                longest_text = self.medium.render(text, True, self.white)
            assign_list.append(assignment_text)


        for i in range(len(self.assignments_list)):
            date = self.assignments_list[f'Assignment_{i}']['due_date']
            assign_date_text = self.medium.render(date, True, self.white)
            assign_date_text.set_alpha(alpha)
            date_list.append(assign_date_text)

        return [assign_list, date_list, longest_text]

    @staticmethod
    def time_to_seconds(time):
        try:
            time_obj = datetime.datetime.strptime(time, "%H:%M:%S")
            total_sec = time_obj.second + time_obj.minute * 60 + time_obj.hour * 60 * 60
        except:
            time_obj = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M")
            total_sec = time_obj.minute*60 + time_obj.hour*60*60
        return total_sec

    def return_icon(self, current_weathercode, alpha, seconds):
        is_day = (self.sunset_sec > seconds > self.sunrise_sec)
        # select icon
        if current_weathercode == 0 or current_weathercode == 1:
            if is_day:
                weathericon = pygame.image.load("icons/weather_icons/clear-day.png")
            else:
                weathericon = pygame.image.load("icons/weather_icons/clear-night.png")
        elif current_weathercode == 2 or current_weathercode == 3:
            if is_day:
                weathericon = pygame.image.load("icons/weather_icons/partly-cloudy-day.png")
            else:
                weathericon = pygame.image.load("icons/weather_icons/partly-cloudy-night.png")
        elif current_weathercode == 45 or current_weathercode == 48:
            weathericon = pygame.image.load("icons/weather_icons/fog.png")
        elif (50 < current_weathercode < 66) or current_weathercode == 80 or current_weathercode == 81 or \
                current_weathercode == 82:
            weathericon = pygame.image.load("icons/weather_icons/rain.png")
        elif current_weathercode == 66 or current_weathercode == 67:
            weathericon = pygame.image.load("icons/weather_icons/sleet.png")
        elif (70 < current_weathercode < 80) or current_weathercode == 85 or current_weathercode == 86:
            weathericon = pygame.image.load("icons/weather_icons/snow.png")
        elif current_weathercode > 90:
            weathericon = pygame.image.load('icons/weather_icons/thunderstorm.png')
        else:
            weathericon = None

        weathericon = pygame.transform.scale(weathericon, (65, 65))
        weathericon.set_alpha(alpha)
        return weathericon

    def load_birthdays(self):
        week = []
        len_week = len(self.week_bday)
        len_month = len(self.month_bday)
        if len_week > 0:
            for date in self.week_bday:
                day = date[0].strftime("%A %b %d")
                person = date[1]
                text = self.medium.render(str(person) + " " + str(day), True, self.white)
                week.append(text)
        if len_month > 0:
            for date in self.month_bday:
                day = date[0].strftime("%A %b %d")
                person = date[1]
                text = self.medium.render(str(person) + " " + str(day), True, (0, 0, 255))
                week.append(text)

        return week

    def reload_modules(self, module):
        with open("config.json") as f:
            settings = json.load(f)
        dict = {}
        for item in settings["modules"]:
            dict[f"{item['module_name']}"] = item
        if module == "canvas":
            self.canvas = Canvas(
                api_token=dict['Canvas']['module_information']['API_key'],
                url=dict['Canvas']['module_information']['url'],
                active_courses=dict['Canvas']['module_information']['active_courses']
            )
            self.assignments_list = self.canvas.getAsssignments()
        elif module == "weather":
            self.weather = Weather(
                lat=dict['weather']['module_information']['latitude'],
                lon=dict['weather']['module_information']['longitude']
            )
            self.sunrise = self.weather.sunrise_sunset()[0]
            self.sunset = self.weather.sunrise_sunset()[1]
            self.sunrise_sec = self.time_to_seconds(self.sunrise)
            self.sunset_sec = self.time_to_seconds(self.sunset)
            self.current_weathercode = int(self.weather.currentweather()['weathercode'])
            self.temperature_list = self.weather.temperature()
            self.weathercode_list = self.weather.weathercode()


    @staticmethod
    def make_api_request(url):
        # response = requests.get(url)
        # return response.json()
        print("hi")
