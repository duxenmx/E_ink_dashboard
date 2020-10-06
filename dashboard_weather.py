import requests
import d_functions


def get_weather(WEATHER_URL, LATITUDE, LONGITUDE, UNITS, W_API_KEY):
    W_URL = WEATHER_URL + 'lat=' + LATITUDE + '&lon=' + \
        LONGITUDE + '&units=' + UNITS + '&appid=' + W_API_KEY + \
        '&exclude=hourly,minutely,alerts'
    # print(W_URL)
    error_connect = True
    while error_connect == True:
        try:
            # HTTP request
            # print('Attempting to connect to OWM.')
            response_w = requests.get(str(W_URL))
            error_connect = None
        except:
            # Call function to display connection error
            print('Connection error.')
            # error_connect = None
            # error = True
            d_functions.display_error(' WEATHER CONNECTION')
            # break
        # delete the comment below
        #
    error = None
    while error == None:
        # Check status of code request
        if response_w.status_code == 200:
            # print('Connection to Open Weather successful.')
            w_data = response_w.json()
            current = w_data['current']
            utc_time = current['dt']
            day_name = d_functions.get_time(utc_time)
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

            weather_data = []
            weather_data.append('Today is ' + str(day_name))
            weather_data.append(str(format(temp_current, '.0f')) + u'\N{DEGREE SIGN}C')
            # weather_data.append('Feels Like: ' + str(feels_like))
            # weather_data.append('Humidity: ' + str(humidity))
            # weather_data.append('Wind Speed: '+str(wind))
            weather_data.append(str(report.title()))
            weather_data.append(str(format(temp_max, '.0f')) +
                                u'\N{DEGREE SIGN}C / ' + str(format(temp_min, '.0f')) + u'\N{DEGREE SIGN}C')
            # weather_data.append('Probabilty of Precipitation: ' +
            #                    str(daily_precip_percent) + '%')
            weather_data.append(str(icon_code))
            weather_data.append("Forecast")
            for x in [0, 1, 2, 3, 4]:
                weather_data.append(str(d_functions.get_time(daily[x]['dt'])))
                weather_data.append(str(format(daily[x]['temp']['max'], '.0f')) +
                                    u'\N{DEGREE SIGN}C / ' + str(format(daily[x]['temp']['min'], '.0f')) + u'\N{DEGREE SIGN}C')
                weather_data.append(daily[x]['weather'][0]['icon'])
                weather_data.append(daily[x]['weather'][0]['description'])
            return weather_data

            error = True

        else:
            # Call function to display HTTP error
            d_functions.display_error('HTTP')
            # delete the comment above and delete the break
            # break
