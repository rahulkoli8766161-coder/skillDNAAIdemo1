"""
SkillDNA-AI Configuration Module
Loads environment variables and provides configuration for the Flask application.
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
except ImportError:
    pass


class Config:
    """Base configuration class."""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key-change-me')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'

    # Database
    _db_url = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(os.path.dirname(__file__), 'skilldna.db')}")
    try:
        if 'postgresql' in _db_url:
            import psycopg2
    except ImportError:
        _db_url = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'skilldna.db')}"
    
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google Gemini AI
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

    # File Upload
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(__file__),
        os.getenv('UPLOAD_FOLDER', 'uploads')
    )
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 5 * 1024 * 1024))  # 5MB
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
