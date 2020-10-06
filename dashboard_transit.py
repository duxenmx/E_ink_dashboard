import requests
import datetime
import d_functions
from datetime import timedelta


def get_transit(TRANSLINK_URL, T_STOP, T_API_KEY, T_BUS, T_BUS_TIME):
    T_URL = TRANSLINK_URL+T_STOP + '/estimates?apiKey=' + \
        T_API_KEY + '&count=' + T_BUS + '&timeframe=' + T_BUS_TIME
    # print(T_URL)
    error_connect = True
    while error_connect == True:
        try:
            # HTTP request
            # print('Attempting to connect to Translink.')
            response_t = requests.get(str(T_URL), headers={'Accept': 'application/JSON'})
            # print('Connection to Translink successful.')
            error_connect = None
        except:
            # Call function to display connection error
            print('Connection error.')
            # error_connect = None
            # error = True
            d_functions.display_error('TRANSIT CONNECTION')
            # break
        # delete the comment below
        #
    error = None
    while error == None:
        # Check status of code request
        if response_t.status_code == 200:
            # print('Connection to Translink successful.')
            t_data = response_t.json()
            # print(t_data)
            t_route_no = t_data[0]['RouteNo']
            t_schedules = t_data[0]['Schedules']
            t_route_dest_0 = t_schedules[0]['Destination']
            t_route_dest_1 = t_schedules[1]['Destination']
            t_sch_EC_0 = t_schedules[0]['ExpectedCountdown']
            t_sch_EC_1 = t_schedules[1]['ExpectedCountdown']

            # station formatting for space saving
            if t_route_dest_0 == "COMM'L-BDWAY STN" or t_route_dest_0 == "TO GRANVILLE":
                if t_route_dest_0 == "TO GRANVILLE":
                    t_route_dest_0 = "GRANVILLE"
                else:
                    t_route_dest_0 = "COM-BW STN"
            else:
                t_route_dest_0 = t_schedules[0]['Destination']

            if t_route_dest_1 == "COMM'L-BDWAY STN" or t_route_dest_1 == "TO GRANVILLE":
                if t_route_dest_1 == "TO GRANVILLE":
                    t_route_dest_1 = "GRANVILLE"
                else:
                    t_route_dest_1 = "COM-BW STN"
            else:
                t_route_dest_1 = t_schedules[1]['Destination']

            if d_functions.isTimeFormat(t_schedules[0]['ExpectedLeaveTime']):
                t_sch_ELT_0 = datetime.datetime.strptime(
                    str(t_schedules[0]['ExpectedLeaveTime']), '%I:%M%p %Y-%m-%d')
                t_sch_elt_t_0_0 = t_sch_ELT_0.time()
                t_sch_elt_t_0 = t_sch_elt_t_0_0.strftime("%I:%M%p")
            else:
                t_sch_elt_t_0 = t_schedules[0]['ExpectedLeaveTime']

            if d_functions.isTimeFormat(t_schedules[1]['ExpectedLeaveTime']):
                t_sch_ELT_1 = datetime.datetime.strptime(
                    str(t_schedules[1]['ExpectedLeaveTime']), '%I:%M%p %Y-%m-%d')
                t_sch_elt_t_1_1 = t_sch_ELT_1.time()
                t_sch_elt_t_1 = t_sch_elt_t_1_1.strftime("%I:%M%p")
            else:
                t_sch_elt_t_1 = t_schedules[1]['ExpectedLeaveTime']

            bus_sch = []

            if t_sch_EC_0 < 60:
                EC_0_time = ' min'
            else:
                EC_0_time = ' hours'

            if t_sch_EC_1 < 60:
                EC_1_time = ' min'
            else:
                EC_1_time = ' hours'

            bus_sch.append(str(t_route_no) + "-"+str(t_route_dest_0) +
                           " in " + str(timedelta(minutes=t_sch_EC_0))[:-3] + EC_0_time + ",at " + str(t_sch_elt_t_0))

            bus_sch.append(str(t_route_no) + "-"+str(t_route_dest_1) +
                           " in " + str(timedelta(minutes=t_sch_EC_1))[:-3] + EC_1_time + ",at " + str(t_sch_elt_t_1))

            return bus_sch

            error = True

        else:
            # Call function to display HTTP error
            d_functions.display_error('HTTP')
