
"""Retrieve and display weather."""

import os
from PIL import Image
from modules import d_functions as d_f


def get_weather(WEATHER_URL, LATITUDE, LONGITUDE, UNITS, W_API_KEY, color):
    """Retrieve the weather from openweathermap."""

    W_URL = WEATHER_URL + 'lat=' + LATITUDE + '&lon=' + \
        LONGITUDE + '&units=' + UNITS + '&appid=' + W_API_KEY + \
        '&exclude=hourly,minutely,alerts'
    # print(W_URL)

    weather_data = []
    response_w = d_f.url_content(W_URL, 'weather', {}, color)
    if response_w:
        w_data = response_w.json()
        current = w_data['current']
        utc_time = current['dt']
        day_name = d_f.get_time(utc_time)
        temp_current = current['temp']
        #feels_like = current['feels_like']
        #humidity = current['humidity']
        #wind = current['wind_speed']
        weather = current['weather']
        report = weather[0]['description']
        icon_code = weather[0]['icon']
        # icon_URL = 'http://openweathermap.org/img/wn/'+ icon_code +'@4x.png'
        # get daily dict block
        daily = w_data['daily']
        #daily_precip_float = daily[0]['pop']
        #daily_precip_percent = daily_precip_float * 100
        daily_temp = daily[0]['temp']
        temp_max = daily_temp['max']
        temp_min = daily_temp['min']

        if UNITS == "metric":
            unit = "C"
        elif UNITS == "imperial":
            unit = "F"

        weather_data.append('Today is ' + str(day_name))
        weather_data.append(str(format(temp_current, '.0f')) + u'\N{DEGREE SIGN}' + str(unit))
        # weather_data.append('Feels Like: ' + str(feels_like))
        # weather_data.append('Humidity: ' + str(humidity))
        # weather_data.append('Wind Speed: '+str(wind))
        if str(report.title()) == 'Heavy Intensity Rain':
            weather_data.append('Heavy Rain')
        else:
            weather_data.append(str(report.title()))
        weather_data.append(str(format(temp_max, '.0f')) +
                            u'\N{DEGREE SIGN}' + str(unit)+' / ' + str(format(temp_min, '.0f')) + u'\N{DEGREE SIGN}' + str(unit))
        # weather_data.append('Probabilty of Precipitation: ' +
        #                    str(daily_precip_percent) + '%')
        weather_data.append(str(icon_code))
        weather_data.append("Forecast")
        for x in range(0, 5):
            weather_data.append(str(d_f.get_time(daily[x]['dt'])))
            weather_data.append(str(format(daily[x]['temp']['max'], '.0f')) +
                                u'\N{DEGREE SIGN}' + str(unit)+' / ' + str(format(daily[x]['temp']['min'], '.0f')) + u'\N{DEGREE SIGN}' + str(unit))
            weather_data.append(daily[x]['weather'][0]['icon'])
            if daily[x]['weather'][0]['description'] == 'heavy intensity rain':
                weather_data.append('heavy rain')
            else:
                weather_data.append(daily[x]['weather'][0]['description'])

    return weather_data


def draw_weather_mod(w_s_x, w_s_y, w_info, color, picdir, template, draw):
    """Place weather report on the canvas."""

    icondir = os.path.join(picdir, 'icon')
    draw.text((w_s_x, w_s_y), w_info[0], font=d_f.font_size(28), fill=color)
    draw.text((w_s_x + 70, w_s_y + 45), w_info[1], font=d_f.font_size(45), fill=color)
    draw.text((w_s_x + 160, w_s_y + 45), w_info[3], font=d_f.font_size(22), fill=color)
    draw.text((w_s_x + 160, w_s_y + 70), w_info[2], font=d_f.font_size(22), fill=color)
    draw.text((w_s_x + 75, w_s_y + 110), w_info[10], font=d_f.font_size(22), fill=color)
    draw.text((w_s_x + 75, w_s_y + 135), w_info[11] +
              ' ' + w_info[13], font=d_f.font_size(22), fill=color)
    draw.text((w_s_x + 75, w_s_y + 180), w_info[14], font=d_f.font_size(22), fill=color)
    draw.text((w_s_x + 75, w_s_y + 205), w_info[15] +
              ' ' + w_info[17], font=d_f.font_size(22), fill=color)

    icon_file = str(w_info[4]) + '.png'
    icon_image = Image.open(os.path.join(icondir, icon_file))
    template.paste(icon_image, (w_s_x, w_s_y + 35))

    icon_file = str(w_info[12]) + '.png'
    icon_image = Image.open(os.path.join(icondir, icon_file))
    template.paste(icon_image, (w_s_x, w_s_y + 110))

    icon_file = str(w_info[16]) + '.png'
    icon_image = Image.open(os.path.join(icondir, icon_file))
    template.paste(icon_image, (w_s_x, w_s_y + 170))


def run_weather_mod(WEATHER_URL, LATITUDE, LONGITUDE, UNITS, W_API_KEY, mod_w_s_x, mod_w_s_y,  picdir, template, draw, color):
    """Call functions to retrieve and display weather."""

    w_info_array = (get_weather(WEATHER_URL, LATITUDE, LONGITUDE, UNITS, W_API_KEY, color))
    draw_weather_mod(mod_w_s_x, mod_w_s_y, w_info_array, color, picdir, template, draw)
