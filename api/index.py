"""Vercel API handler for Flask app."""

from app import create_app

app = create_app()

# Export for Vercel
def handler(request):
    """Vercel serverless function handler."""
    with app.app_context():
        return app.wsgi_app(request.environ, request.start_response)
