"""Show transit system times."""

import datetime
from datetime import timedelta
import requests
from modules import d_functions as d_f


def route_format(t_route_dest):
    """Shorten destinations to save space."""

    # add more route name formatting to your choice to save dsiplay space
    # If there's a substitution in the dictionary, use it, otherwise return the original
    return {"TO GRANVILLE": "GRANVILLE", "COMM'L-BDWAY STN": "COM-BW STN"}.get(t_route_dest, t_route_dest)


def ELT_format(ELT):
    """time separation, api info gives time and date"""

    if d_f.isTimeFormat(ELT):
        t_sch_ELT = datetime.datetime.strptime(
            str(ELT), '%I:%M%p %Y-%m-%d')
        t_sch_elt_t_0 = t_sch_ELT.time()
        t_sch_elt_t = t_sch_elt_t_0.strftime("%I:%M%p")
    else:
        t_sch_elt_t = ELT
    return t_sch_elt_t


def EC_format(EC):
    """api returns time in minutes, to save space we convert them into hours if above of 60"""

    if EC < 60:
        EC_time = ' min'
    else:
        EC_time = ' hours'
    if EC >= 0:
        t_sch_EC = str(timedelta(minutes=EC))[:-3]
    else:
        t_sch_EC = EC
    return t_sch_EC, EC_time


def get_transit(TRANSLINK_URL, T_STOP, T_API_KEY, T_BUS, T_BUS_TIME, color):
    """Download transit schedule."""

    T_URL = TRANSLINK_URL+T_STOP + '/estimates?apiKey=' + \
        T_API_KEY + '&count=' + T_BUS + '&timeframe=' + T_BUS_TIME
    # print(T_URL)
    error_connect = True
    while error_connect is True:
        try:
            # HTTP request
            # print('Attempting to connect to Translink.')
            response_t = requests.get(str(T_URL), headers={'Accept': 'application/JSON'})
            # print('Connection to Translink successful.')
            error_connect = None
        except:
            # Call function to display connection error
            print('Connection error.')
            response_t = ''
            d_f.display_error('TRANSIT CONNECTION', color)
    error = None
    while error is None:
        # Check status of code request
        if response_t.status_code == 200:
            # print('Connection to Translink successful.')
            t_data = response_t.json()
            # print(t_data)
            t_route_no = t_data[0]['RouteNo']
            t_schedules = t_data[0]['Schedules']

            bus_sch = []
            est_counter = 0

            if int(t_schedules[0]['ExpectedCountdown']) >= 0:
                t_route_dest_0 = route_format(t_schedules[0]['Destination'])
                t_sch_elt_t_0 = ELT_format(t_schedules[0]['ExpectedLeaveTime'])
                t_sch_EC_0, EC_0_time = EC_format(t_schedules[0]['ExpectedCountdown'])
                bus_sch.append(str(t_route_no) + "-"+str(t_route_dest_0) + " in " +
                               str(t_sch_EC_0) + EC_0_time + " at " + str(t_sch_elt_t_0))
                est_counter = est_counter + 1

            if int(t_schedules[1]['ExpectedCountdown']) >= 0:
                t_route_dest_1 = route_format(t_schedules[1]['Destination'])
                t_sch_elt_t_1 = ELT_format(t_schedules[1]['ExpectedLeaveTime'])
                t_sch_EC_1, EC_1_time = EC_format(t_schedules[1]['ExpectedCountdown'])
                bus_sch.append(str(t_route_no) + "-"+str(t_route_dest_1) + " in " +
                               str(t_sch_EC_1) + EC_1_time + " at " + str(t_sch_elt_t_1))
                est_counter = est_counter + 1

            if int(t_schedules[2]['ExpectedCountdown']) >= 0 and est_counter < 2:
                t_route_dest_2 = route_format(t_schedules[2]['Destination'])
                t_sch_elt_t_2 = ELT_format(t_schedules[2]['ExpectedLeaveTime'])
                t_sch_EC_2, EC_2_time = EC_format(t_schedules[2]['ExpectedCountdown'])
                bus_sch.append(str(t_route_no) + "-"+str(t_route_dest_2) + " in " +
                               str(t_sch_EC_2) + EC_2_time + " at " + str(t_sch_elt_t_2))
                est_counter = est_counter + 1

            t_data.clear()
            t_schedules.clear()

            return bus_sch

        else:
            # Call function to display HTTP error
            response_t = ''
            d_f.display_error('HTTP TRANSIT', color)


def draw_transit_mod(tran_s_x, tran_s_y, bus_stop_data, LOCATION, color, draw):
    """Place bus schedule on canvas."""

    draw.text((tran_s_x, tran_s_y-40), LOCATION +
              ' - TRANSLINK', font=d_f.font_size(30), fill=color)
    for x in range(len(bus_stop_data)):
        for y in range(len(bus_stop_data[x])):
            #print("x:" + str(x) + " y: " + str(y))
            if bus_stop_data[x][y]:
                draw.text((tran_s_x, tran_s_y), bus_stop_data[x][y],
                          font=d_f.font_size(22), fill=color)
                # print(bus_stop_data[x][y])
                tran_s_y = tran_s_y + 25


def run_transit_mod(TRANSLINK_URL, t_stop_no, T_API_KEY, T_BUS,
                    T_BUS_TIME,  LOCATION,  mod_t_s_x, mod_t_s_y, draw, color):
    """Call functions to retrieve and display bus schedule."""

    bus_stop = []
    for x_stop in (t_stop_no):
        bus_stop.append(get_transit(
            TRANSLINK_URL, x_stop, T_API_KEY, T_BUS, T_BUS_TIME, color))
    # POPULATING TRANSIT
    draw_transit_mod(mod_t_s_x, mod_t_s_y, bus_stop, LOCATION, color, draw)
    bus_stop.clear()
