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


def get_emails(n : int, creds : Credentials, q = None):  
    """  
    Gets the last n emails from the user's inbox.  
    """  
    service = build('gmail', 'v1', credentials=creds) 
  
    result = service.users().messages().list(userId='me', maxResults = n, q=None, labelIds = ["INBOX", "CATEGORY_PERSONAL"]).execute() 
    emails = []
    messages = result.get('messages') 
    for msg in messages: 
        txt = service.users().messages().get(userId='me', id=msg['id']).execute() 
        try: 
            payload = txt['payload'] 
            headers = payload['headers'] 
            for d in headers: 
                if d['name'] == 'Subject': 
                    subject = d['value'] 
                if d['name'] == 'From': 
                    sender = d['value'] 

            email_parts = payload.get("parts")[0]
            # handle attachements
            attachment_names = []
            attatchement_parts = payload.get("parts")[1:]
            for attachment_part in attatchement_parts:
                if attachment_part:
                    if attachment_part["filename"]:
                        attachment_names.append(attachment_part["filename"])
            try:
                data = email_parts['body']['data']
            except KeyError:
                data = email_parts["parts"][0]["body"]["data"] #sometimes the formatting is different idk
            data = data.replace("-","+").replace("_","/") 
            body = base64.b64decode(data).decode('utf-8')
            emails.append({"subject": subject, "sender": sender, "body": body, "attachments" : attachment_names})
        except Exception as e: 
            print("Unable to get the message: ", e)
    return emails

# # TODO: only for enterprise accounts
# def get_notes(creds : Credentials):
#     service = build('keep', 'v1', credentials=creds)
#     # Call the API
#     results = service.notes().list().execute()
#     print(results)


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


def get_calendar_events(n : int, creds : Credentials) -> list:
    """Get the user's calendar events
    :param creds: The user's credentials
    :return: The user's calendar events:
    
    In  this standard format: {'kind': 'calendar#event', 'etag': '"3424160851032000"', 'id': '7cr9l0ggad4dm9h68vdijaro5k', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=N2NyOWwwZ2dhZDRkbTloNjh2ZGlqYXJvNWsgc3plbGVzYXJvbjM5QG0', 'created': '2024-04-02T17:53:45.000Z', 'updated': '2024-04-02T17:53:45.516Z', 'summary': 'Fogorvos', 'creator': {'email': 'szelesaron39@gmail.com', 'self': True}, 'organizer': {'email': 'szelesaron39@gmail.com', 'self': True}, 'start': {'dateTime': '2024-04-05T10:30:00+02:00', 'timeZone': 'Europe/Budapest'}, 'end': {'dateTime': '2024-04-05T11:30:00+02:00', 'timeZone': 'Europe/Budapest'}, 'iCalUID': '7cr9l0ggad4dm9h68vdijaro5k@google.com', 'sequence': 0, 'reminders': {'useDefault': True}, 'eventType': 'default'}    
    """
    service = build("calendar", "v3", credentials=creds)
    # Call the Calendar v3 API
    # now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            # this sets the start date
            # timeMin=now,
            maxResults=n,
            # singleEvents=True,
            # orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    events_list = []
    for event in events:
        try:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            summary = event["summary"]
            description = event.get("description")
            timezone = event["start"].get("timeZone")
            link = event["htmlLink"]

            start_date_object = datetime.fromisoformat(start)
            end_date_object = datetime.fromisoformat(end)

            events_list.append(
                {
                    "start_date": start_date_object.strftime('%Y-%m-%d-%H-%M'),
                    "end_date": end_date_object.strftime('%Y-%m-%d-%H:%M'),
                    "summary": summary,
                    "description": description,
                    "timezone": timezone,
                    "link": link,
                }
            )
        except KeyError:
            print("KeyError in getting event with link:", event["htmlLink"])
    return events_list

if __name__ == "__main__":
    # print(get_notes(credentials))
    credentials = authenticate()

    res = get_emails(5, credentials)
    for r in res:
        print(r)
        print("\n")
    print(len(res))
    # print(get_drive_files(credentials))
    # print(get_calendar_events(n=1000, creds=credentials))