"""
SkillDNA-AI Application Routes
Handles dashboard, profile, resume upload, AI analysis, career recommendation, and roadmap routes.
"""

import os
import json
from datetime import datetime, timezone
from flask import Blueprint, request, redirect, url_for, flash, render_template, session, current_app
from werkzeug.utils import secure_filename
from database import db
from models import User, UserProfile, Resume, Analysis, Roadmap
from auth import login_required, admin_required, get_current_user
from resume_parser import parse_resume, allowed_file
from ai_service import analyze_career

main_bp = Blueprint('main', __name__)


# ============================================
# Landing Page
# ============================================
@main_bp.route('/')
def index():
    """Landing page."""
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')


# ============================================
# Dashboard
# ============================================
@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main user dashboard."""
    user = get_current_user()
    if not user:
        flash('Session expired. Please log in again.', 'warning')
        return redirect(url_for('auth.login'))

    profile = user.profile
    latest_resume = user.resumes.order_by(Resume.uploaded_at.desc()).first()
    latest_analysis = user.analyses.first()  # Already ordered by desc
    analysis_count = user.analyses.count()

    return render_template('dashboard.html',
                           user=user,
                           profile=profile,
                           latest_resume=latest_resume,
                           latest_analysis=latest_analysis,
                           analysis_count=analysis_count)


# ============================================
# Profile
# ============================================
@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management."""
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        return render_template('profile.html', user=user, profile=user.profile)

    # POST — Update profile
    profile = user.profile
    if not profile:
        profile = UserProfile(user_id=user.id, skills=[])
        db.session.add(profile)

    profile.education = request.form.get('education', '').strip()
    profile.current_field = request.form.get('current_field', '').strip()
    profile.career_goal = request.form.get('career_goal', '').strip()
    profile.experience = request.form.get('experience', '').strip()

    # Handle skills — comes as comma-separated or JSON
    skills_input = request.form.get('skills', '').strip()
    if skills_input:
        try:
            # Try parsing as JSON array first
            skills_list = json.loads(skills_input)
        except (json.JSONDecodeError, TypeError):
            # Fall back to comma-separated
            skills_list = [s.strip() for s in skills_input.split(',') if s.strip()]
        profile.skills = skills_list
    else:
        profile.skills = []

    profile.updated_at = datetime.now(timezone.utc)

    try:
        db.session.commit()
        flash('Profile updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Profile update error: {e}')
        flash('Failed to update profile. Please try again.', 'error')

    return redirect(url_for('main.profile'))


# ============================================
# Resume Upload
# ============================================
@main_bp.route('/upload-resume', methods=['POST'])
@login_required
def upload_resume():
    """Handle resume file upload and text extraction."""
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    if 'resume' not in request.files:
        flash('No file selected.', 'error')
        return redirect(url_for('main.profile'))

    file = request.files['resume']

    if file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('main.profile'))

    if not allowed_file(file.filename):
        flash('Invalid file format. Please upload PDF, DOCX, or TXT.', 'error')
        return redirect(url_for('main.profile'))

    try:
        # Ensure upload directory exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)

        # Secure the filename and save
        filename = secure_filename(file.filename)
        # Add user ID prefix to prevent conflicts
        unique_filename = f"user_{user.id}_{filename}"
        filepath = os.path.join(upload_folder, unique_filename)
        file.save(filepath)

        # Extract text from resume
        success, extracted_text = parse_resume(filepath)

        if not success:
            flash(f'Resume processing error: {extracted_text}', 'error')
            # Clean up the file
            if os.path.exists(filepath):
                os.remove(filepath)
            return redirect(url_for('main.profile'))

        # Save resume record
        resume = Resume(
            user_id=user.id,
            filename=filename,
            extracted_text=extracted_text
        )
        db.session.add(resume)
        db.session.commit()

        flash('Resume uploaded and processed successfully!', 'success')

    except Exception as e:
        db.session.rollback()
        print(f'Resume upload error: {e}')
        flash('Failed to upload resume. Please try again.', 'error')

    return redirect(url_for('main.profile'))


