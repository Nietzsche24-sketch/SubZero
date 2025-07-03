# SubZero ❄️

SubZero is an AI-powered subscription killer and personal finance watchdog.

## Features

- 📬 Scans Gmail for recurring subscriptions
- 🧹 Cleans and normalizes messy merchant names
- ❌ Generates draft cancellation emails
- ⚙️ Auto-creates Gmail filters to archive/cancel
- 🕐 Runs on a weekly cron schedule
- 💾 Includes weekly tarball backup system

## How to Use

1. Authenticate Gmail (OAuth flow)
2. Choose from the command menu:
   - Scan for subscriptions
   - Normalize merchant names
   - Draft cancel emails
   - Generate Gmail filters

## Automation

- Weekly cron job: `run_subzero.sh`
- Weekly backup: `weekly_lantern_backup.sh`

## Future Goals

- 💳 Bank integration (Plaid / Stripe)
- 📱 Mobile UI dashboard
- 🌎 i18n / localization
- 🔐 End-to-end encryption

## Dev Notes

All scripts live in the root or `scripts/`. Gmail API keys are stored securely in `.env`.

---

MIT License
