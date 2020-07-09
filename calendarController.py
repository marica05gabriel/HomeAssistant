import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime as dt
import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class EventPrototype:
    def __init__(self):
        self.event = {
            'summary': '%s',
            'location': '',
            'description': '',
            'start': {
                'dateTime': '%s',
                'timeZone': 'Europe/Bucharest',
            },
            'end': {
                'dateTime': '%s',
                'timeZone': 'Europe/Bucharest',
            },
            'recurrence': [],
            'attendees': [],
            'reminders': {},
        }

    def build(self, summary, startDate, endDate):
        self.event['summary'] = summary
        self.event['start']['dateTime'] = startDate
        self.event['end']['dateTime'] = endDate
        print(self.event)
        return self.event


class CalendarController:
    def __init__(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
        self.service = build('calendar', 'v3', credentials=self.creds)

    def insert(self, body):
        event = self.service.events().insert(calendarId='primary', body=body).execute()
        print('Event created: %s' % (event.get('htmlLink')))

    def getEvents(self, timeMin, timeMax):
        # timeMin = datetime.datetime(2020,6,15, 12, 0, 0).strftime("%Y-%m-%dT%H:%M:%SZ")
        # timeMax = datetime.datetime(2020,7,15, 13, 0, 0).strftime("%Y-%m-%dT%H:%M:%SZ")
        # timeMin = "2020-06-03T10:00:00-07:00",
        # timeMax = "2020-08-31T10:00:00Z",
        events_result = self.service.events().list(calendarId='primary',
                                        timeMax=timeMax,
                                        timeMin=timeMin,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
        return events_result.get('items', [])

    def getEventById(self, eventId):
        event = self.service.events().get(calendarId='primary', eventId=eventId).execute()
        return event