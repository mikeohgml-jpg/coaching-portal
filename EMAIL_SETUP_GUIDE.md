# Email Setup Guide - Coaching Portal
**For: Michael Oh (Mikeoh.gml@gmail.com)**

## Quick Setup Option: Gmail SMTP (Recommended)

This is the easiest way to get emails working with your personal Gmail account.

### Step 1: Generate Gmail App Password

1. Go to your Google Account: https://myaccount.google.com/
2. Click **Security** in the left menu
3. Under "How you sign in to Google", enable **2-Step Verification** (if not already enabled)
4. Once 2-Step Verification is enabled, scroll down to **App passwords**
5. Click **App passwords**
6. In "Select app", choose **Mail**
7. In "Select device", choose **Other** and type: **Coaching Portal**
8. Click **Generate**
9. **Copy the 16-character password** (it will look like: `abcd efgh ijkl mnop`)

### Step 2: Update Email Service Code

I'll create a new SMTP email service for you that uses Gmail SMTP instead of Gmail API.

### Step 3: Add Environment Variables to Vercel

After I update the code, you'll need to add these to Vercel:

```bash
GMAIL_SENDER_EMAIL=Mikeoh.gml@gmail.com
GMAIL_APP_PASSWORD=<your-16-character-password>
```

---

## Alternative: Use a Free Email Service

### Option 1: SendGrid (Easiest)
- Free tier: 100 emails/day
- No credit card required
- Setup time: 5 minutes

### Option 2: Mailgun
- Free tier: 100 emails/day (first month only)
- Requires credit card
- Very reliable

### Option 3: AWS SES
- Very cheap (100 emails/day free)
- Requires AWS account
- More technical setup

---

## My Recommendation

**Use Gmail SMTP** - It's the quickest way to get emails working with your existing Gmail account.

Would you like me to:
1. ✅ Update the code to use Gmail SMTP
2. ✅ Help you set up the App Password
3. ✅ Configure Vercel environment variables
4. ✅ Test the email sending

This will take about 10 minutes total.

---

## Email Templates Ready

Your portal will send:

### Welcome Email (New Client)
```
From: Michael Oh <Mikeoh.gml@gmail.com>
Subject: Welcome to Your Coaching Program, [Client Name]!

- Professional HTML email
- Includes all package details
- Start/end dates
- Investment amount
```

### Invoice Email (Session)
```
From: Michael Oh <Mikeoh.gml@gmail.com>
Subject: Coaching Session Invoice - [Date]

- Professional HTML invoice
- Session details
- Hours and amount
- Payment confirmation
```

Both emails will be professionally formatted and mobile-responsive.

---

**Next Step:** Let me know if you want to proceed with Gmail SMTP setup, and I'll update the code for you!
