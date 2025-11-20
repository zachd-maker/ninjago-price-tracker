# Lego Ninjago Price Tracker 🥷

Automatically monitors Amazon, Walmart, Target, and Lego.com for Lego Ninjago set deals and sends email alerts when prices drop.

## Features

- ✅ Monitors multiple retailers automatically
- ✅ Tracks price history over time
- ✅ Alerts you when prices drop 15% or more
- ✅ Runs every 6 hours via GitHub Actions (completely free!)
- ✅ No need to keep your computer running

## Setup Instructions

### Step 1: Create a GitHub Account (if you don't have one)

1. Go to [github.com](https://github.com)
2. Click "Sign up" and create a free account

### Step 2: Create a New Repository

1. Click the "+" button in the top right corner
2. Select "New repository"
3. Name it: `ninjago-price-tracker`
4. Make it **Public** (required for free GitHub Actions)
5. Check "Add a README file"
6. Click "Create repository"

### Step 3: Upload the Files

1. In your new repository, click "Add file" → "Upload files"
2. Drag and drop ALL the files from this folder:
   - `price_tracker.py`
   - `requirements.txt`
   - `.github/workflows/price_check.yml`
3. Click "Commit changes"

**Important:** Make sure the `.github/workflows/price_check.yml` file is in the correct folder structure. You may need to create folders manually if drag-and-drop doesn't work.

### Step 4: Set Up Email Notifications (Optional but Recommended)

To receive email alerts when deals are found, you'll need to configure email settings.

#### Option A: Using Gmail (Recommended)

1. **Create an App Password for Gmail:**
   - Go to your Google Account settings: [myaccount.google.com](https://myaccount.google.com)
   - Click "Security" in the left sidebar
   - Under "How you sign in to Google," enable "2-Step Verification" if not already enabled
   - After enabling 2FA, go back to Security and find "App passwords"
   - Select "Mail" and "Other (Custom name)" - name it "Ninjago Tracker"
   - Click "Generate"
   - **Copy the 16-character password** - you'll need this in the next step

2. **Add Secrets to GitHub:**
   - In your GitHub repository, click "Settings" tab
   - In the left sidebar, click "Secrets and variables" → "Actions"
   - Click "New repository secret"
   - Add these three secrets:

   **Secret 1:**
   - Name: `SENDER_EMAIL`
   - Value: Your Gmail address (e.g., `yourname@gmail.com`)
   - Click "Add secret"

   **Secret 2:**
   - Name: `SENDER_PASSWORD`
   - Value: The 16-character app password you generated
   - Click "Add secret"

   **Secret 3:**
   - Name: `RECIPIENT_EMAIL`
   - Value: The email where you want to receive alerts (can be the same as sender)
   - Click "Add secret"

#### Option B: Skip Email Setup

If you don't configure email, the script will still run and track prices. You can check the "Actions" tab in GitHub to see if any deals were found in the logs.

### Step 5: Enable GitHub Actions

1. Go to the "Actions" tab in your repository
2. If prompted, click "I understand my workflows, go ahead and enable them"
3. Click on "Ninjago Price Tracker" workflow on the left
4. Click "Enable workflow" if needed

### Step 6: Run Your First Check (Test It!)

1. In the "Actions" tab, click "Ninjago Price Tracker"
2. Click "Run workflow" dropdown (on the right)
3. Click the green "Run workflow" button
4. Wait 1-2 minutes, then refresh the page
5. You should see a workflow run appear - click it to see the results
6. Click "check-prices" to see detailed logs

### Step 7: Customize the Schedule (Optional)

By default, the tracker runs every 6 hours. To change this:

1. Edit `.github/workflows/price_check.yml`
2. Find the line: `- cron: '0 */6 * * *'`
3. Change to your preference:
   - Every 3 hours: `'0 */3 * * *'`
   - Every 12 hours: `'0 */12 * * *'`
   - Every day at 9am: `'0 9 * * *'`
   - Every 2 hours: `'0 */2 * * *'`

## How It Works

1. **Scraping:** The script checks each retailer's website for Ninjago products
2. **Price Storage:** Prices are saved to `price_history.csv` in your repository
3. **Deal Detection:** When a price drops 15% or more from the previous check, it's flagged as a deal
4. **Notifications:** You get an email with product details and links
5. **Automation:** GitHub Actions runs this automatically every 6 hours for free

## Viewing Results

### Check Email
If configured, you'll receive emails when deals are found.

### Check GitHub Actions Logs
1. Go to "Actions" tab
2. Click on any workflow run
3. Click "check-prices"
4. Expand the "Run price tracker" section to see what was found

### Check Price History
1. In your repository, open `price_history.csv`
2. You'll see a log of all prices over time

## Troubleshooting

### No emails being sent
- Double-check your GitHub Secrets are named correctly (case-sensitive)
- Make sure you used an App Password, not your regular Gmail password
- Check the Actions logs for error messages

### Workflow not running
- Make sure the repository is Public
- Check that the workflow file is in the correct location: `.github/workflows/price_check.yml`
- Enable workflows in the Actions tab

### Not finding many products
- Web scraping can be fragile as websites change their structure
- Amazon typically works best
- The script may need updates as websites change their HTML structure

## Customization Ideas

### Change the Deal Threshold
Edit `price_tracker.py`, line ~180:
```python
if discount_pct >= 15:  # Change 15 to your desired percentage
```

### Add More Retailers
Add new methods to the `NinjagoTracker` class following the pattern of existing retailers.

### Change Email Format
Edit the `send_email_alert()` method to customize how deal emails look.

## Important Notes

- **Rate Limiting:** The script includes delays between requests to be respectful to websites
- **Web Scraping Legality:** This tool is for personal use. Always respect robots.txt and terms of service
- **Reliability:** Websites change their structure frequently, so some retailers may stop working and need code updates
- **GitHub Actions Limits:** Free tier includes 2,000 minutes/month, which is more than enough for this use case

## Cost

This setup is **100% free**:
- GitHub Actions: Free for public repositories
- Gmail: Free
- No servers or hosting fees

## Future Enhancements

- Add more retailers (Best Buy, Barnes & Noble, etc.)
- Use APIs instead of web scraping where available
- Add Discord/Slack notifications
- Track specific set numbers
- Create price trend graphs

## Questions?

If something isn't working, check the Actions logs first - they usually show what went wrong!

---

Happy deal hunting! 🎯🥷
