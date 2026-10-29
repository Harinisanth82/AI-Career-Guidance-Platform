# AI-Career-Guidance-Platform

Full-stack career development app with a React and TypeScript frontend, FastAPI backend, PostgreSQL support, and AI-powered career guidance.

An intelligent, full-stack, database-driven career development and employability diagnostic platform. The system evaluates candidate competencies, pinpoints skill gaps against industry benchmarks, synthesizes structured 5-phase career progression roadmaps, scores multi-factor employability readiness, and delivers personalized career guidance.

---

## 🏛️ Project Architecture

The repository is organized into distinct full-stack tiers:

```text
ai-career-guidance-platform/
│
├── frontend/               # React 19 + TypeScript + Tailwind CSS v4 + Vite
│   ├── public/             # Static public assets
│   ├── src/                # UI components, pages, contexts, services, types
│   ├── .env.example        # Frontend environment template
│   ├── package.json        # Frontend dependencies and build configuration
│   ├── tsconfig.json       # TypeScript frontend configuration
│   └── vite.config.ts      # Vite dev server and /api proxy configuration
│
├── backend/                # Python FastAPI REST API with SQLAlchemy ORM
│   ├── app/                # Routers, intelligence services, database models, schemas
│   ├── analytics/          # Statistical correlation and academic analytics
│   ├── data/               # Career benchmarks and synthetic datasets
│   ├── scripts/            # Database migration utilities
│   ├── tests/              # End-to-end integration and interview test suites
│   ├── .env.example        # Backend environment template
│   ├── requirements.txt    # Python dependencies
│   └── career_guidance.db  # SQLite database
│
├── package.json            # Root workspace orchestration scripts
├── run-frontend.bat        # 1-click launcher for React Vite frontend
├── run-backend.bat         # 1-click launcher for FastAPI backend
├── run-analytics.bat       # 1-click launcher for statistical analytics suite
└── start-both.bat          # 1-click launcher for running both services concurrently
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.10+** (tested on Python 3.14)
- **Node.js 18+** with npm

### Option A: One-Click Launchers (Windows)
Double-click or run from command prompt:
- `start-both.bat` — Starts both the Python FastAPI backend and the React Vite frontend in parallel.
- Alternatively, launch them individually using `run-backend.bat` and `run-frontend.bat`.

### Option B: Terminal / Command Line

#### 1. Start the Python FastAPI Backend
```powershell
# From project root:
.\backend\venv\Scripts\Activate.ps1
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- **Backend API**: http://127.0.0.1:8000
- **Interactive Swagger Documentation**: http://127.0.0.1:8000/docs
- *Database is automatically initialized with 15 standard career tracks and verified resources.*

#### 2. Start the React Frontend
```powershell
# Using root shortcut:
npm run dev:frontend

# Or directly from the frontend directory:
cd frontend
npm run dev
```
- **Frontend URL**: http://localhost:5173
- *Requests to `/api/*` are automatically proxied to `http://127.0.0.1:8000`.*

---

## 🧪 Testing and Verification

### Backend Integration Test Suite
To run the automated 17-step end-to-end API test suite:
```powershell
npm run test:backend
# Or: .\backend\venv\Scripts\python.exe backend/tests/test_api_suite.py
```
This tests:
1. Student registration & JWT authentication
2. Profile creation & academic preferences
3. 15-career benchmark discovery and compatibility scoring
4. 4-tier skill-gap diagnostic classification
5. 12-factor assessment scoring
6. 5-phase career progression roadmap generation and task status updates
7. 6-factor employability readiness calculation
8. Verified skill evidence tracking
9. Interactive technical interview simulation and rubric evaluation
10. Deterministic ATS resume keyword analysis
11. AI conversational career advisor responses

### Frontend Linting & Production Build
```powershell
npm run lint    # Executes TypeScript typechecking (tsc --noEmit)
npm run build   # Generates production distribution in frontend/dist/
```

---

## 📊 Academic Research & Analytics Suite
Run the statistical analysis and research evaluation suite:
```powershell
.\run-analytics.bat
```
Generates student cohort benchmarks, skill-gap deficit distributions, and academic thesis evaluation documents in `backend/data/` and `backend/analytics/`.

---

## 💻 Available Pages & Core Features

| Route | View | Description |
|---|---|---|
| `/` | Landing Page | Hero section, system features, and quick login entrypoint |
| `/login` | Authentication | Sign in with email or click 1-click demo login buttons |
| `/register` | Onboarding | Create student profile, select target career, and set academic baseline |
| `/dashboard` | Student Cockpit | Central dashboard with employability score ring, active milestones, and next action items |
| `/discovery` | Career Discovery | Rank compatibility across 15 career pathways using vector similarity |
| `/explorer/:id` | Career Explorer | In-depth role requirements, capstones, certifications, and compensation ranges |
| `/skills` | Skill-Gap Diagnostic | 4-tier matrix (Demonstrated, Developing, Priority Gaps, Advanced Target) |
| `/roadmap` | Career Roadmap | 5-phase career curriculum with interactive task check-offs |
| `/employability` | Readiness Dashboard | 6-factor breakdown (Skills, Academic, Evidence, Roadmap, Interview, ATS) with bottleneck diagnosis |
| `/resume` | Resume ATS Optimizer | Instant scoring, keyword extraction, and metric-driven bullet point enhancements |
| `/interview` | Mock Interview Arena | Role-tailored technical & behavioral interview simulation with rubric feedback |
| `/evidence` | Skill Evidence | Portfolio of verified GitHub repositories, live demo URLs, and certifications |
| `/learning` | Learning Resources | Curated, free educational courses and documentation mapped to roles |
| `/timeline` | Milestone Timeline | Chronological journal of achievements, assessments, and profile events |
| `/profile` | Profile & Academics | Manage GPA, skills, education history, and career preferences |
| `/settings` | Settings & Preferences | Theme preferences (Light / Dark mode toggle) and notification options |

---

## ⚙️ Environment Configuration

For production hosting, GitHub setup, Vercel frontend settings, and the separate FastAPI/PostgreSQL backend deployment, follow the [deployment guide](DEPLOYMENT.md).

- **Root template**: [`.env.example`](.env.example)
- **Backend template**: [`backend/.env.example`](backend/.env.example)
- **Frontend template**: [`frontend/.env.example`](frontend/.env.example)

By default, the platform runs out-of-the-box using the embedded SQLite database (`backend/career_guidance.db`) and local algorithmic intelligence engines. If a `GEMINI_API_KEY` is provided in `backend/.env`, the chat advisor unlocks Google GenAI live responses.
