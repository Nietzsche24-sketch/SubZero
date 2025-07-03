import os

def main():
    while True:
        print("\n🧊 SubZero Command Center")
        print("[1] Scan Gmail for subscriptions")
        print("[2] Clean and categorize merchant names")
        print("[3] Generate cancel email drafts")
        print("[4] Generate Gmail filters")
        print("[5] Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            os.system("python scan_gmail.py")
        elif choice == "2":
            os.system("python merchant_cleaner.py && python categorize_merchants.py")
        elif choice == "3":
            os.system("python generate_cancel_drafts.py")
        elif choice == "4":
            os.system("python generate_gmail_filters.py")
        elif choice == "5":
            print("Exiting SubZero. ❄️")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
