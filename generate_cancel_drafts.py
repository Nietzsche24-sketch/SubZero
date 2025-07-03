import csv
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

LABEL = "SubZero-Cancel"
CSV_FILE = "recurring_merchants.csv"

def get_gmail_service():
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow

    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    service = build('gmail', 'v1', credentials=creds)
    return service

def create_draft(service, user_id, message_body, subject, label_ids=[]):
    message = MIMEText(message_body)
    message['to'] = "support@example.com"
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'message': {'raw': raw, 'labelIds': label_ids}}
    return service.users().drafts().create(userId=user_id, body=body).execute()

def main():
    service = get_gmail_service()
    user_id = 'me'

    skip_words = ['support', 'notification', 'donotreply', 'noreply', 'arob', 'bg', 'service']

    with open(CSV_FILE, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            merchant = row['Merchant'].strip().lower()
            if any(w in merchant for w in skip_words):
                continue

            subject = f"Cancel recurring charges - {merchant}"
            message_body = (
                f"Hi,\n\nI'm seeing recurring charges from '{merchant}'. "
                f"Please cancel this subscription and confirm the cancellation.\n\nThank you."
            )
            print(f"Creating cancel draft for: {merchant}")
            create_draft(service, user_id, message_body, subject, label_ids=[])

if __name__ == "__main__":
    main()
