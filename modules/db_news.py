#!/usr/bin/python
# -*- coding:utf-8 -*-

# importing the required libraries
import requests
# from PIL import Image, ImageDraw, ImageFont
from modules import d_functions as d_f


the_news = []


def get_news(NEWS_URL, NEWS_API, NEWS_SOURCES, news_country, news_num, color):
    if news_num == 0:
        news_URL = str(NEWS_URL) + "country="+str(news_country).lower() + "&apiKey=" + str(NEWS_API)
    elif news_num == 1:
        news_URL = str(NEWS_URL) + "sources="+str(NEWS_SOURCES) + "&apiKey=" + str(NEWS_API)
    # print(news_URL)
    error_connect = True
    # print(news_URL)
    while error_connect == True:
        try:
            # HTTP request
            # print('Attempting to connect to OWM.')
            response_n = requests.get(str(news_URL))
            error_connect = None
        except:
            # Call function to display connection error
            print('Connection error.')
            # error_connect = None
            # error = True
            d_f.display_error(' NEWS CONNECTION', color)
            # break
        # delete the comment below
        #
    error = None
    while error == None:
        # Check status of code request
        if response_n.status_code == 200:
            # print('Connection to Open Weather successful.')
            n_data = response_n.json()
            # print(n_data)
            news_items = []

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
                    chk_str = chk_str
                    check = True

                #print("after: " + str(chk_str))

                while check is False:
                    if str(n_data["articles"][x]["title"])[chk_str] != " ":
                        chk_str = chk_str - 1
                        #print("space_false: " + str(chk_str))
                        check = False
                    else:
                        chk_str = chk_str
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
            error = True

        else:
            d_f.display_error('NEWS HTTP', color)
            # Call function to display HTTP error
            # break


def draw_news_mod(news_s_x, news_s_y, the_news, color, draw):
    draw.text((news_s_x, news_s_y),  'The News', font=d_f.font_size(20), fill=color)
    news_s_y = news_s_y+24
    for x in range(len(the_news)):
        if the_news[x] != "":
            draw.text((news_s_x, news_s_y), the_news[x], font=d_f.font_size(18), fill=color)
            news_s_y = news_s_y + 22


def run_news_mod(NEWS_URL, NEWS_API, NEWS_SOURCES,
                 news_country,  mod_t_s_x, mod_t_s_y, draw, color):
    the_news = get_news(NEWS_URL, NEWS_API, NEWS_SOURCES, news_country, color)
    # POPULATING TRANSIT

    draw_news_mod(mod_t_s_x, mod_t_s_y, the_news, color, draw)
    the_news.clear()
