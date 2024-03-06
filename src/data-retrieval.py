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

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def main():
    """Fetches the content of the last 3 received emails."""
    creds = None
    # Load credentials from token.json if it exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API to fetch the last 3 messages
        service = build("gmail", "v1", credentials=creds)
        messages = service.users().messages().list(userId="me", labelIds=["INBOX"], maxResults=3).execute().get("messages", [])

        if not messages:
            print("No messages found.")
            return

        print("Last 3 emails:")
        for message in messages:
            msg = service.users().messages().get(userId="me", id=message["id"]).execute()
            message_data = msg["payload"]["headers"]
            for header in message_data:
                if header["name"] == "Subject":
                    subject = header["value"]
                    print("Subject:", subject)
            # Fetching message body
            try:
                msg_str = msg["snippet"]
                print("Snippet:", msg_str)
            except Exception as e:
                print("Error:", e)

    except HttpError as error:
        # Handle errors from Gmail API
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
