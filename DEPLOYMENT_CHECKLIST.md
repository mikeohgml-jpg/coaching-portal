# Coaching Portal - Deployment Checklist

## Pre-Deployment Setup

### 1. Local Environment
- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file created from `.env.example`
- [ ] All required environment variables configured

### 2. Google Cloud Setup
- [ ] Google Cloud project created
- [ ] Google Sheets API enabled
- [ ] Service account created with JSON key downloaded
- [ ] Service account email added to Google Sheet as editor
- [ ] Google Sheet ID extracted and added to `.env`
- [ ] GOOGLE_CREDENTIALS_JSON path set in `.env`

### 3. Google Sheet Structure
- [ ] **Clients sheet** created with columns:
  - A: Name
  - B: Email
  - C: Package Type
  - D: Start Date
  - E: End Date
  - F: Amount Paid
  - G: Created At
  - H: Notes
- [ ] **Sessions sheet** created with columns:
  - A: Client Name
  - B: Coaching Type
  - C: Participant Count
  - D: Coaching Hours
  - E: Amount Collected
  - F: Session Date
  - G: Created At
  - H: Notes

### 4. AI/LLM Service
- [ ] OpenRouter account created (or Anthropic if preferred)
- [ ] API key generated and added to `.env`
- [ ] OPENROUTER_API_KEY or ANTHROPIC_API_KEY configured

### 5. Gmail Setup (Optional)
- [ ] Gmail API enabled in Google Cloud Console
- [ ] Service account delegated email permissions
- [ ] GMAIL_SENDER_EMAIL configured in `.env`

### 6. Flask Security
- [ ] SECRET_KEY generated: `python -c "import secrets; print(secrets.token_hex(32))"`
- [ ] SECRET_KEY added to `.env`
- [ ] FLASK_ENV set to `production`
- [ ] DEBUG set to `False`

## Local Testing

### 1. Application Startup
- [ ] Run startup check: `python startup_check.py`
- [ ] Start application: `python app.py`
- [ ] Application runs without errors
- [ ] Accessible at http://localhost:5000

### 2. Health Check
- [ ] GET http://localhost:5000/ returns 200
- [ ] Returns JSON with status and version

### 3. Form Pages
- [ ] GET /form/new-client loads successfully
- [ ] GET /form/existing-client loads successfully
- [ ] Forms display correctly
- [ ] All form fields render properly

### 4. API Endpoints
- [ ] POST /api/clients/new with valid data succeeds
- [ ] POST /api/clients/new with invalid data returns 400
- [ ] POST /api/clients/existing-session with valid data succeeds
- [ ] GET /api/clients returns list of clients
- [ ] Success pages display correctly
- [ ] Error pages display error messages

### 5. Data Validation
- [ ] Duplicate client detection works
- [ ] Date validation works (end date > start date)
- [ ] Email validation works
- [ ] Amount validation works (must be > 0 for new clients)
- [ ] Client name autocomplete works

### 6. Email Functionality
- [ ] Welcome email generated for new clients
- [ ] Invoice email generated for sessions
- [ ] Emails contain correct information
- [ ] Email sent successfully (or logged gracefully if Gmail not configured)

### 7. Database Integration
- [ ] New client appears in Google Sheet
- [ ] Session appears in Google Sheet
- [ ] Client cache invalidates after update
- [ ] Existing clients appear in dropdown

## Vercel Deployment

### 1. GitHub Repository
- [ ] Repository created on GitHub
- [ ] Code committed: `git add . && git commit -m "Initial commit"`
- [ ] Pushed to GitHub: `git push origin main`
- [ ] `.env` file is in `.gitignore` (not committed)
- [ ] credentials.json in `.gitignore`

### 2. Vercel Project Setup
- [ ] Vercel account created at https://vercel.com
- [ ] Vercel CLI installed: `npm install -g vercel`
- [ ] Project imported from GitHub to Vercel
- [ ] Vercel project name decided

### 3. Environment Variables in Vercel
- [ ] Go to Vercel Dashboard → Project Settings → Environment Variables
- [ ] Add all required variables:

```
GOOGLE_SHEETS_ID=your_sheet_id
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...full JSON...}
OPENROUTER_API_KEY=your_api_key
ANTHROPIC_API_KEY=your_api_key (if using instead of OpenRouter)
GMAIL_SENDER_EMAIL=your_email@gmail.com (optional)
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your_generated_secret_key
DEPLOYMENT_URL=https://your-vercel-app.vercel.app
CORS_ORIGINS=https://your-vercel-app.vercel.app
```

