#!/usr/bin/env python3

"""Load credentials.  For the calendar, Use existing saved login credentials or ask the user to log in."""

import pickle
import os.path
import json
import logging
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

creddir_1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'credentials')
creddir_2 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'credentials/dash_id.json')


def get_calendar_service(creds_file, creddir):
    """Load calendar credentials."""
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


with open(creddir_2, "r") as rdash_id:
    data = json.load(rdash_id)


get_calendar_service(data["G_Meetings"]["CREDENTIALS_FILE"], creddir_1)
