"""Display calendar events."""

import datetime
# import time
import pickle
import os.path
import logging
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from modules import d_functions as d_f


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


def get_calendar_service(creds_file, creddir):
    """Log in to the calendar service, either by saved credentials or manual login."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists(os.path.join(creddir, 'token.pickle')):
        with open(os.path.join(creddir, 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(os.path.join(creddir, str(creds_file))), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(os.path.join(creddir, 'token.pickle'), 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
    return service


def get_meet_mod(cred_file, creddir):
    """Pull meeting list from calendar service."""

    service = get_calendar_service(cred_file, creddir)
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    # print('Getting List of 8 events')
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=8, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    g_cal = []
    cal_var_date = ''
    cal_var_time = ''
    cal_var_item_1 = ''
    cal_var_item_2 = ''
    cal_var = ''

    if not events:
        g_cal.append('No upcoming events found.', "", "", "")
    for event in events:
        start_date, start_time = d_f.sep_datetime(
            event['start'].get('dateTime', event['start'].get('date')))
        end_date, _ = d_f.sep_datetime(
            event['end'].get('dateTime', event['end'].get('date')))
        # time_conv = get_time(start)

        if str(start_date) == str(end_date):
            cal_var_date = str(start_date)
            cal_var_item_1, cal_var_item_2 = d_f.sep_strings(
                str(event['summary']), 26)		# limit of 26 char
        else:
            cal_var_date = str(start_date) + '-' + str(end_date)
            cal_var_item_1, cal_var_item_2 = d_f.sep_strings(
                str(event['summary']), 24)		# limit of 24 char

        cal_var_time = str(start_time)
        cal_var = cal_var_date, cal_var_time,  cal_var_item_1, cal_var_item_2
        g_cal.append(cal_var)

    return g_cal


def draw_meet_mod(t_s_x, t_s_y,  cal_items, draw, color):
    """Display meetings on canvas."""

    draw.text((t_s_x, t_s_y), "Meetings:",  font=d_f.font_size(24), fill=color)
    t_s_y = t_s_y+32
    x_items = 0
    cal_temp = ''

    for i in range(len(cal_items)):
        if x_items < 7:
            if cal_temp != str(cal_items[i][0]):
                draw.text((t_s_x, t_s_y), '- ' +
                          str(cal_items[i][0]), font=d_f.font_size(18), fill=color)
                draw.text((t_s_x+100, t_s_y),
                          str(cal_items[i][1]), font=d_f.font_size(18), fill=color)
                if len(str(cal_items[i][0])) < 10:
                    draw.text((t_s_x+170, t_s_y), " - " +
                              str(cal_items[i][2]) + " ", font=d_f.font_size(18), fill=color)
                else:
                    draw.text((t_s_x+190, t_s_y), " - " +
                              str(cal_items[i][2]) + " ", font=d_f.font_size(18), fill=color)
                t_s_y = t_s_y + 25
                x_items = x_items + 1
                if cal_items[i][3] != " ":
                    draw.text((t_s_x+170, t_s_y),
                              str(cal_items[i][3]) + " ", font=d_f.font_size(18), fill=color)
                    t_s_y = t_s_y + 25
                    x_items = x_items + 1
            else:
                draw.text((t_s_x+100, t_s_y),
                          str(cal_items[i][1]), font=d_f.font_size(18), fill=color)
                if len(str(cal_items[i][0])) < 10:
                    draw.text((t_s_x+170, t_s_y), " - " +
                              str(cal_items[i][2]) + " ", font=d_f.font_size(18), fill=color)
                else:
                    draw.text((t_s_x+190, t_s_y), " - " +
                              str(cal_items[i][2]) + " ", font=d_f.font_size(18), fill=color)
                t_s_y = t_s_y + 25
                x_items = x_items + 1
                if cal_items[i][3] != " ":
                    draw.text((t_s_x+170, t_s_y),
                              str(cal_items[i][3]) + " ", font=d_f.font_size(18), fill=color)
                    t_s_y = t_s_y + 25
                    x_items = x_items + 1
            cal_temp = str(cal_items[i][0])


def run_meeting_mod(CREDENTIALS_FILE, creddir, t_s_x, t_s_y, draw, color):
    """Call functions to Get meeting list and display them."""

    cal_items = get_meet_mod(CREDENTIALS_FILE, creddir)
    draw_meet_mod(t_s_x, t_s_y,  cal_items, draw, color)
    cal_items.clear()