# ============================================
# AI Analysis
# ============================================
@main_bp.route('/analyze', methods=['POST'])
@login_required
def analyze():
    """Trigger AI career analysis."""
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    profile = user.profile
    if not profile or not profile.career_goal:
        flash('Please complete your profile with a career goal before analysis.', 'warning')
        return redirect(url_for('main.profile'))

    # Gather user data for AI
    latest_resume = user.resumes.order_by(Resume.uploaded_at.desc()).first()
    resume_text = latest_resume.extracted_text if latest_resume else 'No resume uploaded'

    user_data = {
        'current_field': profile.current_field or 'Not specified',
        'career_goal': profile.career_goal,
        'education': profile.education or 'Not specified',
        'experience': profile.experience or 'Not specified',
        'skills': profile.skills or [],
        'resume_text': resume_text
    }

    # Perform AI analysis
    success, result = analyze_career(user_data)

    if not success:
        flash(f'Analysis failed: {result}', 'error')
        return redirect(url_for('main.dashboard'))

    try:
        # Save analysis results
        analysis = Analysis(
            user_id=user.id,
            career_goal_analyzed=profile.career_goal,
            current_strengths=result.get('current_strengths', []),
            skill_gaps=result.get('skill_gaps', []),
            skills_to_improve=result.get('skills_to_improve', []),
            recommended_skills=result.get('recommended_skills', []),
            career_recommendation=result.get('career_recommendation', {}),
            alternative_careers=result.get('alternative_careers', []),
            suggested_projects=result.get('suggested_projects', []),
            ai_raw_response=json.dumps(result)
        )
        db.session.add(analysis)
        db.session.flush()  # Get the analysis ID

        # Save roadmap
        roadmap_data = result.get('roadmap', {})
        roadmap = Roadmap(
            user_id=user.id,
            analysis_id=analysis.id,
            stages=roadmap_data.get('stages', []),
            priorities=result.get('priorities', {}),
            estimated_duration=roadmap_data.get('estimated_duration', '')
        )
        db.session.add(roadmap)

        db.session.commit()

        flash('AI analysis completed successfully!', 'success')
        return redirect(url_for('main.analysis_result', analysis_id=analysis.id))

    except Exception as e:
        db.session.rollback()
        print(f'Analysis save error: {e}')
        flash('Analysis completed but failed to save results. Please try again.', 'error')
        return redirect(url_for('main.dashboard'))


# ============================================
# Analysis Results
# ============================================
@main_bp.route('/analysis/<int:analysis_id>')
@login_required
def analysis_result(analysis_id):
    """View specific analysis results."""
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    analysis = db.session.get(Analysis, analysis_id)

    if not analysis or analysis.user_id != user.id:
        flash('Analysis not found.', 'error')
        return redirect(url_for('main.dashboard'))

    return render_template('analysis.html',
                           user=user,
                           analysis=analysis,
                           roadmap=analysis.roadmap,
                           profile=user.profile,
                           latest_resume=user.resumes.first())


@main_bp.route('/analysis/latest')
@login_required
def latest_analysis():
    """View the latest analysis results."""
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    analysis = user.analyses.first()
    if not analysis:
        flash('No analysis found. Please run an analysis first.', 'info')
        return redirect(url_for('main.dashboard'))

    return redirect(url_for('main.analysis_result', analysis_id=analysis.id))


# ============================================
# Career Recommendation
# ============================================
@main_bp.route('/career')
@login_required
def career():
    """Career recommendation page."""
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    analysis = user.analyses.first()
    if not analysis:
        flash('No analysis found. Please run an analysis first.', 'info')
        return redirect(url_for('main.dashboard'))

    return render_template('career.html',
                           user=user,
                           analysis=analysis)


# ============================================
# Learning Roadmap
# ============================================
@main_bp.route('/roadmap')
@login_required
def roadmap():
    """Personalized learning roadmap page."""
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    analysis = user.analyses.first()
    if not analysis:
        flash('No analysis found. Please run an analysis first.', 'info')
        return redirect(url_for('main.dashboard'))

    roadmap = analysis.roadmap

    return render_template('roadmap.html',
                           user=user,
                           analysis=analysis,
                           roadmap=roadmap)


