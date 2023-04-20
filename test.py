import datetime
import pygame
from loader import Loader
import json

# get settings from config.json
with open("config.json") as f:
    settings = json.load(f)

modules = settings["modules"]
canvas_reload_time = datetime.datetime.now().time()
weather_reload_time = datetime.datetime.now().time()

# Initialize Pygame and objects
pygame.init()
loader = Loader()

# Set the size of the screen and related data
screen_data = pygame.display.Info()
screen_width, screen_height = screen_data.current_w, screen_data.current_h
flags = pygame.FULLSCREEN
screen = pygame.display.set_mode((screen_width, screen_height), flags)
pygame.display.set_caption("Black Screen")
black = (0, 0, 0)
white = (255, 255, 255)
padding = 0.01
top_right = (screen_width*padding, screen_height*padding)
top_left = (screen_width*(1-padding), screen_height*padding)
bottom_left = (screen_width*padding, screen_height*(1-padding))
bottom_right = (screen_width*(1-padding), screen_height*(1-padding))
top_adjusts = -1
bottom_adjusts = 1

# images
icon_image = pygame.image.load("icons/clock.jpg")
new_icon_size = (50, 50)
icon_image = pygame.transform.scale(icon_image, new_icon_size)
icon_x = screen_width / 2
icon_y = screen_height / 2
icon_rect = pygame.Rect(icon_x, icon_y, icon_image.get_width(), icon_image.get_height())

assignment_icon = pygame.image.load("icons/assignment.png")
assignment_icon = pygame.transform.scale(assignment_icon, new_icon_size)
assign_rect = pygame.Rect(icon_x, icon_y, assignment_icon.get_width(), assignment_icon.get_height())

# Refresh loop
# in the future, these load booleans will be used to run while loops causing a reload of information at different intervals
load_weather = False
load_assignments = False
load_clock = True
load_mail = False
startup = True
while startup:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            startup = False
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                startup = False
                running = False

    # Fill the screen with the background color
    screen.fill(black)

    # display clock
    clock_text = loader.load_clock(255)
    date_text = loader.load_date(255)
    screen.blit(clock_text, top_right)
    screen.blit(date_text, (top_right[0],top_right[1]+clock_text.get_height()))

    # display assignments
    assignment_data = loader.load_assignments(255)
    assign_values = []
    date_values = []
    for i in range(len(assignment_data[0])):
        tuple = (assignment_data[0][i], (bottom_left[0], bottom_left[1] - (1+i)*assignment_data[0][0].get_height()))
        assign_values.append(tuple)
    for i in range(len(assignment_data[1])):
        tuple = (assignment_data[1][i], (bottom_left[0] + assignment_data[2].get_width() + 10, bottom_left[1] - (1+i)*assignment_data[0][0].get_height()))
        date_values.append(tuple)
    screen.blits(assign_values)
    screen.blits(date_values)

    # weather
    temp_text = loader.load_current_temperature(255)
    max_min = loader.load_max_min(255)
    screen.blit(max_min[0], (top_left[0] - max_min[0].get_width(), top_left[1] + 10))
    screen.blit(max_min[1], (top_left[0] - max_min[0].get_width(), top_left[1] + max_min[0].get_height() + 10))
    screen.blit(temp_text, (top_left[0] - temp_text.get_width() - max_min[0].get_width(), top_left[1]))
    screen.blit(loader.load_icon(255), (top_left[0] - loader.load_icon(255).get_width() - temp_text.get_width()
                                        - max_min[0].get_width(), top_left[1]))
    weather_tiles_info = loader.load_forecast()
    times = []
    icons_ = []
    temps = []
    for i in range(len(weather_tiles_info[0])):
        tuple = (weather_tiles_info[0][i], (top_left[0] - (weather_tiles_info[0][2].get_width() + 40)*(i+1), top_left[1] + temp_text.get_height() + 20))
        times.append(tuple)
    for i in range(len(weather_tiles_info[2])):
        tuple = (loader.return_icon(weather_tiles_info[2][i], 255, weather_tiles_info[3][i]*60*60),
                 (top_left[0] - (60 + 40)*(i+1), top_left[1] + temp_text.get_height() + weather_tiles_info[0][2].get_height()+20))
        icons_.append(tuple)
    for i in range(len(weather_tiles_info[1])):
        tuple = (weather_tiles_info[1][i], (top_left[0] - (weather_tiles_info[0][2].get_width() + 40)*(i+1),
                                            top_left[1] + temp_text.get_height() + weather_tiles_info[0][2].get_height() + 85))
        temps.append(tuple)
    screen.blits(times)
    screen.blits(icons_)
    screen.blits(temps)

    week = loader.load_birthdays()
    day_val = []
    # Birthdays
    for i in range(len(week)):
        tuple = (week[i], (bottom_right[0] - week[i].get_width(), bottom_right[1] - (1+i)*week[i].get_height()))
        day_val.append(tuple)
    screen.blits(day_val)

    current_time = datetime.datetime.now().time()
    diff_time = loader.time_to_seconds(current_time.strftime("%H:%M:%S")) - loader.time_to_seconds(canvas_reload_time.strftime("%H:%M:%S"))
    if diff_time > 3*60*60:
        loader.reload_modules("canvas")
        canvas_reload_time = datetime.datetime.now()
    diff_time = loader.time_to_seconds(current_time.strftime("%H:%M:%S")) - loader.time_to_seconds(weather_reload_time.strftime("%H:%M:%S"))
    if diff_time > 60*60:
        loader.reload_modules("weather")
        weather_reload_time = datetime.datetime.now()
    # Update the display and modules
    pygame.display.update()

pygame.quit()

"""put in code to update modules. Maybe in the future I can use threading to load and reload the modules at the same 
time that I am running the code. While they are updating I can put a loading text over the area that the module usually
appears"""

"""
i will use if-else loops and the config.json to decide the items to include

when I use the if-else loops i can use variables like assign_x and assign_y and the preset positions to change location
changing the applications that are displayed may be harder but I could use True and False statements or I could set the alpha
to 0 for the ones that shouldn't be shown (but this would be inefficient with the computer's resources)
"""

"""
I have to fix the Canvas to ensure that the APIs are only called within the init function.
"""