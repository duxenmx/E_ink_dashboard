"""Incomplete module that is intended to retrieve movie listings."""

#import requests		#No longer needed in this module
from PIL import Image
from modules import d_functions as d_f


def get_movies(M_URL_1, color):
    """Pull down movie listings."""

    #Following block replaced by "response_g = .../if response_g:" lines
    #error_connect = True
    #while error_connect is True:
    #    try:
    #        # HTTP request
    #        # print('Attempting to connect to OWM.')
    #        response_c_1 = requests.get(str(C_URL_1))
    #        error_connect = None
    #    except:
    #        # Call function to display connection error
    #        print('Connection error.')
    #        # error_connect = None
    #        # error = True
    #        # d_f.display_error(' MOVIE CONNECTION', color)
    #        # break
    #    # delete the comment below
    #    #
    #error = None
    #while error is None:
    #    # Check status of code request
    #    if response_c_1.status_code != 200:
    #        # Call function to display HTTP error
    #        break
    #        # d_f.display_error('HTTP CURRENCY', color)
    #    else:

    movie_data = []
    response_m = d_f.url_content(M_URL_1, 'movies', {}, color)
    if response_m:
        # print('Connection to Movies successful.')
        m_1_data = response_m.json()

        #FIXME

    return movie_data
