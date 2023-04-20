import datetime
import pygame
from loader import Loader
import json
import time
import threading
import queue

# get settings from config.json
with open("config.json") as f:
    settings = json.load(f)

modules = settings["modules"]

# Initialize Pygame and objects
pygame.init()
def load_loader(queue):
    loader = Loader()
    queue.put(loader)

loader_queue = queue.Queue()
load_thread = threading.Thread(target=load_loader, args=(loader_queue,))
load_thread.start()
print("thread started")
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
x_large = pygame.font.Font('fonts/Roboto/Roboto-Medium.ttf', 86)
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
    print('loop started')
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
    print(loader_queue)
    print(not loader_queue.empty())

    if loader_queue is not None:
        loader = loader_queue.get()
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

        # Mail
    else:
        loading_text = x_large.render("loading...", True, white)
        screen.blit(loading_text, (screen_width/2, screen_height/2))
    # Update the display and modules
    pygame.display.update()

load_thread.join()
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

""""
New modules:
    - Mail
    - Calendar
    - Maps
        - Bus
        - Car 
        - Bike
    - Virtual Assistant
    - Sports 
    - Alarm Clock
    - Bluetooth devices - bluetooth module
    - Lights 
    - Timer
    - Birthdays
    - Dossiers
"""

"""
Maybe add a loader module that has the following properties
- add code to modules in loader rather than to the loops
- add the loader modules to the loops with with inputs being called into the module
    - the inputs will be most of the variables put before the loops
- the loader module will take information from config.json that will tell it what modules to use and where to put them
- this adds customizablity to the program that doesn't have to be hard coded
- this could be wrapped into the virtual assistant
"""

"""
I would like to possibly add a server and a website so that this code can be controlled from my phone and computer as well
as from a virtual assistant

Threading can be used to run the virtual assistant and mirror concurrently 

Have the virtual assistant save sentences that aren't previously trained to use for training data in the future
    - it can ask if it did the right thing or I can find a way to say that it did or didnt and use that for training
    - as more data is collected and more applications are added I can continuously retrain the model to make it more 
        accurate. 
"""