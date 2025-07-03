import csv
import os
import xml.etree.ElementTree as ET

INPUT_FILE = "data/recurring_merchants_final.csv"
OUTPUT_FILE = "filters/cancel_filters.xml"
LABEL = "SubZero-Cancel"

os.makedirs("filters", exist_ok=True)

def sanitize(value):
    return value.replace('"', '').strip()

def create_filter(from_value):
    entry = ET.Element("entry")
    ET.SubElement(entry, "category", term="filter")
    ET.SubElement(entry, "title").text = "Mail Filter"
    ET.SubElement(entry, "apps:property", name="from", value=from_value)
    ET.SubElement(entry, "apps:property", name="label", value=LABEL)
    ET.SubElement(entry, "apps:property", name="shouldArchive", value="true")
    return entry

filters = ET.Element("feed", xmlns="http://www.w3.org/2005/Atom", attrib={"xmlns:apps": "http://schemas.google.com/apps/2006"})

with open(INPUT_FILE, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get("Cancel?") == "YES":
            merchant = sanitize(row["Merchant"])
            if "@" in merchant or "noreply" in merchant.lower() or "billing" in merchant.lower():
                filters.append(create_filter(merchant))

tree = ET.ElementTree(filters)
tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)

print(f"✅ Gmail filter XML generated: {OUTPUT_FILE}")
