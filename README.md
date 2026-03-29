# n.siva Portfolio (Frontend + Backend + DB)

## Project Structure

- `frontend/index.html`
- `frontend/style.css`
- `frontend/script.js`
- `frontend/profile-photo-placeholder.svg`
- `backend/server.py`
- `backend/database.py`
- `backend/portfolio.db`

## Run Locally

1. Install Python 3.10+.
2. From project root:
   - `pip install -r requirements.txt`
   - `python -c "from backend.database import init_db; init_db()"`
   - `python backend/server.py`
3. Open: `http://localhost:5000`

## Set Your Real Profile Photo

1. Copy your photo into `frontend/` as `profile.jpg`.
2. In `frontend/index.html`, change:
   - `src="./profile-photo-placeholder.svg"`
   - to `src="./profile.jpg"`

## Deploy to GitHub + Render

1. Create a new GitHub repository and push this project.
2. In Render:
   - New > Web Service
   - Connect GitHub repo
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn backend.server:app`
3. Deploy.

> Note: Render free service can restart after inactivity. SQLite is ephemeral on free instances, so form entries may reset after redeploy/restart.

## CI/CD (GitHub Actions)

This repo includes `.github/workflows/ci-cd.yml`:

- **CI**: runs on every push/PR. Installs Python deps and performs basic smoke checks.
- **CD** (optional): on push to `main`, triggers a Render deploy hook if you add the secret.

### Enable CD (optional)

1. In Render, open your service → Settings → Deploy Hook → copy the hook URL.
2. In GitHub repo → Settings → Secrets and variables → Actions → New repository secret:
   - Name: `RENDER_DEPLOY_HOOK`
   - Value: (paste Render deploy hook URL)
