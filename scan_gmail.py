from auth_init import authenticate
from googleapiclient.discovery import build
import base64
import email
from datetime import datetime, timedelta

def get_gmail_service():
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    return service

def scan_inbox_last_30_days():
    service = get_gmail_service()

    # Calculate the date 30 days ago
    thirty_days_ago = (datetime.utcnow() - timedelta(days=30)).strftime('%Y/%m/%d')
    query = f'after:{thirty_days_ago}'

    print(f"🔍 Scanning emails after {thirty_days_ago}...")

    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=500
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print("📭 No messages found in the last 30 days.")
        return

    print(f"✅ Found {len(messages)} messages")

    for i, msg in enumerate(messages, 1):
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = msg_data['payload'].get('headers', [])
        
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        sender  = next((h['value'] for h in headers if h['name'] == 'From'), '(No Sender)')
        date    = next((h['value'] for h in headers if h['name'] == 'Date'), '(No Date)')

        print(f"📩 Email #{i}")
        print(f"    🟣 Subject: {subject}")
        print(f"    📧 From: {sender}")
        print(f"    🕒 Date: {date}")
        print("-" * 50)

if __name__ == '__main__':
    scan_inbox_last_30_days()
