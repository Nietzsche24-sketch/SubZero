import os
import base64
import csv
import re
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Keywords to filter emails
KEYWORDS = [
    "subscription", "receipt", "invoice", "billing", "payment", "charged",
    "renewal", "trial", "confirmed", "transfer", "unsubscribe", "cancel",
    "digitalocean", "siteground", "thank you", "sports interaction"
]

# Load token
def load_credentials():
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        from google_auth_oauthlib.flow import InstalledAppFlow
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)
        print("✅ Saved new token with correct scopes.")

    return creds

# Get date N days ago in Gmail format
def get_rfc3339_date(days=30):
    date = datetime.utcnow() - timedelta(days=days)
    return date.strftime('%Y/%m/%d')

# Main scan function
def scan_emails():
    creds = load_credentials()
    service = build('gmail', 'v1', credentials=creds)

    query = f'after:{get_rfc3339_date(30)}'
    results = service.users().messages().list(userId='me', q=query, maxResults=100).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
        return

    output = []

    for i, msg in enumerate(messages, start=1):
        msg_detail = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata',
            metadataHeaders=['Subject', 'From', 'Date']
        ).execute()

        headers = msg_detail.get("payload", {}).get("headers", [])
        subject = sender = date = ""
        matched = delete_me = False

        for h in headers:
            if h["name"] == "Subject":
                subject = h["value"]
                matched = any(kw in subject.lower() for kw in KEYWORDS)
                delete_me = subject.strip().lower().startswith("#delete")
            elif h["name"] == "From":
                sender = h["value"]
            elif h["name"] == "Date":
                date = h["value"]

        if matched or delete_me:
            print(f"\n📧 Email #{i}")
            print(f"📌 Subject: {subject}")
            print(f"👤 From: {sender}")
            print(f"📅 Date: {date}")

            output.append({
                "Subject": subject,
                "From": sender,
                "Date": date
            })

            if delete_me:
                print("🗑️ Deleting email based on '#delete' keyword...")
                service.users().messages().delete(userId='me', id=msg['id']).execute()

    # Write to CSV
    if output:
        with open("subscription_emails.csv", "w", newline='', encoding="utf-8") as csvfile:
            fieldnames = ["Subject", "From", "Date"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in output:
                writer.writerow(row)

# Run the scan
if __name__ == "__main__":
    scan_emails()
