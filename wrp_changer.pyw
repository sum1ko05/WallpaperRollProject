import ctypes
import random
import os
from copy import deepcopy
import config_manager as cfg
import time
import datetime


def change_wallpaper(folder_path, image_name):
    path_to_image = folder_path + "/" + image_name
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path_to_image , 0)

supported_formats = ['jpg',
                     'png',
                     'bmp']

def get_images(folder_path):
    files = os.listdir(folder_path)
    images = []
    for item in files:
        format = item.split('.')[1]
        if format in supported_formats:
            images.append(item)
    return images

def cmp_time(a:list, b:list) -> bool:
    if a[0] != b[0]:
        return a[0] >= b[0]
    if a[1] != b[1]:
        return a[1] >= b[1]
    if a[2] != b[2]:
        return a[2] >= b[2]
    return False

def delta_time(from_time:list, to_time:list) -> int:
    from_time_int = from_time[2] + (from_time[1] * 60) + (from_time[0] * 60 * 60)
    to_time_int = to_time[2] + (to_time[1] * 60) + (to_time[0] * 60 * 60)
    result = to_time_int - from_time_int
    if result < 0:
        result += 24 * 60 * 60
    return result

data = cfg.load_config()
mode = data.get('Changing mode')
if mode == 'Autostart only': #Autostart only
    theme = data.get('Fixed theme')
    theme_path = data.get("Themes").get(theme)
    images = get_images(theme_path)
    if len(images) > 0:
        change_wallpaper(theme_path, random.choice(images))
    exit()
elif mode == 'Fixed interval (random)': #Fixed interval (random)
    theme = data.get('Fixed theme')
    interval = data.get('Fixed interval')
    theme_path = data.get("Themes").get(theme)
    images = get_images(theme_path)
    current_image = ""
    if len(images) > 0:
        while True:
            new_image = random.choice(images)
            if current_image != new_image:
                current_image = new_image
                change_wallpaper(theme_path, current_image)
                if interval > 0:
                    time.sleep(interval)
                else: exit()
    exit()
elif mode == 'Fixed interval (linear)': #Fixed interval (linear)
    theme = data.get('Fixed theme')
    interval = data.get('Fixed interval')
    theme_path = data.get("Themes").get(theme)
    images = get_images(theme_path)
    current_image = ""
    if len(images) > 0:
        while True:
            for current_image in images:
                change_wallpaper(theme_path, current_image)
                if interval > 0:
                    time.sleep(interval)
                else: exit()
    exit()
elif mode == 'Change theme at time (random)':
    settings = list(data['Settings'].items())[::-1]
    if len(settings) > 0:
        last = list(deepcopy(settings[0]))
        last[1][0] = [0, 0, 0]
        last = tuple(last)
        settings.append(last)

        current_image = ""
        index_image = 0
        while True:
            current_time = datetime.datetime.now().time()
            current_time = [current_time.hour, current_time.minute, current_time.second]
            current_theme = ()
            index = 0
            for theme in settings:
                if cmp_time(current_time, theme[1][0]):
                    current_theme = theme
                    break
                index += 1
            #
            theme_path = data.get("Themes").get(current_theme[0])
            images = get_images(theme_path)
            time_to_sleep = min(delta_time(current_time, settings[index - 1][1][0]), #Time to next theme
                                delta_time([0, 0, 0], current_theme[1][1]))          #Interval
            
            new_image = random.choice(images)
            if current_image != new_image:
                current_image = new_image
                change_wallpaper(theme_path, current_image)
                if time_to_sleep > 0:
                    time.sleep(time_to_sleep)
                else: time.sleep(delta_time(current_time, settings[index - 1][1][0]))
    exit()

elif mode == 'Change theme at time (linear)':
    settings = list(data['Settings'].items())[::-1]
    if len(settings) > 0:
        last = list(deepcopy(settings[0]))
        last[1][0] = [0, 0, 0]
        last = tuple(last)
        settings.append(last)

        while True:
            current_time = datetime.datetime.now().time()
            current_time = [current_time.hour, current_time.minute, current_time.second]
            current_theme = ()
            index = 0
            for theme in settings:
                if cmp_time(current_time, theme[1][0]):
                    current_theme = theme
                    break
                index += 1
            #
            current_image = ""
            theme_path = data.get("Themes").get(current_theme[0])
            images = get_images(theme_path)
            time_to_sleep = min(delta_time(current_time, settings[index - 1][1][0]), #Time to next theme
                                delta_time([0, 0, 0], current_theme[1][1]))          #Interval
            
            new_image = images[index_image]
            if current_image != new_image:
                current_image = new_image
                change_wallpaper(theme_path, current_image)
                if time_to_sleep > 0:
                    if delta_time(current_time, settings[index - 1][1][0]) != time_to_sleep and index_image < len(images)-1:
                        index_image += 1
                    else: index_image = 0
                    time.sleep(time_to_sleep)
                else: 
                    index_image = 0
                    time.sleep(delta_time(current_time, settings[index - 1][1][0]))
    exit()
else:
    exit()