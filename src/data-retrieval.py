# get data from the following 3 sources:
# 1. gmail
# 2. google drive
# 3. google keep
# 4. google location history(?)

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64  
from datetime import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/calendar.readonly"]


def authenticate(token_path: str = "src/auth_data/token.json"):
    """Authenticate the user and return the credentials.
        If a new service is added, token.json needs to be deleted.
    """
    creds = None
    # Load credentials from token.json if it exists
    # TODO: this expires and the refresh doesnt work?
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "src/auth_data/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return creds


# TODO: improve parsing, handle email chains
def get_emails(n : int, creds : Credentials):  
    """  
    Gets the last n emails from the user's inbox.  
    """  
    service = build('gmail', 'v1', credentials=creds) 
  
    # request a list of all the messages 
    result = service.users().messages().list(userId='me', maxResults = n, labelIds = ["INBOX", "CATEGORY_PERSONAL"]).execute() 
  
    # We can also pass maxResults to get any number of emails. Like this: 
    # result = service.users().messages().list(maxResults=200, userId='me').execute() 
    messages = result.get('messages') 
  
    # iterate through all the messages 
    for msg in messages: 
        # Get the message from its id 
        txt = service.users().messages().get(userId='me', id=msg['id']).execute() 
  
        # Use try-except to avoid any Errors 
        try: 
            # Get value of 'payload' from dictionary 'txt' 
            payload = txt['payload'] 
            headers = payload['headers'] 
  
            # Look for Subject and Sender Email in the headers 
            for d in headers: 
                if d['name'] == 'Subject': 
                    subject = d['value'] 
                if d['name'] == 'From': 
                    sender = d['value'] 
  
            # The Body of the message is in Encrypted format. So, we have to decode it. 
            # Get the data and decode it with base 64 decoder. 
            parts = payload.get('parts')[0] 
            data = parts['body']['data'] 
            data = data.replace("-","+").replace("_","/") 
            body = base64.b64decode(data).decode('utf-8')

            # Printing the subject, sender's email and message 
            print("######################################")
            print("Subject: ", subject) 
            print("From: ", sender) 
            print("Message: ", body) 
            print("######################################")
            print('\n') 
        except Exception as e: 
            print("Unable to get the message: ", e)
            print(payload)

# TODO: only for enterprise accounts
def get_notes(creds : Credentials):
    service = build('keep', 'v1', credentials=creds)
    # Call the API
    results = service.notes().list().execute()
    print(results)


# TODO: clean up auth
def get_drive_files(creds : Credentials):
    """Search file in drive location"""

    service = build("drive", "v3", credentials=creds)

    # Call the Drive v3 API
    results = (
        service.files()
        .list(pageSize=10, fields="nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])
    return items



def get_calendar_events(creds : Credentials):
    """Get the user's calendar events"""

    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar v3 API
    now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    return events

if __name__ == "__main__":
    credentials = authenticate()

    # print(get_emails(6, credentials))
    # print(get_notes(credentials))
    # print(get_drive_files(credentials))
    print(get_calendar_events(credentials))
    