import os, imaplib, email, csv, re
from email.header import decode_header
from datetime import datetime, timedelta

# CONFIG
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = os.environ['EMAIL_ACCOUNT']
APP_PASSWORD = os.environ['APP_PASSWORD']
OUTPUT_CSV = "recurring_merchants.csv"

# REGEX
KEYWORDS = re.compile(r'subscription|billing|invoice|charged|renewal|receipt', re.IGNORECASE)
AMOUNT_REGEX = re.compile(r'\$?(\d+\.\d{2})')

# Look back 60 days
SINCE_DATE = (datetime.now() - timedelta(days=60)).strftime('%d-%b-%Y')

def connect():
    print("[...] Connecting to Gmail IMAP...")
    M = imaplib.IMAP4_SSL(IMAP_SERVER)
    M.login(EMAIL_ACCOUNT, APP_PASSWORD)
    M.select("inbox")
    return M

def parse_email(msg):
    subject = msg["subject"] or ""
    decoded_subject, encoding = decode_header(subject)[0]
    if isinstance(decoded_subject, bytes):
        subject = decoded_subject.decode(encoding or "utf-8", errors="ignore")

    try:
        body = msg.get_payload(decode=True).decode('utf-8')
    except Exception:
        try:
            body = msg.get_payload(decode=True).decode('latin-1', errors="ignore")
        except Exception:
            body = ""

    return subject, body

def scan_inbox():
    M = connect()
    result, data = M.search(None, f'(SINCE {SINCE_DATE})')
    email_ids = data[0].split()
    print(f"[✓] Fetched {len(email_ids)} emails from last 60 days")

    merchant_counts = {}

    for i, eid in enumerate(email_ids):
        try:
            print(f"[{i+1}/{len(email_ids)}] Processing email ID: {eid.decode()}")
            result, data = M.fetch(eid, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject, body = parse_email(msg)
            sender = msg.get("From", "")
            merchant = sender.split('<')[-1].split('@')[0].strip() or "unknown"

            if KEYWORDS.search(subject) or KEYWORDS.search(body):
                amount_match = AMOUNT_REGEX.search(subject + body)
                amount = amount_match.group(1) if amount_match else "N/A"

                if merchant not in merchant_counts:
                    merchant_counts[merchant] = {"count": 0, "amounts": []}

                merchant_counts[merchant]["count"] += 1
                if amount != "N/A":
                    merchant_counts[merchant]["amounts"].append(f"${amount}")
        except Exception as e:
            print(f"⚠️  Error processing email {eid}: {e}")
            continue
        sender = msg.get("From", "")
        merchant = sender.split('<')[-1].split('@')[0].strip() or "unknown"

        if KEYWORDS.search(subject) or KEYWORDS.search(body):
            amount_match = AMOUNT_REGEX.search(subject + body)
            amount = amount_match.group(1) if amount_match else "N/A"

            if merchant not in merchant_counts:
                merchant_counts[merchant] = {"count": 0, "amounts": []}

            merchant_counts[merchant]["count"] += 1
            if amount != "N/A":
                merchant_counts[merchant]["amounts"].append(f"${amount}")

    return merchant_counts

def save_results(merchant_counts):
    with open(OUTPUT_CSV, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Merchant", "Count", "Amounts"])
        for merchant, data in sorted(merchant_counts.items(), key=lambda x: -x[1]["count"]):
            writer.writerow([merchant, data["count"], ', '.join(data["amounts"])])

if __name__ == "__main__":
    counts = scan_inbox()
    save_results(counts)

    print("\n🔁 Recurring Merchants Detected:\n")
    for merchant, data in sorted(counts.items(), key=lambda x: -x[1]["count"]):
        print(f"{merchant:30} | Count: {data['count']:2} | Est. Charges: {', '.join(data['amounts']) or 'N/A'}")

    print("\n💸 Done. Review recurring_merchants.csv and cancel junk.")
