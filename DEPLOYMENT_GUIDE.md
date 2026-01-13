# Deployment Guide - Render.com

This project is ready to be deployed on **Render.com** (a free cloud platform).

## 🚀 Steps to Deploy

### 1. Push to GitHub
1. Create a new repository on GitHub (e.g., `hospital-cms`).
2. Run these commands in your project folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/hospital-cms.git
   git push -u origin main
   ```

### 2. Create Web Service on Render
1. Go to [dashboard.render.com](https://dashboard.render.com/).
2. Click **New +** -> **Web Service**.
3. Select "Build and deploy from a Git repository".
4. Connect your GitHub account and select the `hospital-cms` repo.

### 3. Configure Settings
Render will auto-detect Python. Ensure these settings:
- **Name:** `hospital-demo` (or similar)
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app` (This is already in your `Procfile`)
- **Instance Type:** Free

### 4. Deploy!
- Click **Create Web Service**.
- Wait for the deployment to finish (green checkmark).
- Your URL will be something like `https://hospital-demo.onrender.com`.

## ⚠️ Database Note
Since we are using SQLite (`hospital.db`), the database file is stored on the server's disk.
**On Render's Free Tier:** The disk is "ephemeral", meaning **data will be wiped** every time the app restarts or you redeploy.
- For a **Resume Project / Demo**: This is usually fine.
- For **Production**: You would need to connect a hosted PostgreSQL or MySQL database (like Render's managed PostgreSQL).
