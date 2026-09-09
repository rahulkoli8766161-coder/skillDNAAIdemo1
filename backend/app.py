"""
SkillDNA-AI — Main Flask Application
AI Career Genome Analyzer
"""

import os
import sys
from datetime import timedelta
from flask import Flask, render_template

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def create_app():
    """Flask application factory."""
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    # Load configuration
    from config import Config
    app.config.from_object(Config)

    # Session configuration
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

    # Ensure upload folder exists
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)

    # Initialize database
    from database import init_db
    init_db(app)

    # Register blueprints
    from auth import auth_bp
    from routes import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('base.html', error_code=404, error_message='Page not found'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('base.html', error_code=500, error_message='Internal server error'), 500

    @app.errorhandler(413)
    def file_too_large(e):
        return render_template('base.html', error_code=413, error_message='File too large. Maximum size is 5MB.'), 413

    print(" * SkillDNA-AI application initialized successfully")
    return app


# Run the application
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
