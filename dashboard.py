

from waveshare_epd import epd7in5_V2
from io import BytesIO
import json
import traceback
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import calendar
import d_functions
import dashboard_transit
import dashboard_weather
import os
import sys

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
icondir = os.path.join(picdir, 'icon')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')

# libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
# if os.path.exists(libdir):
#    sys.path.append(libdir)
# sys.path.append('lib')

epd = epd7in5_V2.EPD()


# Set the fonts
font20 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 20)
font22 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 22)
font26 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 26)
font30 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 30)
font35 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 35)
font45 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 45)
font50 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 50)

# Set the colors
black = 'rgb(0,0,0)'
white = 'rgb(255,255,255)'
grey = 'rgb(235,235,235)'


# Initialize and clear screen
print('Initializing and clearing screen.')
epd.init()
epd.Clear()


W_API_KEY = 'YOUR WEATHER API KEY'
T_API_KEY = 'YOUR TRANSLINK API KEY'
T_STOP_1 = 'STOP NO 1'
T_STOP_2 = 'STOP NO 2'
T_STOP_3 = 'STOP NO 3'
T_STOP_4 = 'STOP NO 4'
T_BUS = '2' #HOW MANY ESTIMATES WILL LOOK PER STOP
T_BUS_TIME = '600' #TIME TO LOOK BETWEEN ESTIMATES, 600 IS 10 HOURS 
LOCATION = 'YOUR LOCATION' #not using this for the moment, so you can leave it empty
LATITUDE = 'YOUR LATITUDE'
LONGITUDE = 'YOUR LONGITUDE'
UNITS = 'metric'#can be metric or imperial


WEATHER_URL = 'http://api.openweathermap.org/data/2.5/onecall?'
TRANSLINK_URL = 'http://api.translink.ca/RTTIAPI/V1/stops/'

bus_stop = []
w_info = []
t_stop_no = [T_STOP_1, T_STOP_2, T_STOP_3, T_STOP_4]

while True:
    s_x = 50
    s_x_inc = 25
    t_s_size = font22

    # API CALLS
    for x_stop in (t_stop_no):
        bus_stop.append(dashboard_transit.get_transit(
            TRANSLINK_URL, x_stop, T_API_KEY, T_BUS, T_BUS_TIME))

    w_info = (dashboard_weather.get_weather(WEATHER_URL, LATITUDE, LONGITUDE, UNITS, W_API_KEY))

    # Open template file
    template = Image.open(os.path.join(picdir, 'template.png'))
    # Initialize the drawing context with template as background
    draw = ImageDraw.Draw(template)

    # POPULATING TRANSIT
    draw.text((8, 10), 'TRANSIT', font=font30, fill=black)
    for x in range(len(bus_stop)):
        for y in (0, 1):
            if bus_stop[x][y] != "":
                draw.text((8, s_x), bus_stop[x][y], font=t_s_size, fill=black)
                # print(bus_stop[x][y])
                s_x = s_x+s_x_inc

   # POPULATING WEATHER
    draw.text((440, 10), w_info[0], font=font30, fill=black)
    draw.text((510, 55), w_info[1], font=font45, fill=black)
    draw.text((610, 55), w_info[3], font=font22, fill=black)
    draw.text((610, 80), w_info[2], font=font22, fill=black)
    draw.text((515, 130), w_info[10], font=font22, fill=black)
    draw.text((515, 155), w_info[11] + ' ' + w_info[13], font=font22, fill=black)
    draw.text((515, 190), w_info[14], font=font22, fill=black)
    draw.text((515, 215), w_info[15] + ' ' + w_info[17], font=font22, fill=black)

    icon_file = str(w_info[4]) + '.png'
    icon_image = Image.open(os.path.join(icondir, icon_file))
    template.paste(icon_image, (440, 45))

    icon_file = str(w_info[12]) + '.png'
    icon_image = Image.open(os.path.join(icondir, icon_file))
    template.paste(icon_image, (440, 120))

    icon_file = str(w_info[16]) + '.png'
    icon_image = Image.open(os.path.join(icondir, icon_file))
    template.paste(icon_image, (440, 180))

   # POPULATING CALENDAR
    cal_month = datetime.now().month
    cal_year = datetime.now().year
    cal_day = datetime.now().day
    cal_n_m = calendar.month_name[cal_month]
    cal_text = calendar.TextCalendar(calendar.SUNDAY)
    cal_list = cal_text.monthdayscalendar(cal_year, cal_month)
    cal_s_x = 440
    cal_s_y = 325

    draw.text((500, 260), str(cal_n_m) + ' ' + str(cal_year), font=font35, fill=black)
    draw.text((440, 300), 'SU    MO    TU   WED  THU   FRI   SAT', font=font22, fill=black)

    for cal_x in (0, 1, 2, 3, 4):
        for cal_y in (0, 1, 2, 3, 4, 5, 6):
            if cal_list[cal_x][cal_y] != 0:
                if cal_list[cal_x][cal_y] == cal_day:
                    draw.rectangle((cal_s_x, cal_s_y, cal_s_x+22, cal_s_y+22), fill=black)
                    draw.text((cal_s_x, cal_s_y), str(
                        cal_list[cal_x][cal_y]), font=font22, fill=white, align='right')
                else:
                    draw.text((cal_s_x, cal_s_y), str(
                        cal_list[cal_x][cal_y]), font=font22, fill=black, align='right')
            cal_s_x = cal_s_x + 55
        cal_s_x = 440
        cal_s_y = cal_s_y + 30

    # DRAWING BOUNDARIES
    draw.line((425, 0, 425, 500), fill=0, width=2)
    draw.line((0, 260, 900, 260), fill=0, width=2)

    '''

	# Draw bottom right box
	draw.text((627, 330), 'UPDATED', font=font35, fill=white)
	current_time = datetime.now().strftime('%I:%M')
	draw.text((627, 375), current_time, font=font60, fill=white)

	'''

    # Save the image for display as PNG
    screen_output_file = os.path.join(picdir, 'screen_output.png')
    template.save(screen_output_file)
    # Close the template file
    template.close()

    # Write to screen, refresh in 300 seconds / 5 min
    d_functions.write_to_screen(screen_output_file, 300)
    bus_stop.clear()
    w_info.clear()
