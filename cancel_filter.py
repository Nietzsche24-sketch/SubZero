import csv

def is_cancel_worthy(category, count, amounts):
    try:
        count = int(count)
    except:
        return False

    # Always cancel suspicious
    if category == "Suspicious":
        return True

    # Repeated unknown = suspicious
    if category == "Unknown" and count >= 2:
        return True

    # Check for all low amounts (< $2)
    try:
        cleaned_amounts = [
            float(a.replace("$", "").strip()) for a in amounts.split(",")
            if a.strip().startswith("$")
        ]
        if all(amt < 2 for amt in cleaned_amounts):
            return True
    except:
        pass

    return False

def mark_cancel_worthy(input_path="data/recurring_merchants_categorized.csv",
                       output_path="data/recurring_merchants_final.csv"):
    with open(input_path, newline='') as infile, \
         open(output_path, "w", newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)
        writer.writerow(headers + ["Cancel?"])

        for row in reader:
            if not row: continue
            _, _, count, amounts, category = row
            cancel = "YES" if is_cancel_worthy(category, count, amounts) else ""
            writer.writerow(row + [cancel])

if __name__ == "__main__":
    mark_cancel_worthy()
