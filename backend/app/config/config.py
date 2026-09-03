import os
from dotenv import load_dotenv

# Load environmental variables from .env if present
load_dotenv()

raw_db_url = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/skillswap_campus_db"
)
# Render and other cloud providers provide postgres:// which SQLAlchemy 1.4+ deprecated in favor of postgresql://
if raw_db_url and raw_db_url.startswith("postgres://"):
    raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)

class Config:
    """Base application configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    
    # Database Settings
    SQLALCHEMY_DATABASE_URI = raw_db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SkillSwap Specific Options
    ALLOWED_EMAIL_DOMAIN = os.getenv("ALLOWED_EMAIL_DOMAIN", ".edu")
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    
    # Session Cookie Security Configuration
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", str(APP_ENV == "production")).lower() in ("true", "1", "yes")

