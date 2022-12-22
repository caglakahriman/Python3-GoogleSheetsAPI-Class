from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class SHEET_ACTION:
    "Basic sheets actions"
    def __init__(self, sheet_id:str, range:str) -> None:
        self.sheet_id = sheet_id
        self.range = range
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = self._credentials()
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.sheet = self.service.spreadsheets()

    def _credentials(self):
        creds = ''
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                creds = flow.run_local_server(port=8080)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds