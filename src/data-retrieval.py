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
from googleapiclient.errors import HttpError
import base64  

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def authenticate(token_path: str = "src/data/token.json"):
    """Authenticate the user and return the credentials."""
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
                "src/data/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return creds


  
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
            print("--------------------------------")
            print("Subject: ", subject) 
            print("From: ", sender) 
            print("Message: ", body) 
            print("--------------------------------")
            print('\n') 
        except Exception as e: 
            print("Unable to get the message: ", e)
            print(payload)


if __name__ == "__main__":
    credentials = authenticate()
    print(get_emails(6, credentials))
