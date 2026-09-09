# SkillDNA-AI — INTECH AI Career Genome Analyzer

🌐 **Live Web Tunnel Links:**
- **Public App Link:** [https://skilldna-ai.loca.lt](https://skilldna-ai.loca.lt)
- **GitHub Repository:** [https://github.com/rahulkoli8766161-coder/skillDNAAIdemo1](https://github.com/rahulkoli8766161-coder/skillDNAAIdemo1)
- **Recommended Domain:** `skilldna.tech` / `skilldna.ai`

An AI-powered career counseling web application that analyzes your resume, skills, education, and career goal to generate a personalized **Career Genome Report** with learning roadmap, skill gap analysis, and alternative career paths — powered by Google Gemini AI.

## Features
- 🔐 User registration & login (session-based auth)
- 📄 Resume upload & text extraction (PDF, DOCX, TXT)
- 🤖 AI Career Genome Analysis (Google Gemini)
- 📊 Skill gap & strength identification
- 🗺️ Personalized step-by-step learning roadmap
- 💼 Alternative career pathway suggestions
- 🧪 Portfolio project recommendations
- 🖨️ Printable / PDF-exportable reports

## Tech Stack
- **Backend:** Python 3 + Flask 3.1
- **Database:** SQLite (dev) / PostgreSQL (prod) via SQLAlchemy
- **AI:** Google Gemini (`google-generativeai`)
- **Frontend:** HTML5 + Vanilla CSS + Jinja2 templates

## Quick Start

```bash
cd backend
pip install flask flask-sqlalchemy python-dotenv werkzeug google-generativeai PyPDF2 python-docx
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

## Configuration
Copy `.env.example` to `.env` and set:
```
GEMINI_API_KEY=your_key_from_aistudio.google.com
SECRET_KEY=a-random-secret-key
```

## Database Entities
| Entity | Description |
|--------|-------------|
| `users` | Login accounts |
| `user_profiles` | Career info (skills, goal, education) |
| `resumes` | Uploaded resume files + extracted text |
| `analyses` | AI-generated career analysis results |
| `roadmaps` | Personalized learning roadmap stages |

## License
MIT
