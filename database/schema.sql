-- SkillDNA-AI Database Schema Reference
-- PostgreSQL
-- This file serves as documentation. Tables are created via SQLAlchemy ORM.

-- ============================================
-- Users Table
-- Stores user authentication information
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- ============================================
-- User Profiles Table
-- Stores career-related information
-- ============================================
CREATE TABLE IF NOT EXISTS user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    education VARCHAR(255) DEFAULT '',
    current_field VARCHAR(255) DEFAULT '',
    career_goal VARCHAR(255) DEFAULT '',
    experience VARCHAR(255) DEFAULT '',
    skills JSONB DEFAULT '[]'::jsonb,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Resumes Table
-- Stores uploaded resume information
-- ============================================
CREATE TABLE IF NOT EXISTS resumes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    extracted_text TEXT DEFAULT '',
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Analyses Table
-- Stores AI-generated career analysis results
-- ============================================
CREATE TABLE IF NOT EXISTS analyses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    career_goal_analyzed VARCHAR(255) DEFAULT '',
    current_strengths JSONB DEFAULT '[]'::jsonb,
    skill_gaps JSONB DEFAULT '[]'::jsonb,
    skills_to_improve JSONB DEFAULT '[]'::jsonb,
    recommended_skills JSONB DEFAULT '[]'::jsonb,
    career_recommendation JSONB DEFAULT '{}'::jsonb,
    alternative_careers JSONB DEFAULT '[]'::jsonb,
    suggested_projects JSONB DEFAULT '[]'::jsonb,
    ai_raw_response TEXT DEFAULT '',
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Roadmaps Table
-- Stores personalized learning roadmaps
-- ============================================
CREATE TABLE IF NOT EXISTS roadmaps (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    analysis_id INTEGER NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
    stages JSONB DEFAULT '[]'::jsonb,
    priorities JSONB DEFAULT '{}'::jsonb,
    estimated_duration VARCHAR(100) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
