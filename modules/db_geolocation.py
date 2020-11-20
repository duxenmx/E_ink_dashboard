import requests
from modules import d_functions
g_data = []


def get_geo(G_URL, G_API, color):
    GEO_URL = str(G_URL) + '?api-key=' + str(G_API)
    # print(T_URL)
    error_connect = True
    while error_connect == True:
        try:
            # HTTP request
            # print('Attempting to connect to Translink.')
            response_g = requests.get(GEO_URL)
            # print('Connection to Translink successful.')
            # print(GEO_URL)
            error_connect = None
        except:
            # Call function to display connection error
            print('Connection error.')
            # error_connect = None
            # error = True
            d_functions.display_error('GEOLOCATION CONNECTION', color)
            # break
        # delete the comment below
        #
    error = None
    while error == None:
        # Check status of code request
        if response_g.status_code == 200:
            # print('Connection to Translink successful.')
            g_data = response_g.json()
            geo_data = []
            geo_data.append(g_data["city"])
            geo_data.append(g_data["region_code"])
            geo_data.append(g_data["country_name"])
            geo_data.append(g_data["latitude"])
            geo_data.append(g_data["longitude"])
            geo_data.append(g_data["currency"]["code"])
            geo_data.append(g_data["currency"]["name"])
            geo_data.append(g_data["country_code"])
            # return bus_sch

            return geo_data

            error = True

        else:
            # Call function to display HTTP error
            d_functions.display_error('HTTP GEOLOCATION', color)
