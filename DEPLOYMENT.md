# Deploy ADQ Website to Render.com

Complete step-by-step guide to deploy the ADQ website with admin panel on Render.com (free tier).

## Overview

- **Backend API**: FastAPI + SQLite (hosted on Render)
- **Frontend Admin**: React (hosted on Render Static Site)
- **Static Website**: Original HTML/CSS/JS (hosted on GitHub Pages or Render)

## Prerequisites

1. A [Render.com](https://render.com) account (free)
2. Your GitHub repository: https://github.com/Alool266/-adq-website
3. Git installed on your computer

---

## Step 1: Push Latest Code to GitHub

First, make sure all your code is pushed to GitHub:

```bash
cd c:/Users/lx/Desktop/-adq-website
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

---

## Step 2: Deploy Backend to Render

### 2.1 Create a New Web Service

1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select the repository: `Alool266/-adq-website`
5. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `adq-backend` |
| **Region** | Choose closest to your users |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt && python init_db.py` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | **Free** |

### 2.2 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Click **"Generate"** to create a random string |
| `DATABASE_URL` | `sqlite:///./data/adq_website.db` |

### 2.3 Add Persistent Disk (for database & uploads)

Scroll to **"Disks"** → **"Add Disk"**:

| Setting | Value |
|---------|-------|
| **Name** | `backend-data` |
| **Mount Path** | `/opt/render/project/src/data` |
| **Size** | `1 GB` (free tier) |

### 2.4 Deploy

Click **"Create Web Service"** and wait for deployment (~3-5 minutes).

**Note your backend URL**: `https://adq-backend.onrender.com`

---

## Step 3: Deploy Frontend Admin Panel to Render

### 3.1 Create a Static Site

1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Static Site"**
3. Select the repository: `Alool266/-adq-website`
4. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `adq-admin` |
| **Branch** | `main` |
| **Root Directory** | `frontend` |
| **Build Command** | `npm install && npm run build` |
| **Publish Directory** | `build` |
| **Plan** | **Free** |

### 3.2 Add Environment Variables

| Key | Value |
|-----|-------|
| `REACT_APP_API_URL` | `https://adq-backend.onrender.com` (your backend URL) |

### 3.3 Deploy

Click **"Create Static Site"** and wait for deployment (~2-3 minutes).

**Note your admin URL**: `https://adq-admin.onrender.com`

---

## Step 4: Update API URL in Frontend

Update the frontend API service to use the production backend URL:

1. Edit `frontend/src/services/api.js`
2. Change `API_URL` to your Render backend URL:

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'https://adq-backend.onrender.com/api/v1';
```

3. Commit and push:

```bash
git add frontend/src/services/api.js
git commit -m "Update API URL for production"
git push origin main
```

---

## Step 5: Initialize Database

After the backend is deployed, you need to run the database initialization:

### Option A: Automatic (via Render Dashboard)
1. Go to your backend service on Render
2. Click **"Shell"** tab
3. Run: `python init_db.py`

### Option B: Manual (via API)
Open your browser and visit:
```
https://adq-backend.onrender.com/health
```

If it returns `{"status": "healthy"}`, the backend is working.

---

## Step 6: Access Your Admin Panel

1. Go to: `https://adq-admin.onrender.com`
2. Login with:
   - **Username**: `admin`
   - **Password**: `admin123`
3. **⚠️ Change the password immediately!**

---

## Step 7: (Optional) Deploy Static Website to GitHub Pages

For the main website (non-admin), you can use GitHub Pages:

1. Go to your repository settings on GitHub
2. Navigate to **Pages**
3. Set source to `main` branch, `/` folder
4. Your site will be at: `https://Alool266.github.io/-adq-website/`

---

## URLs After Deployment

| Service | URL |
|---------|-----|
| **Backend API** | `https://adq-backend.onrender.com` |
| **API Docs** | `https://adq-backend.onrender.com/docs` |
| **Admin Panel** | `https://adq-admin.onrender.com` |
| **Static Website** | `https://Alool266.github.io/-adq-website/` |

---

## Troubleshooting

### Backend won't start
- Check logs in Render dashboard
- Ensure `init_db.py` runs successfully
- Verify environment variables are set

### Frontend can't connect to backend
- Check `REACT_APP_API_URL` environment variable
- Ensure CORS is configured in backend (already done)
- Check browser console for errors

### Images not uploading
- Ensure persistent disk is mounted correctly
- Check disk space in Render dashboard
- Verify file size limits (default: 5MB)

### Database not persisting
- Ensure persistent disk is configured
- Check mount path: `/opt/render/project/src/data`

---

## Admin Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |

**⚠️ IMPORTANT**: Change the default password after first login!

---

## Cost Estimate

| Service | Plan | Cost |
|---------|------|------|
| Backend (Web Service) | Free | $0/month |
| Frontend (Static Site) | Free | $0/month |
| Database (SQLite on Disk) | Free | $0/month |
| **Total** | | **$0/month** |

---

## Notes

- Render free tier has a 15-minute spin-down period (first request after inactivity takes ~30 seconds)
- For production use, consider upgrading to a paid plan ($7/month)
- SQLite is fine for small sites; upgrade to PostgreSQL for larger deployments

---

## Support

For issues or questions:
- Render Docs: https://render.com/docs
- GitHub Issues: https://github.com/Alool266/-adq-website/issues
