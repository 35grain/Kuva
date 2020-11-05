from __future__ import print_function
from datetime import *
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def display_calendar(USER_ID):
    # User ID from identification application

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    creds = None
    # The file USER_ID+'.pickle' stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(USER_ID+'.pickle'):
        with open(USER_ID+'.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(USER_ID+'.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Check for list of calendars
    page_token = None
    while True:
      calendar_list = service.calendarList().list(pageToken=page_token).execute()
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break

    events = []

    # Call the Calendar API
    now = datetime.now().isoformat()
    end_of_day = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(1)).isoformat()
    print('Getting the events for today',date.today().strftime("%d.%m.%Y"))

    # Get events from all calendars
    for calendar in calendar_list['items']:
        id=calendar['id']
        events_result = service.events().list(calendarId=id, timeMin=now + '+02:00',
                                            timeMax=end_of_day + '+02:00', singleEvents=True,
                                            orderBy="startTime", maxResults=10).execute()
        events += events_result.get('items', [])

    # Output list of events
    if not events:
        print('No upcoming events today.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        location = ""
        print()
        if len(start) < 11:
            start = start.replace("-",".")
            end = end.replace("-",".")
            print(start,"-",end)
        else:
            print(start,"-",end)
        print(event['summary'])
        try:
            location = event['location']
            print(location)
        except:
            pass

