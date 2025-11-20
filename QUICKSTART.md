# Quick Start Guide

## 5-Minute Setup

### 1. Create GitHub Account
- Go to [github.com](https://github.com) and sign up

### 2. Create Repository
- Click "+" → "New repository"
- Name: `ninjago-price-tracker`
- Make it **Public**
- Click "Create repository"

### 3. Upload Files
- Click "Add file" → "Upload files"
- Upload all files from this folder
- Commit changes

### 4. Set Up Email (Optional)
Go to Settings → Secrets → Actions → New secret

Add these 3 secrets:
- `SENDER_EMAIL` = your Gmail address
- `SENDER_PASSWORD` = Gmail app password (get from Google Account → Security → App Passwords)
- `RECIPIENT_EMAIL` = where to send alerts

### 5. Enable & Test
- Go to "Actions" tab
- Enable workflows
- Click "Run workflow" to test

Done! It will now check every 6 hours automatically and email you when it finds deals.

## What It Does

✅ Checks Amazon, Walmart, Target, Lego.com every 6 hours  
✅ Emails you when prices drop 15%+  
✅ Tracks all Ninjago sets automatically  
✅ Completely free (runs on GitHub)

## View Results

- **Email**: Get instant deal alerts
- **GitHub Actions**: Click "Actions" tab to see logs
- **Price History**: View `price_history.csv` in your repo

## Need Help?

See full README.md for detailed troubleshooting.
