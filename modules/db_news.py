#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""Retrieve and display news headlines."""

# importing the required libraries
#import requests		#No longer needed in this module
# from PIL import Image, ImageDraw, ImageFont
from modules import d_functions as d_f


#the_news = []		#Does not need to be defined here - parameter in draw_news_mod, local variable in run_news_mod


def get_news(NEWS_URL, NEWS_API, NEWS_SOURCES, news_country, news_num, color):
    """Retrieve news."""
    if news_num == 0:
        news_URL = str(NEWS_URL) + "country="+str(news_country).lower() + "&apiKey=" + str(NEWS_API)
    elif news_num == 1:
        news_URL = str(NEWS_URL) + "sources="+str(NEWS_SOURCES) + "&apiKey=" + str(NEWS_API)
    # print(news_URL)

    #Following block replaced by "response_g = .../if response_g:" lines
    #error_connect = True
    #while error_connect:
    #    try:
    #       # HTTP request
    #        # print('Attempting to connect to OWM.')
    #        response_n = requests.get(str(news_URL))
    #        error_connect = None
    #    except:
    #        # Call function to display connection error
    #        print('Connection error.')
    #        # error_connect = None
    #        d_f.display_error(' NEWS CONNECTION', color)
    #        # break
    #    # delete the comment below
    #    #
    #error = None
    #while error is None:
    #    # Check status of code request
    #    if response_n.status_code != 200:
    #        d_f.display_error('NEWS HTTP', color)
    #        # Call function to display HTTP error
    #        # break
    #    else:



    news_items = []
    response_n = d_f.url_content(news_URL, 'news', {}, color)
    if response_n:
        # print('Connection to News successful.')
        n_data = response_n.json()
        # print(n_data)

        for x in range(0, 5):
            chk_str = int(len(str(n_data["articles"][x]["title"])))
            chk_str_1 = chk_str
            # print(x)
            #print("before: " + str(chk_str))
            # 43
            check = False
            if chk_str > 48:
                chk_str = 48
            else:
                #chk_str = chk_str			#Does no action
                check = True

            #print("after: " + str(chk_str))

            while check is False:
                if str(n_data["articles"][x]["title"])[chk_str] != " ":
                    chk_str = chk_str - 1
                    #print("space_false: " + str(chk_str))
                    check = False
                else:
                    #chk_str = chk_str		#Does no action
                    #print("space_true: " + str(chk_str))
                    check = True

            if chk_str_1 >= 48:
                news_items.append(str(x+1) + "- " +
                                  str(n_data["articles"][x]["title"])[0:chk_str] + " ")
                if chk_str_1 > 92:
                    news_items.append(str(n_data["articles"][x]["title"])[chk_str+1:91] + " ")
                else:
                    news_items.append(str(n_data["articles"][x]["title"])[
                                      chk_str+1:chk_str_1] + " ")
            else:
                news_items.append(str(x+1) + "- " +
                                  str(n_data["articles"][x]["title"])[0:chk_str] + " ")
            # print(news_items[x])

    return news_items



def draw_news_mod(news_s_x, news_s_y, the_news, color, draw):
    """Draw headlines on the canvas."""
    draw.text((news_s_x, news_s_y),  'The News', font=d_f.font_size(20), fill=color)
    news_s_y = news_s_y+24
    for x in range(len(the_news)):
        if the_news[x] != "":
            draw.text((news_s_x, news_s_y), the_news[x], font=d_f.font_size(18), fill=color)
            news_s_y = news_s_y + 22


def run_news_mod(NEWS_URL, NEWS_API, NEWS_SOURCES,
                 news_country,  mod_t_s_x, mod_t_s_y, draw, color):
    """Call functions to get and display news."""
    news_num = 0		#FIXME - this values was missing in the get_news call below.  Not sure where to get it.  dashboard.py appears to call this twice, once set to 0, other set to 1.
    news_array = get_news(NEWS_URL, NEWS_API, NEWS_SOURCES, news_country, news_num, color)

    draw_news_mod(mod_t_s_x, mod_t_s_y, news_array, color, draw)
    #news_array.clear()			#Not needed as this is cleared on function exit.
