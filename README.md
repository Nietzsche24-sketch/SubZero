# SubZero

**SubZero** automatically scans your Gmail for “#DELETE” emails (and deletes them)  
and builds a CSV of recurring‐merchant charge counts every 30 days.

## Usage

Set these secrets in GitHub (see below):  
- EMAIL_ACCOUNT  
- APP_PASSWORD  

Two workflows run:

- **imap_scanner.py**: looks for `#DELETE` in subjects & nukes those messages  
- **recurring_scanner.py**: scans the last 30 days for billing keywords, outputs `recurring_merchants.csv`