# ============================================
# Analysis History
# ============================================
@main_bp.route('/history')
@login_required
def history():
    """View analysis history."""
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    analyses = user.analyses.all()

    return render_template('history.html',
                           user=user,
                           analyses=analyses)


# ============================================
# Skill Genome Matrix & Inventory
# ============================================
@main_bp.route('/skills')
@login_required
def skills():
    """Detailed skill genome matrix and inventory."""
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    profile = user.profile
    latest_analysis = user.analyses.first()

    return render_template('skills.html',
                           user=user,
                           profile=profile,
                           latest_analysis=latest_analysis)


# ============================================
# Portfolio Projects Hub
# ============================================
@main_bp.route('/projects')
@login_required
def projects():
    """Hands-on portfolio projects hub."""
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    latest_analysis = user.analyses.first()
    projects_list = latest_analysis.suggested_projects if latest_analysis else []

    return render_template('projects.html',
                           user=user,
                           latest_analysis=latest_analysis,
                           projects=projects_list)


# ============================================
# AI Career Interview Prep
# ============================================
@main_bp.route('/interview')
@login_required
def interview():
    """AI interview Q&A and practice scenarios."""
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    profile = user.profile
    latest_analysis = user.analyses.first()

    return render_template('interview.html',
                           user=user,
                           profile=profile,
                           latest_analysis=latest_analysis)


# ============================================
# User Account Settings
# ============================================
@main_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """User account settings and security management."""
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'change_password':
            current_pass = request.form.get('current_password', '')
            new_pass = request.form.get('new_password', '')
            confirm_pass = request.form.get('confirm_password', '')

            from werkzeug.security import check_password_hash, generate_password_hash
            if not check_password_hash(user.password_hash, current_pass):
                flash('Current password is incorrect.', 'error')
            elif new_pass != confirm_pass:
                flash('New passwords do not match.', 'error')
            elif len(new_pass) < 8:
                flash('New password must be at least 8 characters.', 'error')
            else:
                user.password_hash = generate_password_hash(new_pass, method='pbkdf2:sha256')
                db.session.commit()
                flash('Password updated successfully!', 'success')

        return redirect(url_for('main.settings'))

    return render_template('settings.html', user=user)


# ============================================
# ADMIN MANAGEMENT PORTAL
# ============================================

@main_bp.route('/admin')
@admin_required
def admin_dashboard():
    """Admin Management Dashboard."""
    users = User.query.order_by(User.id.desc()).all()
    
    total_users = len(users)
    total_admins = sum(1 for u in users if u.is_admin)
    total_analyses = Analysis.query.count()
    total_resumes = Resume.query.count()
    total_roadmaps = Roadmap.query.count()

    # Domain field distribution
    field_counts = {}
    for u in users:
        if u.profile and u.profile.current_field:
            f = u.profile.current_field.strip().title()
            field_counts[f] = field_counts.get(f, 0) + 1
        else:
            field_counts['Unspecified'] = field_counts.get('Unspecified', 0) + 1

    return render_template('admin.html',
                           users=users,
                           total_users=total_users,
                           total_admins=total_admins,
                           total_analyses=total_analyses,
                           total_resumes=total_resumes,
                           total_roadmaps=total_roadmaps,
                           field_counts=field_counts)


