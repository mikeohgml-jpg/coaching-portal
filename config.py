"""Configuration management for Coaching Portal application."""

import os
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    """Base configuration."""
    
    # Flask configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    
    # API configuration
    GOOGLE_CLIENTS_SHEET_ID = os.getenv("GOOGLE_CLIENTS_SHEET_ID")
    GOOGLE_SESSIONS_SHEET_ID = os.getenv("GOOGLE_SESSIONS_SHEET_ID")
    GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Deployment configuration
    DEPLOYMENT_URL = os.getenv("DEPLOYMENT_URL", "http://localhost:5000")
    
    # Cache configuration
    CLIENT_CACHE_TTL = 30  # 30 seconds (reduced for frequent updates)
    
    # Email configuration (SMTP)
    GMAIL_SENDER_EMAIL = os.getenv("GMAIL_SENDER_EMAIL")
    GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
    GMAIL_SENDER_NAME = os.getenv("GMAIL_SENDER_NAME", "Michael Oh")

    # CORS configuration
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    WTF_CSRF_ENABLED = False


def get_config():
    """Get appropriate config based on environment."""
    env = os.getenv("FLASK_ENV", "development")
    
    if env == "production":
        return ProductionConfig
    elif env == "testing":
        return TestingConfig
    else:
        return DevelopmentConfig
