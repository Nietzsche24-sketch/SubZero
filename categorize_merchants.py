import csv

CATEGORY_MAP = {
    "Apple": "SaaS",
    "Google": "SaaS",
    "Microsoft": "SaaS",
    "Zoom": "SaaS",
    "Spotify": "Entertainment",
    "Netflix": "Entertainment",
    "Crave": "Entertainment",
    "Rogers": "Utility",
    "Bell": "Utility",
    "Bank": "Financial",
    "Amazon": "Shopping",
    "PayPal": "Financial",
    "Invoice": "Billing",
    "Generic Receipt": "Billing",
    "Donotreply": "Notifications",
    "Noreply": "Notifications",
    "Notifications": "Notifications"
}

SUSPICIOUS_AMOUNTS = {"$0.91", "$1.42", "$1.12", "$0.01"}

def detect_category(cleaned, amounts):
    # Suspicious if only junk amounts
    if all(amt.strip() in SUSPICIOUS_AMOUNTS for amt in amounts.split(",")):
        return "Suspicious"
    return CATEGORY_MAP.get(cleaned, "Unknown")

def add_categories(input_path="data/recurring_merchants_cleaned.csv",
                   output_path="data/recurring_merchants_categorized.csv"):
    with open(input_path, newline='') as infile, \
         open(output_path, "w", newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)
        writer.writerow(headers + ["Category"])

        for row in reader:
            if not row: continue
            _, cleaned, _, amounts = row
            category = detect_category(cleaned, amounts)
            writer.writerow(row + [category])

if __name__ == "__main__":
    add_categories()
