import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    # Basic Configurations
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY environment variable is not set!")

    # Database Configurations
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("DATABASE_URL environment variable is not set!")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session Configurations
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV')
    if not SESSION_COOKIE_SECURE:
        print("WARNING: SESSION_COOKIE_SECURE is set to False. This should only be used in development.")
    SESSION_FILE_DIR = os.path.join(os.getcwd(), 'flask_session')

    # Microsoft Graph API (Email) Configurations
    AZURE_TENANT_ID = os.environ.get('AZURE_TENANT_ID', '')
    AZURE_CLIENT_ID = os.environ.get('AZURE_CLIENT_ID', '')
    AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET', '')
    if not all([AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET]):
        raise RuntimeError("Azure AD credentials (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET) must be set in environment variables.")