# GitHub & Vercel Deployment Guide

A comprehensive step-by-step guide to deploy the Coaching Portal Python application to GitHub and Vercel.

---

## 📋 Prerequisites Checklist

Before starting, ensure you have the following:

- [ ] **Git Installed** - Download from [git-scm.com](https://git-scm.com/)
  - Verify: Run `git --version` in your terminal
  
- [ ] **GitHub Account** - Create at [github.com](https://github.com)
  - With email and password configured
  - SSH keys configured (optional but recommended)
  
- [ ] **Vercel Account** - Create at [vercel.com](https://vercel.com)
  - Can sign up with GitHub for easier integration
  
- [ ] **Project Requirements** - All dependencies listed in `requirements.txt`
  - Ensure your local environment runs without errors
  - Test with: `python app.py`

- [ ] **Environment Variables Ready**
  - `GOOGLE_SHEETS_ID` - Your Google Sheets ID
  - `GOOGLE_CREDENTIALS_JSON` - Service account JSON (base64 encoded)
  - `OPENROUTER_API_KEY` - Your OpenRouter API key
  - `ANTHROPIC_API_KEY` - Your Anthropic API key

### System Requirements
- Windows 10/11, macOS, or Linux
- Python 3.8+ installed
- Terminal/Command Prompt access
- Minimum 500MB free disk space

---

## 🚀 Section 1: GitHub Setup & Push

### Step 1.1: Initialize Git Repository Locally

If you haven't already initialized a git repository in your project:

```bash
cd coaching-portal-python
git init
```

**Output example:**
```
Initialized empty Git repository in C:\Users\cgmik\OneDrive\Documents\Agentic Workflow\Coaching\coaching-portal-python\.git/
```

### Step 1.2: Create `.gitignore` File

Create a `.gitignore` file in the project root to exclude unnecessary files:

```bash
# In coaching-portal-python directory
```

**Add this content to `.gitignore`:**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg
*.egg-info/
dist/
build/
.Python
venv/
ENV/
env/
pip-log.txt
pip-delete-this-directory.txt

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Node (if using node packages)
node_modules/
npm-debug.log

# Temporary files
*.tmp
*.bak
temp/
```

**Create the file:**
```bash
# Windows (PowerShell)
@"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg
*.egg-info/
dist/
build/
.Python
venv/
ENV/
env/
pip-log.txt
pip-delete-this-directory.txt

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Node (if using node packages)
node_modules/
npm-debug.log

# Temporary files
*.tmp
*.bak
temp/
"@ | Out-File -Encoding UTF8 .gitignore
```

### Step 1.3: Configure Git User (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 1.4: Stage All Files

```bash
git add .
```

**Verify staged files:**
```bash
git status
```

**Expected output:**
```
On branch main

No commits yet

Changes to be committed:
  new file:   app.py
  new file:   config.py
  new file:   models.py
  new file:   requirements.txt
  new file:   vercel.json
  new file:   .gitignore
  ...and other project files
```

### Step 1.5: Create Initial Commit

```bash
git commit -m "Initial commit: Coaching Portal Python application"
```

**Expected output:**
```
[main (root-commit) abc1234] Initial commit: Coaching Portal Python application
 15 files changed, 1250 insertions(+)
 ...
```

### Step 1.6: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. **Repository name:** `coaching-portal-python`
3. **Description:** "Flask web application for managing coaching clients and sessions"
4. **Visibility:** Choose Public or Private based on your preference
5. **Initialize repository:** Leave unchecked (we already have local commits)
6. Click **Create repository**

**Screenshot reference:** After creation, you'll see a page with instructions. Your repository URL will be:
```
https://github.com/YOUR_USERNAME/coaching-portal-python.git
```

### Step 1.7: Add Remote and Push to GitHub

Add the GitHub repository as a remote and push your code:

```bash
git remote add origin https://github.com/YOUR_USERNAME/coaching-portal-python.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username**

**Expected output:**
```
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 8 threads
Compressing objects: 100% (12/12), done.
Writing objects: 100% (15/15), 8.42 KiB | 2.81 MiB/s, done.
Total 15 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/YOUR_USERNAME/coaching-portal-python.git
 * [new branch]      main -> main
Branch 'main' is set to track remote branch 'main' from 'origin'.
```

### Step 1.8: Verify GitHub Push

Visit your repository:
```
https://github.com/YOUR_USERNAME/coaching-portal-python
```

✅ **Success indicators:**
- All your project files appear on GitHub
- Commit history shows your initial commit
- README.md displays properly
- No sensitive files (.env) are visible

---

## 🌐 Section 2: Vercel Deployment

### Step 2.1: Sign In to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click **Sign Up** (or **Sign In** if you already have an account)
3. **Recommended:** Sign up with GitHub for seamless integration
4. Authorize Vercel to access your GitHub account

### Step 2.2: Import Project from GitHub

1. Click **Add New...** → **Project**
2. Click **Import Git Repository**
3. Paste your repository URL: `https://github.com/YOUR_USERNAME/coaching-portal-python`
   - **Alternative:** Click **GitHub** and select from your repositories list
4. Click **Continue**

**Expected display:**
```
Import Git Repository

GitHub Repository
https://github.com/YOUR_USERNAME/coaching-portal-python

Project Name: coaching-portal-python
Framework: Python
```

### Step 2.3: Configure Project Settings

Vercel should auto-detect Python. Verify:

- **Project Name:** `coaching-portal-python` (or your preferred name)
- **Framework Preset:** Python
- **Root Directory:** `./` (or `.` - the project root)

**Build Settings (keep defaults):**
- **Build Command:** Leave empty (or use default)
- **Output Directory:** Leave empty

Click **Continue**

### Step 2.4: Set Environment Variables

This is **critical** for your application to function.

On the "Environment Variables" page, add each variable:

| Variable Name | Value | Notes |
|---|---|---|
| `GOOGLE_SHEETS_ID` | Your Google Sheets ID | Find in your sheet URL: `docs.google.com/spreadsheets/d/{ID}` |
| `GOOGLE_CREDENTIALS_JSON` | Service account JSON (base64 encoded) | See instructions below |
| `OPENROUTER_API_KEY` | Your OpenRouter API key | Get from openrouter.ai dashboard |
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Get from claude.ai/api dashboard |
| `FLASK_ENV` | `production` | Pre-configured in vercel.json |
| `DEBUG` | `False` | Pre-configured in vercel.json |

**For each variable:**
1. Enter the **Name** (from table above)
2. Paste the **Value**
3. Click **Add** or press Enter
4. Repeat for next variable

**Special Instructions for `GOOGLE_CREDENTIALS_JSON`:**

If your credentials JSON file is too large, encode it to base64:

```bash
# PowerShell
$content = Get-Content "path/to/credentials.json" -Raw
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content)) | Set-Clipboard
```

Then paste the base64 string as the environment variable value.

Your `config.py` should decode it:
```python
import base64
import json

credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
if credentials_json and credentials_json.startswith("ey"):
    credentials_dict = json.loads(base64.b64decode(credentials_json))
else:
    credentials_dict = json.loads(credentials_json)
```

### Step 2.5: Deploy

Click **Deploy** button

**Expected output:**
```
Building...
🔨 Building your project...

Vercel CLI  23.x.x
🎯 Deploying project...

> HEAD at 123abc456def789

Creating image...
Build complete
```

Wait 2-3 minutes for deployment to complete.

### Step 2.6: Get Your Deployment URL

After successful deployment, you'll see:

```
✅ Deployed Successfully!

Production: https://coaching-portal-python.vercel.app
```

Vercel automatically assigns a domain. You can:
- Use the auto-generated domain
- Add a custom domain (click **Domains** in project settings)

---

## 🔧 Environment Variables Configuration

### Understanding Your Environment Variables

Your `vercel.json` file references these variables with `@` prefix:

```json
"env": {
  "GOOGLE_SHEETS_ID": "@google_sheets_id",
  "GOOGLE_CREDENTIALS_JSON": "@google_credentials_json",
  "OPENROUTER_API_KEY": "@openrouter_api_key",
  "ANTHROPIC_API_KEY": "@anthropic_api_key"
}
```

The `@` prefix tells Vercel to **inject the variable from the environment settings**.

### How to Update Environment Variables After Deployment

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Find the variable you want to update
4. Click the **Edit** icon (pencil icon)
5. Update the value
6. Click **Save**
7. Vercel will **automatically redeploy** with new variables

⚠️ **Important:** Any changes to environment variables trigger a redeployment.

### Securing Sensitive Variables

- **Never commit** `.env` files to GitHub
- **Verify** `.gitignore` includes `.env*`
- **Use** Vercel's environment variable system for sensitive data
- **Rotate** API keys periodically
- **Review** access permissions for service accounts

---

## ✅ Post-Deployment Verification

### Step 3.1: Test Basic Functionality

1. Navigate to your Vercel deployment URL
2. You should see the Coaching Portal homepage
3. Test these features:

| Feature | Test | Expected Result |
|---|---|---|
| **New Client Form** | Load `/` or home page | Form loads with all fields |
| **Existing Client Form** | Load `/existing-client` | Form loads with client dropdown |
| **API Health** | Make request to `/health` (if available) | Returns 200 OK |
| **Form Submission** | Submit new client form | Success page or confirmation |

### Step 3.2: Check Logs

Monitor deployment logs for errors:

1. In Vercel dashboard, click **Deployments**
2. Click the latest deployment
3. Go to **Logs** tab
4. Check for any errors (red text)

**Common issues to look for:**
```
ImportError: No module named 'flask'    → Missing dependencies
NameError: name 'app' is not defined    → app.py configuration error
ValueError: GOOGLE_SHEETS_ID not set    → Missing environment variable
```

### Step 3.3: Test Email Functionality

If your app sends emails:

1. Submit a form that triggers email
2. Check your inbox (including spam folder)
3. Verify email formatting and content

### Step 3.4: Monitor Performance

In Vercel dashboard:

1. Click **Analytics**
2. Monitor:
   - **CPU Time** - Should be under 10s per request
   - **Memory** - Should be under 500MB
   - **Status Codes** - Should be 2xx (200, 201) for successful requests
   - **Errors** - Should be zero or minimal

### Step 3.5: Verify Google Sheets Integration

1. Access your Google Sheet
2. Submit a form in the deployed app
3. Check if new data appears in the spreadsheet
4. Verify data formatting and accuracy

---

## 🐛 Troubleshooting Guide

### Problem: "Build Failed" During Deployment

**Symptoms:**
```
Error: Build failed - Unable to install dependencies
```

**Solutions:**
1. Check `requirements.txt` for syntax errors
2. Ensure no conflicting package versions
3. Test locally: `pip install -r requirements.txt`
4. Clear Vercel cache: Settings → Deployments → Delete all deployments, then redeploy

**Command to check:**
```bash
pip install -r requirements.txt
```

---

### Problem: "ModuleNotFoundError" or "ImportError"

**Symptoms:**
```
ModuleNotFoundError: No module named 'flask'
ImportError: cannot import name 'Flask'
```

**Solutions:**
1. Verify all imports in `app.py` match installed packages
2. Check `requirements.txt` includes all dependencies
3. Redeploy after updating `requirements.txt`:
   ```bash
   git add requirements.txt
   git commit -m "Update dependencies"
   git push origin main
   ```

---

### Problem: Environment Variables Not Working

**Symptoms:**
```
ValueError: GOOGLE_SHEETS_ID environment variable not found
KeyError: 'OPENROUTER_API_KEY'
```

**Solutions:**
1. Go to Vercel project → **Settings** → **Environment Variables**
2. Verify all required variables are added
3. Check variable names match exactly (case-sensitive):
   - ✅ Correct: `GOOGLE_SHEETS_ID`
   - ❌ Wrong: `google_sheets_id` or `GOOGLE_SHEETs_ID`
4. Delete empty environment variables
5. Redeploy after changes

**Verify locally with:**
```bash
# Create .env file locally with variables
python -c "import os; print(os.getenv('GOOGLE_SHEETS_ID'))"
```

---

### Problem: Google Sheets Not Updated

**Symptoms:**
- Form submits successfully but data doesn't appear in spreadsheet
- Error messages in logs about Google Sheets API

**Solutions:**
1. Verify service account has access to spreadsheet:
   - Share the sheet with the service account email
   - Must have **Editor** permission
2. Check `GOOGLE_SHEETS_ID` is correct
3. Verify `GOOGLE_CREDENTIALS_JSON` is properly formatted and base64 encoded
4. Check logs for authentication errors
5. Test locally with same credentials

---

### Problem: SSL Certificate Errors

**Symptoms:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solutions:**
1. This is rare with Vercel (they handle SSL)
2. Check if external API calls use HTTP instead of HTTPS
3. Update code to use HTTPS for all external requests:
   ```python
   response = requests.get("https://api.example.com/...")  # Use https://
   ```

---

### Problem: Deployment Hangs or Takes Too Long

**Symptoms:**
- Deployment shows "Building..." for over 10 minutes
- Build times exceed normal (usually 2-3 minutes)

**Solutions:**
1. Check if there are large files in the repository
2. Clear Vercel cache: Project Settings → Deployments → "Clear Cache"
3. Try redeploying manually from GitHub
4. Check for infinite loops or blocking operations in startup code
5. Increase function timeout in `vercel.json` if needed

---

### Problem: "Cannot find module python"

**Symptoms:**
```
Error: Cannot find module 'python'
```

**Solutions:**
1. Verify `vercel.json` exists and is valid JSON
2. Check `vercel.json` build configuration:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app.py"
       }
     ]
   }
   ```
3. Ensure `app.py` is in the root directory
4. Redeploy from the Vercel dashboard

---

### Problem: CORS Errors in Browser Console

**Symptoms:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solutions:**
1. Verify Flask-CORS is installed in `requirements.txt`
2. Check `app.py` includes CORS initialization:
   ```python
   from flask_cors import CORS
   app = Flask(__name__)
   CORS(app)
   ```
3. Verify `requirements.txt` includes: `Flask-CORS==4.0.0`
4. Check that your frontend calls use correct domain
5. Redeploy after making changes

---

### Problem: "Internal Server Error" (500)

**Symptoms:**
```
500 Internal Server Error
```

**Solutions:**
1. Check Vercel logs for detailed error messages
2. Enable debug logging:
   - Set `DEBUG=True` in environment variables (development only)
   - Check logs for stack trace
3. Common causes:
   - Unhandled exceptions in route handlers
   - Missing database connections
   - Missing environment variables
   - Syntax errors in Python code
4. Test locally: `python app.py`
5. Check all dependencies are imported correctly

---

## 📚 Quick Reference: Common Commands

### Git Commands

```bash
# Check status of changes
git status