@main_bp.route('/api/admin/analytics')
@admin_required
def admin_analytics():
    """API endpoint for admin analytics graphs (logins, signups, fields)."""
    from sqlalchemy import func
    
    users = User.query.all()
    
    # 1. Signups & Logins by date (last 7 days or all dates)
    signup_dates = {}
    login_dates = {}
    
    for u in users:
        if u.created_at:
            d_str = u.created_at.strftime('%Y-%m-%d')
            signup_dates[d_str] = signup_dates.get(d_str, 0) + 1
        if u.last_login:
            d_str = u.last_login.strftime('%Y-%m-%d')
            login_dates[d_str] = login_dates.get(d_str, 0) + 1

    # Combine unique dates and sort
    all_dates = sorted(list(set(signup_dates.keys()).union(set(login_dates.keys()))))
    if not all_dates:
        all_dates = [datetime.now(timezone.utc).strftime('%Y-%m-%d')]

    signups_series = [signup_dates.get(d, 0) for d in all_dates]
    logins_series = [login_dates.get(d, 0) for d in all_dates]

    # 2. Career Fields breakdown
    field_counts = {}
    for u in users:
        field = (u.profile.current_field.strip().title() if u.profile and u.profile.current_field else 'Technical Domain')
        field_counts[field] = field_counts.get(field, 0) + 1

    return {
        'dates': all_dates,
        'signups': signups_series,
        'logins': logins_series,
        'fields': list(field_counts.keys()),
        'field_counts': list(field_counts.values())
    }


@main_bp.route('/admin/users/<int:user_id>/update', methods=['POST'])
@admin_required
def admin_update_user(user_id):
    """Admin update user information and role."""
    target_user = db.session.get(User, user_id)
    if not target_user:
        flash('User not found.', 'error')
        return redirect(url_for('main.admin_dashboard'))

    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip().lower()
    education = request.form.get('education', '').strip()
    current_field = request.form.get('current_field', '').strip()
    is_admin = request.form.get('is_admin') == 'on' or request.form.get('is_admin') == '1' or request.form.get('is_admin') == 'true'

    if not full_name or not email:
        flash('Name and email are required.', 'error')
        return redirect(url_for('main.admin_dashboard'))

    # Check email conflict
    existing = User.query.filter(User.email == email, User.id != user_id).first()
    if existing:
        flash('Another user with this email already exists.', 'error')
        return redirect(url_for('main.admin_dashboard'))

    try:
        target_user.full_name = full_name
        target_user.email = email
        target_user.is_admin = is_admin

        # Update or create user profile
        if not target_user.profile:
            profile = UserProfile(user_id=target_user.id, education=education, current_field=current_field)
            db.session.add(profile)
        else:
            target_user.profile.education = education
            target_user.profile.current_field = current_field

        db.session.commit()
        flash(f'User "{target_user.full_name}" updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Admin update user error: {e}')
        flash('Failed to update user details.', 'error')

    return redirect(url_for('main.admin_dashboard'))


@main_bp.route('/admin/users/<int:user_id>/toggle-admin', methods=['POST'])
@admin_required
def admin_toggle_role(user_id):
    """Quickly toggle admin status for a user."""
    current_admin_id = session.get('user_id')
    if current_admin_id == user_id:
        flash('You cannot change your own administrator status.', 'warning')
        return redirect(url_for('main.admin_dashboard'))

    target_user = db.session.get(User, user_id)
    if not target_user:
        flash('User not found.', 'error')
        return redirect(url_for('main.admin_dashboard'))

    try:
        target_user.is_admin = not target_user.is_admin
        db.session.commit()
        role_label = "Administrator" if target_user.is_admin else "Standard User"
        flash(f'User "{target_user.full_name}" role set to {role_label}.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Toggle admin role error: {e}')
        flash('Failed to update user role.', 'error')

    return redirect(url_for('main.admin_dashboard'))


@main_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    """Delete a user and cascade remove all related records."""
    current_admin_id = session.get('user_id')
    if current_admin_id == user_id:
        flash('You cannot delete your own logged-in admin account.', 'error')
        return redirect(url_for('main.admin_dashboard'))

    target_user = db.session.get(User, user_id)
    if not target_user:
        flash('User not found.', 'error')
        return redirect(url_for('main.admin_dashboard'))

    try:
        user_name = target_user.full_name
        db.session.delete(target_user)
        db.session.commit()
        flash(f'User "{user_name}" and all associated data deleted permanently.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f'Admin delete user error: {e}')
        flash('Failed to delete user.', 'error')

    return redirect(url_for('main.admin_dashboard'))

