# GitHub and Vercel Deployment Guide

## Architecture and production requirements

Deploy the React/Vite frontend on Vercel. Deploy the FastAPI backend as a separate web service (for example, Render) and use a managed PostgreSQL database. The API uses SQLAlchemy for its main reads and writes; MongoDB is only an optional mirror and cannot replace the SQL database. The local SQLite file is ignored by Git and is not persistent hosting storage.

The backend requires `JWT_SECRET_KEY`, `DATABASE_URL`, and `FRONTEND_ORIGINS` in production. Set `ENVIRONMENT=production`. Set `GEMINI_API_KEY` only if you want Gemini-powered features; keep it in the backend host, never in Vercel. The frontend needs `VITE_API_BASE_URL` set to the backend's HTTPS URL ending in `/api`.

## 1. Run and verify locally

Open PowerShell in the project root. Install frontend dependencies:

```powershell
npm --prefix frontend ci
```

Create and activate a Python environment, then install backend dependencies:

```powershell
py -3.12 -m venv backend/venv
backend/venv/Scripts/Activate.ps1
python -m pip install -r backend/requirements.txt
```

Copy `backend/.env.example` to `backend/.env`. For local development, SQLite works. Replace `JWT_SECRET_KEY` with a random local secret and set `GEMINI_API_KEY` only if needed. Start the backend in one PowerShell window:

```powershell
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

Start the frontend in a second window at the project root:

```powershell
npm run dev:frontend
```

Visit `http://localhost:5173`. Check backend health at `http://127.0.0.1:8000/api/health` and API documentation at `http://127.0.0.1:8000/docs`.

Run the project checks from the project root:

```powershell
npm run lint
npm run build
python backend/tests/test_api_suite.py
python backend/tests/test_interview_flow.py
```

The live Gemini interview test at `python backend/tests/test_live_interview.py` makes real external AI requests and may consume API quota. Run it only when you intentionally want to validate the configured Gemini integration.

## 2. Create a GitHub repository and upload the project

In GitHub, create a new empty repository. Do not select options to add a README, license, or `.gitignore` because this folder already contains project files. Copy its HTTPS repository address.

This project is already initialized on `main` and connected to the GitHub repository. To check the current branch and confirm that local environment files are ignored, run from PowerShell at the project root:

```powershell
git status --short
git remote -v
git check-ignore backend/.env backend/career_guidance.db
```

If either sensitive/local file is not listed as ignored, stop and fix `.gitignore` before staging. Stage the source and inspect the staged file list:

```powershell
git add .
git status --short
git diff --cached --name-only
```

Do not commit if `backend/.env`, any real `.env` file, a database file, a virtual environment, or a credential file appears in the staged list. Then commit and push to the connected repository:

```powershell
git commit -m "Prepare application for production deployment"
git push
```

Use `git remote -v` to verify that `origin` points to the intended GitHub repository before pushing.

## 3. Deploy the backend and database

Create a managed PostgreSQL database and a Python web service with a persistent provider. For Render, create a PostgreSQL database, then create a Web Service connected to the GitHub repository.

Use these service settings:

- Root directory: repository root (`.`)
- Runtime: Python
- Build command: `pip install -r backend/requirements.txt`
- Start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/api/health`

Add these environment variables in the backend service dashboard:

| Name | Value |
|---|---|
| `ENVIRONMENT` | `production` |
| `JWT_SECRET_KEY` | A new, randomly generated secret of at least 32 characters |
| `DATABASE_URL` | The provider's PostgreSQL URL; use `postgresql+psycopg://` instead of `postgresql://` at the start if needed |
| `FRONTEND_ORIGINS` | The exact Vercel site origin, e.g. `https://your-project.vercel.app` (no trailing slash) |
| `GEMINI_API_KEY` | Optional; set only in the backend dashboard if using Gemini |

Generate a signing secret in PowerShell with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

