

import time
import datetime
from datetime import datetime
from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
icondir = os.path.join(picdir, 'icon')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')

epd = epd7in5_V2.EPD()

font22 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 22)
font50 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 50)
# Set the colors
black = 'rgb(0,0,0)'


def get_time(local_time):
    pst_time = time.localtime(int(local_time))
    pst_time = time.strftime('%A, %b %d', pst_time)
    return pst_time


def isTimeFormat(input):
    try:
        time.strptime(input, '%I:%M%p %Y-%m-%d')
        return True
    except ValueError:
        return False

# define funciton for writing image and sleeping for 5 min.


def write_to_screen(image, sleep_seconds):
    print('Writing to screen.')
    # Write to screen
    h_image = Image.new('1', (epd.width, epd.height), 255)
    # Open the template
    screen_output_file = Image.open(os.path.join(picdir, image))
    # Initialize the drawing context with template as background
    h_image.paste(screen_output_file, (0, 0))
    epd.display(epd.getbuffer(h_image))
    # Sleep
    print('Sleeping for ' + str(sleep_seconds) + '.')
    time.sleep(sleep_seconds)

# define function for displaying error


def display_error(error_source):
    # Display an error
    print('Error in the', error_source, 'request.')
    # Initialize drawing
    error_image = Image.new('1', (epd.width, epd.height), 255)
    # Initialize the drawing
    draw = ImageDraw.Draw(error_image)
    draw.text((100, 150), error_source + ' ERROR', font=font50, fill=black)
    draw.text((100, 300), 'Retrying in 30 seconds', font=font22, fill=black)
    current_time = datetime.now().strftime('%H:%M')
    draw.text((300, 365), 'Last Refresh: ' + str(current_time), font=font50, fill=black)
    # Save the error image
    error_image_file = 'error.png'
    error_image.save(os.path.join(picdir, error_image_file))
    # Close error image
    error_image.close()
    # Write error to screen
    write_to_screen(error_image_file, 30)
