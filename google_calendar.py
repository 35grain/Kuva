from __future__ import print_function
from datetime import *
import easygui
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def kuva_kalender(USER_ID):
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
      kalendrid = service.calendarList().list(pageToken=page_token).execute()
      page_token = kalendrid.get('nextPageToken')
      if not page_token:
        break

    events = []

    # Call the Calendar API
    praegu = datetime.now().isoformat()
    päeva_lõpp = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(1)).isoformat()

    # Get events from all calendars
    for calendar in kalendrid['items']:
        id=calendar['id']
        events_result = service.events().list(calendarId=id, timeMin=praegu + '+02:00',
                                            timeMax=päeva_lõpp + '+02:00', singleEvents=True,
                                            orderBy='startTime', maxResults=10).execute()
        events += events_result.get('items', [])

    # Output list of events
    if not events:
        kuva_sündmusi = 'Tänaseks ei ole rohkem sündmusi kirjas.'
    else:
        kuva_sündmusi = 'Sinu tänased sündmused:\n\n'
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            toimumispaik = ''
            if len(start) < 11:
                start = start.replace('-','.')
                end = end.replace('-','.')
            
            split1 = start.split('T')
            sõne1 = split1[1]
            split2 = sõne1.split('+')
            start = split2[0]

            split3 = end.split('T')
            sõne2 = split3[1]
            split4 = sõne2.split('+')
            end = split4[0]
            
            try:
                toimumispaik = event['toimumispaik']
                kuva_sündmusi += start + '-' + end + '\n' + event['summary'] + '\n' + event['toimumispaik'] + '\n'
            except:
                kuva_sündmusi += start + '-' + end + '\n' + event['summary'] + '\n'
    
    easygui.msgbox(kuva_sündmusi,date.today().strftime('%d.%m.%Y'))
