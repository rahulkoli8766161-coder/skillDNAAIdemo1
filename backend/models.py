"""
SkillDNA-AI Database Models
SQLAlchemy ORM models for all database tables.
"""

from datetime import datetime, timezone
from database import db


class User(db.Model):
    """User account model for authentication."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    resumes = db.relationship('Resume', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    analyses = db.relationship('Analysis', backref='user', lazy='dynamic', cascade='all, delete-orphan',
                               order_by='Analysis.analyzed_at.desc()')

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        """Convert user to dictionary (excluding password)."""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class UserProfile(db.Model):
    """User career profile information."""
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    education = db.Column(db.String(255), default='')
    current_field = db.Column(db.String(255), default='')
    career_goal = db.Column(db.String(255), default='')
    experience = db.Column(db.String(255), default='')
    skills = db.Column(db.JSON, default=list)  # List of skill strings
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<UserProfile user_id={self.user_id}>'

    def to_dict(self):
        """Convert profile to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'education': self.education,
            'current_field': self.current_field,
            'career_goal': self.career_goal,
            'experience': self.experience,
            'skills': self.skills or [],
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Resume(db.Model):
    """User resume storage and extracted text."""
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    extracted_text = db.Column(db.Text, default='')
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Resume {self.filename}>'

    def to_dict(self):
        """Convert resume to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'extracted_text': self.extracted_text[:200] + '...' if self.extracted_text and len(self.extracted_text) > 200 else self.extracted_text,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }


class Analysis(db.Model):
    """AI career analysis results."""
    __tablename__ = 'analyses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    career_goal_analyzed = db.Column(db.String(255), default='')
    current_strengths = db.Column(db.JSON, default=list)
    skill_gaps = db.Column(db.JSON, default=list)
    skills_to_improve = db.Column(db.JSON, default=list)
    recommended_skills = db.Column(db.JSON, default=list)
    career_recommendation = db.Column(db.JSON, default=dict)
    alternative_careers = db.Column(db.JSON, default=list)
    suggested_projects = db.Column(db.JSON, default=list)
    ai_raw_response = db.Column(db.Text, default='')
    analyzed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    roadmap = db.relationship('Roadmap', backref='analysis', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Analysis id={self.id} user_id={self.user_id}>'

    def to_dict(self):
        """Convert analysis to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'career_goal_analyzed': self.career_goal_analyzed,
            'current_strengths': self.current_strengths or [],
            'skill_gaps': self.skill_gaps or [],
            'skills_to_improve': self.skills_to_improve or [],
            'recommended_skills': self.recommended_skills or [],
            'career_recommendation': self.career_recommendation or {},
            'alternative_careers': self.alternative_careers or [],
            'suggested_projects': self.suggested_projects or [],
            'analyzed_at': self.analyzed_at.isoformat() if self.analyzed_at else None
        }


class Roadmap(db.Model):
    """Personalized learning roadmap generated by AI."""
    __tablename__ = 'roadmaps'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analyses.id'), nullable=False)
    stages = db.Column(db.JSON, default=list)  # List of stage objects
    priorities = db.Column(db.JSON, default=dict)  # {high: [], medium: [], low: []}
    estimated_duration = db.Column(db.String(100), default='')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Roadmap id={self.id} analysis_id={self.analysis_id}>'

    def to_dict(self):
        """Convert roadmap to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'analysis_id': self.analysis_id,
            'stages': self.stages or [],
            'priorities': self.priorities or {},
            'estimated_duration': self.estimated_duration,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
