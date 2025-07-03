import os, imaplib, email, csv, re
from email.header import decode_header
from datetime import datetime, timedelta

# CONFIG
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = os.environ['EMAIL_ACCOUNT']
APP_PASSWORD = os.environ['APP_PASSWORD']
OUTPUT_CSV = 'recurring_merchants.csv'

# Keywords indicating a bill or subscription
KEYWORDS = re.compile(
    r'subscription|billing|invoice|charged|renewal|receipt', 
    re.IGNORECASE
)

def connect():
    M = imaplib.IMAP4_SSL(IMAP_SERVER)
    M.login(EMAIL_ACCOUNT, APP_PASSWORD)
    M.select('INBOX')
    return M

def scan_recent(days=30):
    since = (datetime.now() - timedelta(days=days)).strftime('%d-%b-%Y')
    # Search for all messages since X days ago
    typ, data = M.search(None, f'(SINCE {since})')
    return data[0].split()

if __name__ == '__main__':
    M = connect()
    ids = scan_recent(30)
    counts = {}

    for num in ids:
        typ, msg_data = M.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])

        # decode subject
        raw = msg.get('Subject', '')
        subj, enc = decode_header(raw)[0]
        if isinstance(subj, bytes):
            subj = subj.decode(enc or 'utf-8', errors='ignore')

        # extract sender domain
        frm = msg.get('From', '')
        m = re.search(r'@([A-Za-z0-9.-]+)', frm)
        domain = m.group(1) if m else frm

        # check keywords in subject or first part of body
        body = ''
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode(errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors='ignore')

        if KEYWORDS.search(subj) or KEYWORDS.search(body):
            counts[domain] = counts.get(domain, 0) + 1

    # save to CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Merchant', 'Count in last 30 days'])
        for merchant, cnt in sorted(counts.items(), key=lambda x: -x[1]):
            writer.writerow([merchant, cnt])

    print(f"✅ Wrote recurring merchants to {OUTPUT_CSV}")
