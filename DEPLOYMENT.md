# ADQ Website - Supabase + Vercel Deployment Guide

## Prerequisites
- GitHub account
- Supabase account (already created: https://kepyyudsrfhofseownnj.supabase.co)
- Vercel account (free)

---

## Step 1: Set Up Supabase Database

1. Go to your Supabase dashboard: https://supabase.com/dashboard/project/kepyyudsrfhofseownnj
2. Click **"SQL"** in the left sidebar
3. Click **"New Query"**
4. Copy and paste the contents of `backend/supabase-setup.sql`
5. Click **"Run"** to create all tables
6. You should see "Success. No rows returned"

---

## Step 2: Deploy Backend to Vercel

1. Go to https://vercel.com/new
2. Import your GitHub repository: `Alool266/-adq-website`
3. Select the **backend** folder as the root directory
4. Add Environment Variables:
   - `SUPABASE_URL` = `https://kepyyudsrfhofseownnj.supabase.co`
   - `SUPABASE_PASSWORD` = `sWie0KkZwQ2V231p`
5. Click **"Deploy"**
6. Wait for deployment (2-3 minutes)
7. Note your backend URL (e.g., `https://adq-website-backend.vercel.app`)

---

## Step 3: Deploy Frontend to Vercel

1. Go to https://vercel.com/new
2. Import your GitHub repository: `Alool266/-adq-website`
3. Select the **frontend** folder as the root directory
4. Add Environment Variable:
   - `REACT_APP_API_URL` = `[YOUR_BACKEND_URL]` (from Step 7)
5. Click **"Deploy"**
6. Wait for deployment (2-3 minutes)

---

## Step 4: Initialize Database

After backend deployment completes:

1. Visit: `[YOUR_BACKEND_URL]/setup`
2. You should see: `{"message": "Admin user created! You can now login with admin/admin123"}`
3. Optionally visit: `[YOUR_BACKEND_URL]/debug` to verify admin exists

---

## Step 5: Login and Test

1. Go to your frontend URL
2. Login with:
   - **Username**: `admin`
   - **Password**: `admin123`
3. You should now have full access to the admin panel!

---

## Important Notes

- **Database**: Supabase PostgreSQL persists all data automatically
- **File Uploads**: Currently stored locally on Vercel (ephemeral). For production, use Supabase Storage.
- **Environment Variables**: Keep your Supabase password secure. Never commit it to Git.
- **Custom Domain**: You can add a custom domain in Vercel settings if needed.

---

## Troubleshooting

### Backend deployment fails?
- Check that `backend/vercel.json` exists
- Ensure `psycopg2-binary` is in `requirements.txt`
- Check Vercel logs for specific errors

### Frontend can't connect?
- Verify `REACT_APP_API_URL` is set correctly in Vercel environment variables
- Redeploy frontend after changing env vars

### Login fails?
- Visit `[BACKEND_URL]/reset-admin` to reset admin password
- Check backend logs for errors
- Verify database tables were created in Supabase

---

## Files Modified for Supabase

- `backend/app/database.py` - Updated to use Supabase PostgreSQL
- `backend/requirements.txt` - Added `psycopg2-binary`
- `backend/vercel.json` - Vercel deployment config
- `backend/supabase-setup.sql` - Database schema
- `backend/app/main.py` - Simplified for Vercel serverless
