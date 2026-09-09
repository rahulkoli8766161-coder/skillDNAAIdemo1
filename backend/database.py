"""
SkillDNA-AI Database Module
Manages database connection, session, and initialization using SQLAlchemy with PostgreSQL.
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()


def init_db(app):
    """
    Initialize the database with the Flask application.
    Creates all tables if they don't exist.
    """
    db.init_app(app)

    with app.app_context():
        # Import models to register them with SQLAlchemy
        import models  # noqa: F401

        # Create all tables
        db.create_all()

        print(" * Database tables created successfully")


def drop_db(app):
    """Drop all database tables. Use with caution."""
    with app.app_context():
        db.drop_all()
        print(" * All database tables dropped")