# View commit history
git log --oneline

# Add all changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push origin main

# Pull latest from GitHub
git pull origin main

# Create new branch
git checkout -b feature/my-feature

# Switch branches
git checkout main

# Merge a branch
git merge feature/my-feature
```

### Testing Locally Before Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py

# Test specific endpoint
curl http://localhost:5000/

# Check environment variables
python -c "import os; print(os.getenv('VARIABLE_NAME'))"
```

---

## 🔗 Helpful Documentation Links

### GitHub
- **Getting Started with GitHub**: https://docs.github.com/en/get-started
- **Creating a Repository**: https://docs.github.com/en/get-started/quickstart/create-a-repo
- **Pushing Commits to Remote**: https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository
- **GitHub Issues & Discussions**: https://docs.github.com/en/get-started/quickstart/hello-world

### Vercel
- **Vercel Documentation**: https://vercel.com/docs
- **Python Deployment**: https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python
- **Environment Variables**: https://vercel.com/docs/concepts/projects/environment-variables
- **Custom Domains**: https://vercel.com/docs/concepts/projects/domains

### Flask & Python
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Flask-CORS**: https://flask-cors.readthedocs.io/
- **Pydantic**: https://docs.pydantic.dev/
- **Python Deployment Best Practices**: https://docs.python.org/3/library/venv.html

