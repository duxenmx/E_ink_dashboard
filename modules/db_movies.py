"""Incomplete module that is intended to retrieve movie listings."""

import requests
# import d_functions as d_f
from PIL import Image


def get_movies(C_URL_1):
    """Pull down movie listings."""
    error_connect = True

    while error_connect is True:
        try:
            # HTTP request
            # print('Attempting to connect to OWM.')
            response_c_1 = requests.get(str(C_URL_1))
            error_connect = None
        except:
            # Call function to display connection error
            print('Connection error.')
            # error_connect = None
            # error = True
            # d_f.display_error(' CURRENCY CONNECTION', color)
            # break
        # delete the comment below
        #
    error = None
    while error is None:
        # Check status of code request
        if response_c_1.status_code == 200:
            # print('Connection to Movies successful.')
            c_1_data = response_c_1.json()
            cur_exch = []

            return cur_exch
            error = True

        else:
            # Call function to display HTTP error
            break
            # d_f.display_error('HTTP CURRENCY', color)
