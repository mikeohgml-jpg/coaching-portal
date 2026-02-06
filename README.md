# Coaching Portal Python Application

A production-ready Flask web application for managing coaching clients and sessions. The portal provides a clean interface for registering new clients, recording coaching sessions, and automated email generation using AI.

## Features

- **Client Management**
  - Register new coaching clients with package details
  - Track client information in Google Sheets
  - Automatic duplicate detection

- **Session Recording**
  - Log coaching sessions with detailed information
  - Multiple session types supported (one-on-one, group, workshop, etc.)
  - Flexible pricing and hours tracking

- **Automated Communications**
  - AI-generated personalized welcome emails for new clients
  - Automated invoice emails after coaching sessions
  - Professional HTML email templates

- **Web Interface**
  - Clean, responsive Bootstrap 5 design
  - Form validation (client-side and server-side)
  - Real-time client dropdown with autocomplete
  - Success and error pages with helpful guidance

- **API-Driven Architecture**
  - RESTful API endpoints for all operations
  - JSON request/response format
  - Comprehensive error handling

## Technology Stack

- **Backend**: Python 3.8+, Flask 3.0
- **API Integration**: Google Sheets, Gmail, Claude AI (via OpenRouter)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Data Validation**: Pydantic
- **Deployment**: Vercel (serverless)

## Project Structure

```
coaching-portal-python/
├── app.py                           # Main Flask application
├── config.py                        # Configuration management
├── models.py                        # Pydantic data models
├── services/
│   ├── google_sheets_service.py    # Google Sheets API integration
│   ├── email_service.py            # Gmail API integration
│   ├── ai_service.py               # Claude AI integration
│   ├── client_service.py           # High-level business logic
│   └── auth_service.py             # Authentication utilities
├── templates/
│   ├── base.html                   # Base template with navigation
│   ├── new_client_form.html        # New client registration form
│   ├── existing_client_form.html   # Session recording form
│   ├── success.html                # Success page
│   └── error.html                  # Error page
├── static/
│   ├── style.css                   # Custom styling
│   └── script.js                   # Frontend JavaScript
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore file
├── vercel.json                     # Vercel deployment config
└── README.md                       # This file
```

## Local Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Google Cloud project with Sheets and Gmail APIs enabled
- Google service account credentials (JSON key file)
- OpenRouter or Anthropic API key (for AI features)

### Installation

1. **Clone or download the repository**

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Fill in your actual API keys and configuration:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` with your credentials:
     - `GOOGLE_SHEETS_ID`: Your Google Sheet ID
     - `GOOGLE_CREDENTIALS_JSON`: Path to your Google service account JSON
     - `OPENROUTER_API_KEY`: Your OpenRouter API key
     - `ANTHROPIC_API_KEY`: Your Anthropic API key (if not using OpenRouter)
     - `GMAIL_SENDER_EMAIL`: Your Gmail address (optional, for email features)
     - `SECRET_KEY`: Generate a secure random string for Flask

6. **Set up Google Credentials**
   - Download your Google service account JSON key file
   - Place it in the project directory or a secure location
   - Update `GOOGLE_CREDENTIALS_JSON` in `.env` with the path

7. **Prepare Google Sheets**
   - Create a Google Sheet with the following sheets:
     - **Clients**: Headers: Name, Email, Package Type, Start Date, End Date, Amount Paid, Created At, Notes
     - **Sessions**: Headers: Client Name, Coaching Type, Participant Count, Coaching Hours, Amount Collected, Session Date, Created At, Notes
   - Share the sheet with your service account email
   - Update `GOOGLE_SHEETS_ID` in `.env`

### Running Locally

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check endpoint |
| GET | `/form/new-client` | Display new client registration form |
| POST | `/api/clients/new` | Submit new client data |
| GET | `/form/existing-client` | Display coaching session form |
| POST | `/api/clients/existing-session` | Submit coaching session data |
| GET | `/api/clients` | Get list of all clients (for dropdown) |
| GET | `/success` | Success page |
| GET | `/error` | Error page |

## Environment Variables Guide

### Required Variables

- **GOOGLE_SHEETS_ID**: The ID from your Google Sheet URL
  - Example: `1A2B3C4D5E6F7G8H9I0J`

- **GOOGLE_CREDENTIALS_JSON**: Path to your Google service account JSON file
  - Example: `/path/to/credentials.json` or `./credentials.json`

- **OPENROUTER_API_KEY** or **ANTHROPIC_API_KEY**: API key for Claude AI
  - Get from https://openrouter.io or https://console.anthropic.com

### Optional Variables

- **GMAIL_SENDER_EMAIL**: Gmail address for sending emails
  - Example: `coaching@example.com`
  - Leave blank to disable email features

- **FLASK_ENV**: Set to `production` for production deployments
  - Default: `development`

- **DEBUG**: Set to `False` in production
  - Default: `False`

- **SECRET_KEY**: Secret key for Flask session management
  - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

- **DEPLOYMENT_URL**: Your application's public URL
  - Example: `https://coaching-portal.vercel.app`

## Deployment to Vercel

### Prerequisites

