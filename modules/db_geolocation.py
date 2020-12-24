
"""Retrieve geolocation data."""

#import requests		#No longer needed in this module
from modules import d_functions as d_f


def get_geo(G_URL, G_API, color):
    """Get geolocation data."""
    g_data = []
    GEO_URL = str(G_URL) + '?api-key=' + str(G_API)
    # print(GEO_URL)

    #Following block replaced by "response_g = .../if response_g:" lines
    #error_connect = True
    #while error_connect is True:
    #    try:
    #        # HTTP request
    #        # print('Attempting to connect to Translink.')
    #        response_g = requests.get(GEO_URL)
    #        # print('Connection to Translink successful.')
    #        # print(GEO_URL)
    #        error_connect = None
    #    except:
    #        # Call function to display connection error
    #        print('Connection error.')
    #        # error_connect = None
    #        # error = True
    #        d_f.display_error('GEOLOCATION CONNECTION', color)
    #        # break
    #    # delete the comment below
    #    #
    #error = None
    #while error is None:
    #    # Check status of code request
    #    if response_g.status_code != 200:
    #        # Call function to display HTTP error
    #        d_f.display_error('HTTP GEOLOCATION', color)
    #    else:


    geo_data = []
    response_g = d_f.url_content(GEO_URL, 'geolocation', {}, color)
    if response_g:
        g_data = response_g.json()
        geo_data.append(g_data["city"])
        geo_data.append(g_data["region_code"])
        geo_data.append(g_data["country_name"])
        geo_data.append(g_data["latitude"])
        geo_data.append(g_data["longitude"])
        geo_data.append(g_data["currency"]["code"])
        geo_data.append(g_data["currency"]["name"])
        geo_data.append(g_data["country_code"])

    return geo_data