For `DATABASE_URL`, use the database provider's private/internal URL when the backend and database share a provider network. URL-encode special characters in the password. Do not use SQLite for a production service. Once the backend deploys, open `https://YOUR-BACKEND-HOST/api/health`; it should return a healthy response and show PostgreSQL as the database. Check `https://YOUR-BACKEND-HOST/docs` for the API documentation.

## 4. Deploy the frontend on Vercel

In Vercel, select **Add New → Project**, import the GitHub repository, then set:

- Root Directory: `frontend`
- Framework Preset: Vite
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm ci`

Add this frontend environment variable for **Production** (and Preview if you want previews to call the same backend):

| Name | Value |
|---|---|
| `VITE_API_BASE_URL` | `https://YOUR-BACKEND-HOST/api` |

Set this variable in Vercel; do not commit a production `.env` file. The `.env.example` files document local defaults and required variable names only. Deploy. The included `frontend/vercel.json` rewrites direct page visits to the SPA entry point so routes such as `/interview` work after refresh. After Vercel assigns the production domain, add that exact origin to the backend's `FRONTEND_ORIGINS` variable and redeploy/restart the backend.

## 5. Verify the live application

Open the Vercel domain and check the landing page, registration, login, onboarding, dashboard, and each main route. Refresh a nested route such as `/interview` directly. Register a test account, complete onboarding, and check the main career, roadmap, resume, evidence, and interview flows. Check browser developer tools' Network panel for failed `/api` calls. Confirm the backend health route reports PostgreSQL.

Use a test account and non-production data during verification. Confirm that Gemini features work only if `GEMINI_API_KEY` was configured on the backend. Never paste backend secrets into browser developer tools or Vercel frontend variables.

## Troubleshooting

- **Vercel build fails:** Confirm Root Directory is `frontend`, then use `npm ci` and `npm run build` locally from the frontend folder. Check the build log for the first TypeScript or dependency error.
- **Nested page returns 404:** Confirm the Vercel project root is `frontend` and `frontend/vercel.json` is present in the deployed commit.
- **API calls fail or show CORS errors:** Confirm `VITE_API_BASE_URL` ends in `/api`; confirm the backend is healthy; set `FRONTEND_ORIGINS` to the exact deployed Vercel origin without a trailing slash, then redeploy the backend.
- **Request failed with status 405:** The Vercel frontend is receiving the API POST itself. Deploy the FastAPI backend, set Vercel's `VITE_API_BASE_URL` to `https://YOUR-BACKEND-HOST/api`, and redeploy the frontend. The app now shows a configuration message instead of issuing production requests to a relative `/api` path when this setting is missing.
- **Database connection or startup failure:** Confirm `DATABASE_URL` is the managed PostgreSQL URL, begins with `postgresql+psycopg://` (or `postgresql://`, which this app normalizes), and the service can reach the database. Check allowed network access and URL-encode special password characters.
- **Backend refuses production startup:** Set `ENVIRONMENT=production`, a `JWT_SECRET_KEY` at least 32 characters long, PostgreSQL `DATABASE_URL`, and `FRONTEND_ORIGINS`.
- **Gemini returns unavailable:** Set a valid `GEMINI_API_KEY` in the backend host and redeploy/restart the backend. Do not set it as a `VITE_` variable.
- **Login sessions stop working after secret change:** Changing `JWT_SECRET_KEY` invalidates previously issued tokens; users must sign in again.

## 6. Deploy updates and optionally configure a custom domain

After making changes, run lint, build, and relevant backend checks locally. Commit and push:

```powershell
git add .
git status --short
git commit -m "Describe the update"
git push
```

Vercel and the backend host will deploy from the connected branch according to their deployment settings. Review both deployment logs and repeat the live health, route-refresh, and API checks.

For a custom domain, open the Vercel project **Settings → Domains**, add the domain, and follow the DNS records Vercel provides at your domain registrar. After DNS verifies, update `FRONTEND_ORIGINS` to the new `https://` origin and redeploy the backend. Keep the Vercel domain in that list too if you will continue using it.