- A Vercel account (https://vercel.com)
- Vercel CLI installed: `npm install -g vercel`
- GitHub repository with your code pushed

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Vercel**
   ```bash
   vercel
   ```

3. **Set Environment Variables**
   - Go to your Vercel project dashboard
   - Settings → Environment Variables
   - Add all variables from `.env`:
     - `GOOGLE_SHEETS_ID`
     - `GOOGLE_CREDENTIALS_JSON` (as JSON string)
     - `OPENROUTER_API_KEY`
     - `ANTHROPIC_API_KEY`
     - `FLASK_ENV=production`
     - `DEBUG=False`

4. **Deploy**
   ```bash
   vercel deploy --prod
   ```

### Converting Credentials to JSON String

For `GOOGLE_CREDENTIALS_JSON`, you need to provide the entire JSON file as a string:

```bash
# On macOS/Linux:
cat path/to/credentials.json | jq -c '.' | pbcopy

# On Windows PowerShell:
(Get-Content path/to/credentials.json | ConvertTo-Json -Compress) | Set-Clipboard
```

Then paste the output as the environment variable value in Vercel.

## Form Fields Reference

### New Client Form
- **Name**: Client's full name (required)
- **Email**: Client's email address (required, validated)
- **Package Type**: Type of coaching program (required)
- **Start Date**: Program start date in YYYY-MM-DD format (required)
- **End Date**: Program end date in YYYY-MM-DD format (required, must be after start date)
- **Amount Paid**: Total investment in dollars (required, must be > 0)
- **Notes**: Optional additional information

### Existing Client Session Form
- **Client Name**: Select from registered clients (required, with autocomplete)
- **Coaching Type**: Type of session (one-on-one, group, etc.) (required)
- **Number of Participants**: How many participants (required, must be > 0)
- **Coaching Hours**: Duration in hours (required, must be > 0)
- **Session Date**: Date of the session in YYYY-MM-DD format (required)
- **Amount Collected**: Payment received for this session (required, >= 0)
- **Update Client End Date**: Optional new end date for the client's program
- **Notes**: Optional session notes

## Validation Rules

### Client Data
- Name: 1-255 characters
- Email: Valid email format
- Start Date < End Date
- Amount Paid > $0

### Session Data
- Client must exist in database
- Participant Count ≥ 1
- Coaching Hours > 0.25
- Amount Collected ≥ $0

## Email Templates

### Welcome Email
Automatically sent when a new client registers with:
- Personalized greeting
- Program details and investment amount
- Program dates
- Next steps and expectations

### Invoice Email
Automatically sent after a session with:
- Session details and type
- Coaching hours and participant count
- Amount due/collected
- Professional invoice format

## Troubleshooting

### "Google Sheets API not found"
- Ensure `GOOGLE_CREDENTIALS_JSON` points to a valid file
- Verify the service account has access to your Google Sheet
- Check that Sheets API is enabled in Google Cloud Console

### "API Key not configured"
- Verify `OPENROUTER_API_KEY` or `ANTHROPIC_API_KEY` is set
- Check that the key is valid and hasn't expired
- Ensure the key has permissions for chat completions

### "Client not found in sheet"
- Verify the client name matches exactly (case-insensitive)
- Check that the Clients sheet has the correct structure
- Ensure the client was successfully added to the sheet

### "Email send failed"
- Verify `GMAIL_SENDER_EMAIL` is set
- Ensure the service account has Gmail API permissions
- Check email error logs for specific details

### 500 Server Error
- Check the application logs for error details
- Verify all required environment variables are set
- Ensure all API services are reachable from your network

### Form Validation Fails
- Check browser console for validation error messages
- Verify all required fields are filled
- Ensure date formats are YYYY-MM-DD
- Check that end date is after start date

## Development Tips

### Running with Flask Debug Mode
```bash
export FLASK_ENV=development
export DEBUG=True
python app.py
```

### Testing with curl
```bash
# Health check
curl http://localhost:5000/

# Submit new client
curl -X POST http://localhost:5000/api/clients/new \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "package_type": "Standard",
    "start_date": "2024-01-01",
    "end_date": "2024-03-31",
    "amount_paid": 1500
  }'

# Get all clients
curl http://localhost:5000/api/clients
```

### Enabling Detailed Logging
Edit `app.py` to set logging level:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

1. **Never commit `.env` file** - Use `.env.example` only
2. **Rotate API keys regularly** - Especially in production
3. **Use HTTPS only** - In production deployment
4. **Validate all inputs** - Both client and server-side
5. **Sanitize database queries** - Use parameterized queries
6. **Keep dependencies updated** - Run `pip install --upgrade -r requirements.txt`
7. **Monitor logs** - Check Vercel logs for suspicious activity
8. **Limit CORS** - Restrict to your domain in production

## Performance Optimization

- **Client caching**: Clients list is cached for 5 minutes by default
- **API rate limiting**: Consider implementing rate limiting for production
- **Database indexing**: Add indexes to frequently queried columns in Sheets
- **Async processing**: Use background tasks for email sending

## License

This project is provided as-is for coaching portal management.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the logs for error details
3. Verify all configuration variables
4. Test API endpoints with curl or Postman

## Version History

- **1.0.0** (2024-02-06): Initial release
  - Client registration system
  - Session recording
  - AI-powered email generation
  - Google Sheets integration
  - Vercel deployment support
