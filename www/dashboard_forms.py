from flask_wtf import FlaskForm
from wtforms import TextField,  SubmitField,  SelectField

from wtforms import validators, ValidationError


class Dashform(FlaskForm):
    T_URL = TextField("Transit URL: ", [validators.Required()])
    T_API_KEY = TextField("Transit API KEY: ", [validators.Required()])
    Stops = TextField("Bus Stops: ", [validators.Required()])
    T_BUS = SelectField("How many schedules: ", choices=[(h, h)for h in range(3, 6)])
    T_BUS_TIME = SelectField("Time range to look for Bus arrivals (in hours): ", choices=[
                             (g, g)for g in range(1, 16)])

    W_URL = TextField("Weather URL: ", [validators.Required()])
    W_API_KEY = TextField("Weather API: ", [validators.Required()])
    UNITS = SelectField('Units: ', choices=[('metric', 'Metric'), ('imperial', 'Imperial')])

    G_URL = TextField("Geolocation URL: ", [validators.Required()])
    G_API_KEY = TextField("Geolocation API: ", [validators.Required()])

    C_URL_1 = TextField("Currency URL: ", [validators.Required()])
    C_API_KEY_1 = TextField("Currency API: ", [validators.Required()])
    C_URL_2 = TextField("Selected currencies URL: ", [validators.Required()])
    C_API_KEY_2 = TextField("Selected currencies API: ", [validators.Required()])
    C_URL_3 = TextField("Bitcoin info URL: ", [validators.Required()])
    C_API_KEY_3 = TextField("Bitcoin info API: ", [validators.Required()])
    C_URL_4 = TextField("Ethereum info URL: ", [validators.Required()])
    C_API_KEY_4 = TextField("Ethereum info API: ", [validators.Required()])
    CURR_CHECK = TextField("Currencies to display, type up to 4 options: ", [validators.Required()])

    STOCK_W_URL = TextField("Week Stocks URL: ", [validators.Required()])
    STOCK_WE_URL = TextField("Weekend Stocks URL: ", [validators.Required()])
    STOCK_API = TextField("Stocks API: ", [validators.Required()])
    STOCK_CHECK = TextField("Stocks to check: ", [validators.Required()])

    gsheet_json = TextField("G-Sheet API file: ", [validators.Required()])
    sheetname = TextField(" G-Sheet name: ", [validators.Required()])

    CREDENTIALS_FILE = TextField("G-Meetings API file: ", [validators.Required()])
    #pickle_Cal = SubmitField("pickle_Cal")

    NEWS_URL = TextField("News URL: ", [validators.Required()])
    NEWS_API = TextField("News API: ", [validators.Required()])
    NEWS_SOURCES = TextField("News sources: ", [validators.Required()])

    waking_time = SelectField("Time ON (24H): ", choices=[(h, h)for h in range(0, 24)])
    sleeping_time = SelectField("Time OFF (24H): ", choices=[(h, h)for h in range(0, 24)])
    mod_1_choice = SelectField("Module 1: ", choices=[(
        'transit', 'Transit'), ('news', 'News'), ('spotify', 'Spotify'), ('random', 'Random'), ('off', 'OFF')])
    mod_2_choice = SelectField("Module 2: ", choices=[(
        'weather', 'Weather'), ('c-s', 'Currency/Stock'), ('random', 'Random'), ('off', 'OFF')])
    mod_3_choice = SelectField("Module 3: ", choices=[(
        'tasklist', 'Tasklist'), ('meetings', 'Meetings'), ('random', 'Random'), ('off', 'OFF')])
    mod_4_choice = SelectField("Module 4: ", choices=[(
        'calendar', 'Calendar')])
    refresh_time = SelectField("Refresh Time (in min.): ", choices=[(h, h)for h in range(5, 31)])
    awake = SelectField("Test Mode: ", choices=[('false', 'No'), ('true', 'Yes')])
    res_msg = TextField("")
    #submit = SubmitField("Submit")