### Google APIs
- **Google Sheets API**: https://developers.google.com/sheets/api
- **Google Cloud Console**: https://console.cloud.google.com
- **Service Account Setup**: https://cloud.google.com/iam/docs/service-accounts

---

## ✨ Success Indicators

### ✅ GitHub Push Complete When:
- [ ] Repository appears on GitHub
- [ ] All files visible on GitHub
- [ ] Commit history shows your commits
- [ ] No sensitive files (.env) are visible
- [ ] README.md displays properly

### ✅ Vercel Deployment Complete When:
- [ ] Vercel shows "Deployment Successful"
- [ ] You have a live URL (https://...)
- [ ] Forms load and appear responsive
- [ ] No 500 errors in logs
- [ ] All environment variables are set

### ✅ Functionality Verified When:
- [ ] Homepage loads without errors
- [ ] Forms submit successfully
- [ ] Data appears in Google Sheets
- [ ] Emails send correctly (if applicable)
- [ ] No console errors in browser (F12)
- [ ] Performance metrics are healthy

---

## 📞 Next Steps

1. **Monitor Deployments**: Check Vercel dashboard weekly for any errors
2. **Set Up GitHub Actions** (Optional): Automate testing on push
3. **Configure Custom Domain** (Optional): Use your own domain instead of vercel.app
4. **Enable Vercel Analytics** (Optional): Track user visits and performance
5. **Set Up Alerts** (Optional): Get notified of deployment failures

---

## 📝 Notes & Troubleshooting Log

Use this section to document any issues you encounter:

```
Date: _______________
Issue: _______________
Solution: _______________

---

Date: _______________
Issue: _______________
Solution: _______________
```

---

**Document Version:** 1.0  
**Last Updated:** February 2026  
**For Issues:** Check the Troubleshooting Guide or Vercel/GitHub documentation

---

*Happy Deploying! 🚀*
