import ctypes
import random
import os
import config_manager as cfg
import time


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

#Sample path
mypath = "C:/Users/User/Documents/GitHub/WallpaperRollProject/SampleTheme"
f = os.listdir(mypath)

#interval = 5
#t = monotonic()
#while True:
#    if monotonic() - t > interval:
#        t = monotonic()
#
#        change_wallpaper(mypath, random.choice(f))
#        print("Changed")

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
                time.sleep(interval)
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
                time.sleep(interval)
    exit()
else:
    exit()