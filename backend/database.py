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

        # Schema migration check for SQLite columns: is_admin, last_login
        try:
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            columns = [c['name'] for c in inspector.get_columns('users')]
            
            if 'is_admin' not in columns:
                db.session.execute(text('ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0'))
                db.session.commit()
                print(" * Added 'is_admin' column to users table")

            if 'last_login' not in columns:
                db.session.execute(text('ALTER TABLE users ADD COLUMN last_login DATETIME'))
                db.session.commit()
                print(" * Added 'last_login' column to users table")
        except Exception as migration_err:
            print(f" * Migration check note: {migration_err}")

        # Ensure at least one admin exists if users table is non-empty
        try:
            from models import User
            admin_count = User.query.filter_by(is_admin=True).count()
            if admin_count == 0:
                first_user = User.query.order_by(User.id.asc()).first()
                if first_user:
                    first_user.is_admin = True
                    db.session.commit()
                    print(f" * Promoted initial user '{first_user.email}' to Administrator")
        except Exception as admin_err:
            print(f" * Admin seeding note: {admin_err}")

        print(" * Database tables created and verified successfully")


def drop_db(app):
    """Drop all database tables. Use with caution."""
    with app.app_context():
        db.drop_all()
        print(" * All database tables dropped")
