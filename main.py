import os
import random
import textwrap
import sys

import xkcd as xkcd
from PIL import Image
from Adafruit_Thermal import *

image_directory = "./Images"
max_width = 384

def get_latest_or_random_unread_comic():
    max_comic_count = xkcd.getLatestComicNum()
    previous_comic_ids = {}
    for file_name in os.listdir(image_directory):
        key = int(file_name.replace(".png", "").replace(".bmp", ""))
        if key not in previous_comic_ids:
            previous_comic_ids[key] = True

    unread_comic_ids = []
    for i in range(max_comic_count):
        i = i+1
        if i not in previous_comic_ids:
            unread_comic_ids.append(i)

    if max_comic_count not in previous_comic_ids:
        print("Fetching latest comic.")
        return max_comic_count
    print("No new comics. Fetching random comic.")
    random.shuffle(unread_comic_ids)
    return unread_comic_ids[0]

def resize_comic_and_return_data(comic_id):
    with Image.open('{}/{}.png'.format(image_directory, comic_id)) as image_file:
        width, height = image_file.size
        print("Old size is {} by {}".format(width, height))

        if width > height:
            image_file = image_file.rotate(-90)
            width, height = image_file.size
            print("Rotating. Size is now {} by {}".format(width, height))

        scale_factor = float(max_width) / float(width)
        print("Scaling by a factor of {}".format(scale_factor))
        new_height = int(scale_factor * height)

        print("New size is {} by {}".format(max_width, new_height))

        image_file = image_file.resize((max_width, new_height), Image.ANTIALIAS)

        image_file = image_file.convert('1')  # convert image to black and white
        image_file = image_file.point(lambda x: 0 if x < 60 else 255, '1')
        image_filename = '{}/{}.bmp'.format(image_directory, comic_id)
        image_file.save(image_filename)
        return image_file

def print_wrapped(printer, text, size):
    printer.setSize(size)
    for line in textwrap.wrap(text, printer.maxColumn):
        printer.println(line)

# Get a comic
comic = xkcd.getComic(get_latest_or_random_unread_comic())
comic_id = comic.number

# Print info to console and download
print("#{} - {}".format(comic_id, comic.getAsciiTitle()))
print(comic.getAsciiAltText())
comic.download(output=image_directory, outputFile='{}.png'.format(comic_id))

image = resize_comic_and_return_data(comic_id)

# Print to thermal printer
printer = Adafruit_Thermal("/dev/ttyUSB0", 19200, timeout=5)
printer.online()
printer.reset()

printer.justify('C')
print_wrapped(printer, comic.getAsciiTitle(), 'L')

printer.printImage(image)

printer.justify('L')
print_wrapped(printer, "#{}: {}".format(comic_id, comic.getAltText()), 'S')

printer.feed(2)
printer.offline()
