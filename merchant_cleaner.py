import csv
import re
from merchant_cleanup_rules import cleanup_rules

# Optional: Extendable mapping for corporate-level normalization
CLEAN_MAP = {
    r"apple|icloud|donotreply@apple": "Apple",
    r"rogers|fido|chatr": "Rogers",
    r"spotify": "Spotify",
    r"paypal|invoice.*paypal": "PayPal",
    r"zoom": "Zoom",
    r"microsoft|outlook|office365": "Microsoft",
    r"google|youtube|noreply@google": "Google",
    r"amazon|auto-confirm@amazon": "Amazon",
    r"netflix": "Netflix",
    r"crave": "Crave",
    r"bell": "Bell",
    r"td|rbc|bmo|scotiabank": "Bank",
    r"receipt.*": "Generic Receipt"
}

def normalize_name(raw_name):
    raw = raw_name.lower()

    # Phase 1: Apply explicit cleanup rules
    for pattern, replacement in cleanup_rules.items():
        if re.match(pattern, raw):
            return replacement

    # Phase 2: Apply broader corporate normalization patterns
    for pattern, mapped_name in CLEAN_MAP.items():
        if re.search(pattern, raw):
            return mapped_name

    # Phase 3: Fallback to email-style name cleanup
    return re.sub(r'\+.*|@.*', '', raw).strip().title()

def clean_merchants(input_path="data/recurring_merchants.csv",
                    output_path="data/recurring_merchants_cleaned.csv"):
    with open(input_path, newline='') as infile, \
         open(output_path, "w", newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)
        writer.writerow(["Merchant", "Cleaned Name", "Count", "Amounts"])

        for row in reader:
            if not row:
                continue
            merchant, count, *amounts = row
            cleaned = normalize_name(merchant)
            writer.writerow([merchant, cleaned, count] + amounts)

if __name__ == "__main__":
    clean_merchants()
