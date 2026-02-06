# Deploy to GitHub & Vercel - Step by Step Guide

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `coaching-portal`
   - **Description:** Coaching Portal - Client Management Application
   - **Public:** Yes
3. Click "Create repository"
4. Copy the repository URL (e.g., `https://github.com/yourusername/coaching-portal.git`)

## Step 2: Push Code to GitHub

Run these commands in PowerShell:

```powershell
cd "c:\Users\cgmik\OneDrive\Documents\Agentic Workflow\Coaching\coaching-portal-python"

# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/coaching-portal.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 3: Deploy to Vercel

### Option A: Using Vercel CLI (Recommended)

```powershell
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### Option B: Connect GitHub to Vercel (Easier)

1. Go to https://vercel.com
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Import Git Repository"
5. Paste your GitHub repo URL: `https://github.com/YOUR_USERNAME/coaching-portal.git`
6. Click "Import"
7. Set Environment Variables:
   - `GOOGLE_SHEETS_ID` = Your spreadsheet ID
   - `GOOGLE_CREDENTIALS_JSON` = Your credentials JSON
   - `OPENROUTER_API_KEY` = Your API key
   - `GMAIL_SENDER_EMAIL` = Your email
   - `FLASK_ENV` = production
8. Click "Deploy"

## Step 4: Access Your Live Application

Your app will be available at:
```
https://coaching-portal-YOUR_USERNAME.vercel.app
```

## Important Notes

### Before Deployment, Configure:

1. **Google Sheets API**
   - Create project: https://console.cloud.google.com
   - Enable Sheets API
   - Create Service Account
   - Download JSON credentials
   - Share your Google Sheet with service account email

2. **OpenRouter API**
   - Sign up: https://openrouter.io
   - Get API key
   - Add to Vercel env variables

3. **Gmail API**
   - Enable in Google Cloud Console
   - Add email to Vercel env variables

### Environment Variables to Set in Vercel:

```
GOOGLE_SHEETS_ID=your_spreadsheet_id
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
OPENROUTER_API_KEY=sk_xxx
GMAIL_SENDER_EMAIL=your-email@gmail.com
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your_secret_key_here
```

## Troubleshooting

### If deployment fails:
1. Check Vercel logs: `vercel logs`
2. Verify all environment variables are set
3. Check requirements.txt has all dependencies

### If API calls fail:
1. Verify credentials are correct
2. Check API quotas in Google Cloud
3. Verify service account permissions

## After Deployment

1. Test the live URL in your browser
2. Try registering a new client
3. Check Google Sheets for data
4. Monitor Vercel logs for errors

## Success!

Your Coaching Portal is now live at:
**https://coaching-portal-YOUR_USERNAME.vercel.app**

Share this URL with your team to start using the app!
