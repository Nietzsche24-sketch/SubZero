import os, imaplib, email, csv, re
from email.header import decode_header

# configuration via environment
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = os.environ['EMAIL_ACCOUNT']
APP_PASSWORD = os.environ['APP_PASSWORD']

# detect “#delete” in subject
KEYWORD_RE = re.compile(r'#delete', re.IGNORECASE)
OUTPUT_CSV = 'subscription_emails.csv'

def connect_imap():
    M = imaplib.IMAP4_SSL(IMAP_SERVER)
    M.login(EMAIL_ACCOUNT, APP_PASSWORD)
    M.select('INBOX')
    return M

def fetch_and_delete():
    M = connect_imap()
    _, data = M.search(None, 'ALL')
    ids = data[0].split()
    out = []

    for num in ids:
        _, msg_data = M.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])

        # decode subject
        raw = msg.get('Subject','')
        subj, enc = decode_header(raw)[0]
        if isinstance(subj, bytes):
            subj = subj.decode(enc or 'utf-8', errors='ignore')

        if KEYWORD_RE.search(subj):
            frm = msg.get('From')
            date = msg.get('Date')
            print(f"🗑️ Deleting #{num.decode()} – {subj}")
            out.append({'Subject': subj, 'From': frm, 'Date': date})
            M.store(num, '+FLAGS', r'(\Deleted)')

    M.expunge()
    M.logout()

    if out:
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=['Subject','From','Date'])
            w.writeheader()
            w.writerows(out)
        print(f"✅ Saved {len(out)} records to {OUTPUT_CSV}")

if __name__=='__main__':
    fetch_and_delete()
