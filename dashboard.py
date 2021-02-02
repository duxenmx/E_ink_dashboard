#!/usr/bin/env python3
"""Main program that displays the dashboard on the E-ink display."""

import json
import time
import os
# import traceback
from datetime import datetime
from PIL import Image, ImageDraw
from waveshare_epd import epd7in5_V2
from modules import d_functions as d_f
from modules import db_transit as d_t
from modules import db_tasklist as d_tl
from modules import db_g_meetings as d_gm
from modules import db_weather as d_w
from modules import db_news as d_n
from modules import db_curr_stock as d_cs
from modules import db_geolocation as d_geo
from modules import db_spotify as d_spot


picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
creddir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'credentials')

epd = epd7in5_V2.EPD()

# Set the colors
black = 'rgb(0,0,0)'
white = 'rgb(255,255,255)'

# Initialize and clear screen
print('Initializing and clearing screen.')
# epd.init()
# epd.Clear()

geo_data = []
check_awake = 0
mod_1_turn = 1
mod_2_turn = 1
mod_3_turn = 1
mod_4_turn = 1
news_load = 0
cs_load = 0
geo_load = 0
saved_hour = int(datetime.now().strftime('%H'))
news_0 = []
news_1 = []
stock_it = []
curr_ex = []


while True:
    epd.init()
    with open(os.path.join(creddir, 'dash_id.json'), "r") as rdash_id:
        data = json.load(rdash_id)
    # Getting time information to know when its supposed to be active
    awake = data["System"]["awake"].lower()  # for testing mode to activate within sleeping hours
    refresh_sec = int(data["System"]["refresh_time"])  # time in seconds
    waking_time = int(data["System"]["waking_time"])  # time in hours, 24h mode
    sleep_time = int(data["System"]["sleeping_time"])  # time in hours, 24h mode
    mod_1_choice = str(data["System"]["mod_1_choice"]).lower()
    mod_2_choice = str(data["System"]["mod_2_choice"]).lower()
    mod_3_choice = str(data["System"]["mod_3_choice"]).lower()
    mod_4_choice = str(data["System"]["mod_4_choice"]).lower()
    if d_f.time_in_range(waking_time, sleep_time) or awake == "true":
        check_awake = 0
        current_time = datetime.now().strftime('%I:%M%p')
        current_hour = int(datetime.now().strftime('%H'))
        # Open template file
        template = Image.open(os.path.join(picdir, 'template.bmp'))
        # Initialize the drawing context with template as background
        draw = ImageDraw.Draw(template)

        # populating the ids from the json file
        if geo_load == 0:
            geo_data.clear()
            geo_data = d_geo.get_geo(str(data["Geolocation"]["G_URL"]), str(
                data["Geolocation"]["G_API_KEY"]), black)
            geo_load = 1

        W_API_KEY = str(data["Weather"]["W_API_KEY"])
        T_API_KEY = str(data["Transit"]["T_API_KEY"])
        t_stop_no = data["Transit"]["Stops"]
        T_BUS = str(data["Transit"]["T_BUS"])
        T_BUS_TIME = str(int(data["Transit"]["T_BUS_TIME"])*60)

        LOCATION = str(geo_data[0]) + ", " + str(geo_data[1])
        LATITUDE = str(geo_data[3])
        LONGITUDE = str(geo_data[4])
        LOCAL_CUR = str(geo_data[5])
        UNITS = str(data["Weather"]["UNITS"])
        WEATHER_URL = str(data["Weather"]["W_URL"])
        TRANSLINK_URL = str(data["Transit"]["T_URL"])

        gsheetjson = str(data["Tasklist"]["gsheet_json"])
        sheetname = str(data["Tasklist"]["sheetname"])
        meet_creds = str(data["G_Meetings"]["CREDENTIALS_FILE"])

        NEWS_URL = str(data["News"]["NEWS_URL"])
        NEWS_API = str(data["News"]["NEWS_API"])
        NEWS_SOURCES = str(data["News"]["NEWS_SOURCES"])
        NEWS_COUNTRY = str(geo_data[7])

        C_1_URL = str(data["Currency"]["C_URL_1"])
        C_3_URL = str(data["Currency"]["C_URL_3"])
        C_4_URL = str(data["Currency"]["C_URL_4"])
        C_1_API = str(data["Currency"]["C_API_KEY_1"])
        CURR_CHECK = data["Currency"]["CURR_CHECK"]

        ST_W_URL = str(data["Stocks"]["STOCK_W_URL"])
        ST_WE_URL = str(data["Stocks"]["STOCK_WE_URL"])
        ST_API = str(data["Stocks"]["STOCK_API"])
        ST_C = data["Stocks"]["STOCK_CHECK"]

        mod_1_turn = d_f.choose_mod(mod_1_choice, mod_1_turn)
        mod_2_turn = d_f.choose_mod(mod_2_choice, mod_2_turn)
        mod_3_turn = d_f.choose_mod(mod_3_choice, mod_3_turn)

        if saved_hour != current_hour:
            news_load = 0
            cs_load = 0
            saved_hour = current_hour
            news_1.clear()
            news_0.clear()
            stock_it.clear()
            curr_ex.clear()

        # TRANSIT  CALLS or news calls
        if mod_1_turn == 0:
            mod_t_s_x = 8
            mod_t_s_y = 50

            print('Transit loaded')

            d_t.run_transit_mod(TRANSLINK_URL, t_stop_no, T_API_KEY, T_BUS,
                                T_BUS_TIME,  LOCATION,  mod_t_s_x, mod_t_s_y, draw, black)

        elif mod_1_turn == 1:
            # news calls
            mod_t_s_x = 10
            mod_t_s_y = 10

            if news_load == 0:
                #print("news by country")
                news_0 = d_n.get_news(NEWS_URL, NEWS_API, NEWS_SOURCES, NEWS_COUNTRY, 0, black)
                #print("news by source")
                news_1 = d_n.get_news(NEWS_URL, NEWS_API, NEWS_SOURCES, NEWS_COUNTRY, 1, black)
                news_load = 1
                print("news retrieved at " + str(saved_hour))

            print('News loaded')

            if (d_f.tir_min(int(current_hour), 0, 15, 59) or d_f.tir_min(int(current_hour), 30, 45, 59)) and news_load == 1:
                d_n.draw_news_mod(mod_t_s_x, mod_t_s_y, news_0, black, draw)
            elif (d_f.tir_min(int(current_hour), 15, 30, 59) or d_f.tir_min(int(current_hour), 45, 59, 59)) and news_load == 1:
                d_n.draw_news_mod(mod_t_s_x, mod_t_s_y, news_1, black, draw)

        elif mod_1_turn == 2:
            mod_t_s_x = 8
            mod_t_s_y = 50

            print('Spotify loaded')

            spoti_data = d_spot.get_spot_info()
            d_spot.draw_music_mod(mod_t_s_x, mod_t_s_y, spoti_data, black, draw, template)
            if spoti_data[0] == 'track':
                refresh_sec = float(spoti_data[1])/60
            elif spoti_data[0] == 'ad':
                refresh_sec = 10/60

        elif mod_1_turn == 3:
            print("Module 1 is off")

        # Weather or currency-stock
        if mod_2_turn == 0:

            mod_w_s_x = 440
            mod_w_s_y = 10
            print('Weather loaded')
            d_w.run_weather_mod(WEATHER_URL, LATITUDE, LONGITUDE, UNITS, W_API_KEY,
                                mod_w_s_x, mod_w_s_y,  picdir, template, draw, black)
        elif mod_2_turn == 1:
            mod_w_s_x = 440
            mod_w_s_y = 10

            if cs_load == 0:
                curr_ex, stock_it = d_cs.run_st_cur_info(
                    C_1_URL, C_3_URL, C_4_URL, LOCAL_CUR, CURR_CHECK,  C_1_API, ST_WE_URL, ST_W_URL, ST_API, ST_C, black)
                cs_load = 1
                print("C-S retrieved at " + str(saved_hour))

            print('C-S loaded')

            if d_f.tir_min(int(current_hour), 0, 59, 59) and cs_load == 1:
                d_cs.draw_cs_mod(mod_w_s_x, mod_w_s_y, draw, curr_ex, stock_it, LOCAL_CUR, black)
        elif mod_2_turn == 3:
            print("Module 2 is off")

        # populate Tasklist or meetings
        if mod_3_turn == 0:
            mod_tl_s_x = 10
            mod_tl_s_y = 265
            d_tl.run_tasklist_mod(gsheetjson, sheetname, creddir,
                                  mod_tl_s_x, mod_tl_s_y, draw, black)
            print('Tasklist loaded')
            draw.rectangle((8, 450, 175, 475), fill=black)
            draw.text((8, 450), 'UPDATED: ' + str(current_time), font=d_f.font_size(20), fill=white)
        elif mod_3_turn == 1:
            mod_tl_s_x = 10
            mod_tl_s_y = 265
            d_gm.run_meeting_mod(meet_creds, creddir, mod_tl_s_x, mod_tl_s_y, draw, black)
            print('Meetings loaded')
            draw.rectangle((250, 260, 430, 290), fill=black)
            draw.text((255, 260), 'UPDATED: ' + str(current_time),
                      font=d_f.font_size(20), fill=white)
        elif mod_3_turn == 3:
            print("Module 3 is off")

        # Populate the calendar module
        mod_c_s_x = 440
        mod_c_s_y = 325
        d_f.draw_cal_mod(mod_c_s_x, mod_c_s_y, draw, black, white)

        # DRAWING BOUNDARIES
        draw.line((430, 0, 430, 500), fill=0, width=2)
        draw.line((0, 260, 900, 260), fill=0, width=2)

        # do not remove this commented area, testing how it works without saving everything
        # in an image at the end,
        # Save the image for display as PNG
        #screen_output_file = os.path.join(picdir, 'screen_output.bmp')
        # template.save(screen_output_file)
        # Close the template file
    #    template.close()

        # Write to screen next in 300 seconds
        #d_f.write_to_screen(screen_output_file, int(refresh_sec*60))
        d_f.write_to_screen(template, int(refresh_sec*60))

    # if the device is in sleeping hours it will clean the screen to prevent burn out of the screen
    else:
        print('Device Sleeping.')
        if check_awake == 0:
            check_awake = 1
            epd.Clear()
            epd.sleep()
            print('Sleeping for ' + str(refresh_sec) + ' min.')
            time.sleep(refresh_sec*60)
        else:
            # use this else to prevent constant screen refreshing once its sleeping, it will just keep sleeping for 5 more minutes, like me every morning....
            print('Sleeping for ' + str(refresh_sec) + ' min.')
            epd.sleep()
            time.sleep(refresh_sec*60)
