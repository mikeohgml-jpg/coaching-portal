"""Vercel API handler for Flask app."""

import logging
import sys

# Configure logging for Vercel
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

try:
    from app import create_app
    app = create_app()
    logger.info("Flask app initialized successfully for Vercel")
except Exception as e:
    logger.error(f"Failed to initialize Flask app: {e}")
    import traceback
    traceback.print_exc()
    raise