### 4. Google Credentials Formatting
- [ ] GOOGLE_CREDENTIALS_JSON converted to JSON string:
  - Option 1: Use `cat credentials.json | jq -c '.'`
  - Option 2: Load file content as single-line JSON
  - Copy entire JSON object as string value
  - No line breaks, single-line format

### 5. Deployment
- [ ] Run: `vercel deploy --prod` or use Vercel Dashboard
- [ ] Wait for deployment to complete
- [ ] Check deployment logs for errors
- [ ] Verify all environment variables loaded

### 6. Post-Deployment Testing
- [ ] Application accessible at Vercel URL
- [ ] Health check endpoint responds
- [ ] Form pages load
- [ ] Can submit new client form
- [ ] Can submit session form
- [ ] Emails sent successfully
- [ ] Check Vercel logs for errors

### 7. Production Monitoring
- [ ] Set up error monitoring (Sentry, etc.)
- [ ] Configure log aggregation
- [ ] Set up uptime monitoring
- [ ] Create backup of Google Sheet
- [ ] Document API keys and critical configs

## Post-Deployment

### 1. Security Audit
- [ ] Review all environment variables
- [ ] Verify no secrets in code
- [ ] Check CORS configuration for domain
- [ ] Review error messages for info leaks
- [ ] Test with invalid/malicious input
- [ ] Verify rate limiting if implemented

### 2. Performance Testing
- [ ] Test with concurrent users
- [ ] Monitor response times
- [ ] Check database query performance
- [ ] Verify caching works
- [ ] Monitor Vercel usage/costs

### 3. Backup & Recovery
- [ ] Set up Google Sheet backup
- [ ] Document backup procedure
- [ ] Test recovery process
- [ ] Create disaster recovery plan

### 4. Maintenance
- [ ] Schedule dependency updates
- [ ] Plan for certificate renewal
- [ ] Set up monitoring alerts
- [ ] Document support procedures
- [ ] Create runbook for common issues

## Documentation

### 1. User Documentation
- [ ] Create user guide with screenshots
- [ ] Document form field requirements
- [ ] Provide troubleshooting guide
- [ ] Create FAQ

### 2. Technical Documentation
- [ ] Document API endpoint details
- [ ] Create architecture diagram
- [ ] Document deployment procedure
- [ ] Create operations runbook

### 3. Training
- [ ] Train users on system
- [ ] Document common workflows
- [ ] Create video tutorials (optional)

## Troubleshooting Preparation

### 1. Common Issues
- [ ] Document common errors
- [ ] Create resolution steps
- [ ] Test all troubleshooting steps

### 2. Support
- [ ] Set up support email/ticketing
- [ ] Create SLA for response times
- [ ] Document escalation procedures

## Go-Live Checklist

### Final Verification
- [ ] All tests pass locally
- [ ] Production environment configured
- [ ] Backups verified
- [ ] Monitoring active
- [ ] Support team trained
- [ ] Documentation complete
- [ ] Security audit passed

### Launch
- [ ] Announce availability to users
- [ ] Monitor first 24 hours closely
- [ ] Be ready for immediate fixes
- [ ] Celebrate! 🎉

---

## Quick Reference

### Important Commands

```bash
# Local development
python startup_check.py        # Verify setup
python app.py                  # Run development server

# Testing
curl http://localhost:5000/    # Health check

# Git operations
git add .
git commit -m "message"
git push origin main

# Vercel operations
vercel                         # Deploy to preview
vercel deploy --prod          # Deploy to production
vercel logs                    # View logs
vercel env                     # Manage environment variables
```

### Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| GOOGLE_SHEETS_ID | Yes | Your Google Sheet ID |
| GOOGLE_CREDENTIALS_JSON | Yes | Service account JSON |
| OPENROUTER_API_KEY | Yes* | OpenRouter API key (*if using OpenRouter) |
| ANTHROPIC_API_KEY | Yes* | Anthropic API key (*if not using OpenRouter) |
| GMAIL_SENDER_EMAIL | No | Gmail for sending emails |
| FLASK_ENV | Yes | Set to 'production' |
| DEBUG | Yes | Set to 'False' |
| SECRET_KEY | Yes | 32+ character random string |
| DEPLOYMENT_URL | Yes | Your app's public URL |
| CORS_ORIGINS | Yes | Allowed domains for CORS |

---

**Last Updated**: February 2024  
**Version**: 1.0.0
