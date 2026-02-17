# Vercel Deployment Guide

## Overview

Vercel is **perfect for React frontend**. For the backend, you have two options:

1. **Recommended**: Frontend on Vercel + Backend on Render (Free, Simple)
2. **Advanced**: Everything on Vercel with Serverless Functions

---

## Option 1: Vercel Frontend + Render Backend (EASIEST)

### Step 1: Prepare GitHub Repository

**1. Initialize Git (if not done)**
```powershell
cd c:\Users\HP\Desktop\coding\voice-shopping-assistant
git init
git add .
git commit -m "Initial commit"
```

**2. Create GitHub repo**
- Go to https://github.com/new
- Create repo: `voice-shopping-assistant`
- Copy HTTPS URL

**3. Push code**
```powershell
git remote add origin https://github.com/YOUR_USERNAME/voice-shopping-assistant.git
git branch -M main
git push -u origin main
```

---

### Step 2: Deploy Backend on Render (FREE)

**1. Go to https://render.com**
- Sign up with GitHub
- Click "New +"
- Select "Web Service"
- Connect your GitHub repo

**2. Configure Backend**
```
Name: voice-shopping-assistant-api
Runtime: Python 3.9
Build Command: pip install -r requirements.txt
Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app
Root Directory: backend
```

**3. Deploy**
- Click "Deploy"
- Wait 3-5 minutes
- Copy the URL (e.g., `https://voice-shopping-assistant-api.onrender.com`)

---

### Step 3: Deploy Frontend on Vercel (FREE)

**1. Go to https://vercel.com**
- Sign up with GitHub
- Click "Add New..."
- Select "Project"
- Import your GitHub repo

**2. Configure Frontend**
```
Framework: Create React App
Root Directory: frontend
Build Command: npm run build
Output Directory: build
```

**3. Set Environment Variables**
```
REACT_APP_API_URL = https://voice-shopping-assistant-api.onrender.com
```

**4. Deploy**
- Click "Deploy"
- Frontend live at: `https://your-project.vercel.app`

---

### Step 4: Connect Frontend to Backend

**1. Update API calls in frontend**

Edit `frontend/.env`:
```
REACT_APP_API_URL=https://voice-shopping-assistant-api.onrender.com
```

Or update in your service files:
```javascript
// frontend/src/services/api.js (or similar)
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  "https://voice-shopping-assistant-api.onrender.com";
```

**2. Update CORS in backend**

Edit `backend/app/__init__.py`:
```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://your-project.vercel.app",
            "http://localhost:3000"
        ]
    }
})
```

**3. Redeploy**
```powershell
git add .
git commit -m "Update API endpoint"
git push origin main
```

---

## Option 2: Everything on Vercel (Advanced)

### Alternative: Using Vercel Serverless Functions

If you want Flask on Vercel using serverless functions:

**1. Restructure backend for serverless**

Create `/api` directory:
```
api/
  app.py (your Flask app)
  requirements.txt
```

**2. Create `vercel.json`**
```json
{
  "buildCommand": "pip install -r requirements.txt",
  "outputDirectory": ".",
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/app.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    },
    {
      "handle": "filesystem"
    },
    {
      "src": "/(.*)",
      "status": 404,
      "dest": "/frontend/index.html"
    }
  ]
}
```

**3. Modify Flask app for serverless**
```python
from app import create_app

app = create_app()

# Serverless handler
def handler(request):
    # Vercel serverless handler
    with app.app_context():
        return app(environ=request.environ, start_response=request.start_response)
```

**Note**: This is more complex. Stick with **Option 1** for simplicity.

---

## Quick Summary

### Option 1 (Recommended)
```
Frontend: Vercel ✅ (Easy, Fast)
Backend: Render ✅ (Easy, Free)
Total Time: 15 minutes
Cost: $0
```

### Option 2 (All in Vercel)
```
Frontend: Vercel ✅
Backend: Vercel Serverless ⚠️ (Complex, Cold starts)
Total Time: 45 minutes
Cost: $0 (with limitations)
```

---

## Deployment Checklist

- [ ] Git repository created on GitHub
- [ ] Code pushed to GitHub
- [ ] Backend deployed on Render
- [ ] Frontend deployed on Vercel
- [ ] Backend URL copied and added to frontend env
- [ ] CORS updated in backend
- [ ] Frontend and backend communicate ✅

---

## Testing Your Deployment

**Test backend API:**
```powershell
# Replace with your Render URL
curl https://voice-shopping-assistant-api.onrender.com/health
```

**Test frontend:**
- Visit: `https://your-project.vercel.app`
- Should load without CORS errors
- API calls should work

---

## Useful Commands

```powershell
# View Vercel deployments
vercel ls

# Redeploy frontend
git push origin main  # Auto-redeploys on push

# Render logs
# Visit Render dashboard > Logs tab
```

---

## Environment Variables

### Vercel (Frontend)
- `REACT_APP_API_URL`: Backend URL

### Render (Backend)
- `FLASK_ENV`: production
- `FLASK_DEBUG`: 0

---

## Custom Domain (Optional)

### Vercel
1. Go to Project Settings
2. Domains
3. Add custom domain
4. Update DNS records

### Render
1. Go to Service Settings
2. Custom Domain
3. Add your domain

---

## Troubleshooting

**CORS errors?**
- Update CORS origins in `backend/app/__init__.py`
- Redeploy backend

**Vercel can't find build?**
- Ensure Root Directory is set to `frontend`
- Check Build Command: `npm run build`

**Backend sleeping on Render (free tier)?**
- Free tier goes idle after 15 minutes
- Upgrade to paid ($7/month) for always-on
- Or use Railway ($5/mo credit)

**API calls failing?**
- Check backend URL in frontend env variables
- Verify backend is running: `https://backend-url.onrender.com/health`

---

## Next Steps

1. Create GitHub repo
2. Push code
3. Deploy backend to Render (5 min)
4. Deploy frontend to Vercel (5 min)
5. Test and celebrate! 🎉

