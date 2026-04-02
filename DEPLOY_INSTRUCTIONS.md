# Steps to Deploy Your Website to GitHub Pages

## Step 1: Create Repository on GitHub
1. Go to https://github.com/new
2. Repository name: **adq-website**
3. Keep it **Public** (required for GitHub Pages)
4. **DO NOT** initialize with README (we already have one)
5. Click "Create repository"

## Step 2: Link Your Local Repository to GitHub
After creating the repository, GitHub will show you commands. Copy your repository URL and run:

```bash
cd "c:\Users\lx\For MH\website"
git remote add origin https://github.com/YOUR_USERNAME/adq-website.git
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 3: Push to GitHub
```bash
git branch -M main
git push -u origin main
```

## Step 4: Enable GitHub Pages
1. Go to your repository on GitHub
2. Click on **Settings** (top menu)
3. Click on **Pages** (left sidebar)
4. Under "Source", select:
   - Branch: **main**
   - Folder: **/ (root)**
5. Click **Save**

## Step 5: Access Your Website
After 1-2 minutes, your website will be live at:
```
https://YOUR_USERNAME.github.io/adq-website/
```

## Optional: Custom Domain
If you want to use adqdetails.com:
1. In GitHub Pages settings, add your custom domain
2. Update your domain's DNS settings to point to GitHub

---

## Quick Commands Reference

### Check current status:
```bash
git status
```

### See remote URL:
```bash
git remote -v
```

### Update website after changes:
```bash
git add .
git commit -m "Update website"
git push
```

---

**Need help?** 
- GitHub Pages Docs: https://pages.github.com/
- GitHub Support: https://support.github.com/
