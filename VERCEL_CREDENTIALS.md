# Vercel Deployment - Login Credentials

## Production URL
**https://coaching-portal-python.vercel.app**

## Admin Login Credentials
- **Username**: `coachadmin`
- **Password**: `CoachPortal2026!`

⚠️ **UPDATED**: Credentials fixed - redeployed Feb 8, 2026 at 2:03 PM
⚠️ **IMPORTANT**: Change these credentials after your first login for security!

---

## Environment Variables Configured ✅

All required environment variables have been set in Vercel:

1. ✅ `GOOGLE_CREDENTIALS_JSON` - Service account credentials (encrypted)
2. ✅ `GOOGLE_CLIENTS_SHEET_ID` - Clients spreadsheet ID
3. ✅ `GOOGLE_SESSIONS_SHEET_ID` - Sessions spreadsheet ID
4. ✅ `ADMIN_USERNAME` - Admin username
5. ✅ `ADMIN_PASSWORD` - Admin password (8+ characters)
6. ✅ `SECRET_KEY` - Session encryption key
7. ✅ `FLASK_ENV` - Set to `production`
8. ✅ `DEBUG` - Set to `False`

---

## How to Access Your Portal

1. Visit: **https://coaching-portal-python.vercel.app**
2. Log in with the credentials above
3. Test both workflows:
   - New Client Registration
   - Session Recording

---

## To Change Admin Password

You can update the password in Vercel:

```bash
cd "c:\Users\cgmik\OneDrive\Documents\Agentic Workflow\Coaching\coaching-portal-python"
echo 'YourNewStrongPassword' | vercel env add ADMIN_PASSWORD production
vercel --prod
```

Or via Vercel Dashboard:
1. Go to: https://vercel.com/mikeohgml-3853s-projects/coaching-portal-python/settings/environment-variables
2. Find `ADMIN_PASSWORD`
3. Click **Edit** and enter new password
4. Redeploy the application

---

## Deployment Details

- **Latest Deployment**: https://coaching-portal-python-fclko568c-mikeohgml-3853s-projects.vercel.app
- **GitHub Repo**: https://github.com/mikeohgml-jpg/coaching-portal
- **Deployment Status**: ✅ Live and working

---

## Testing Checklist

- [ ] Can access the login page
- [ ] Can log in with admin credentials
- [ ] Can create a new client
- [ ] Can record a session for existing client
- [ ] Verify data appears in Google Sheets

---

**Deployment Date**: February 8, 2026
**Status**: ✅ Production Ready
