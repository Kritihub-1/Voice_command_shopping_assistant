# Deploy to Vercel in 5 Minutes

## ⚡ Fastest Setup

**Important**: Vercel is **best for frontend**. For backend, use **Render** (free).

---

## Step 1: Setup GitHub (2 min)

```powershell
cd c:\Users\HP\Desktop\coding\voice-shopping-assistant

# Initialize git (if not done)
git init
git add .
git commit -m "Initial commit"
```

Go to **https://github.com/new**:
- Create repo: `voice-shopping-assistant`
- Copy HTTPS URL

```powershell
git remote add origin https://github.com/YOUR_USERNAME/voice-shopping-assistant.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend (3 min) - Render

1. Go to **https://render.com**
2. Sign up with GitHub
3. Click **"New Web Service"**
4. Select your repo
5. Settings:
   ```
   Name: voice-shopping-assistant-api
   Root: backend
   Build: pip install -r requirements.txt
   Start: gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app
   ```
6. Click **"Deploy"**
7. **Copy the URL** when done (e.g., `https://voice-shopping-assistant-api.onrender.com`)

⏱️ Takes 3-5 minutes

---

## Step 3: Deploy Frontend (5 min) - Vercel

1. Go to **https://vercel.com**
2. Sign up with GitHub
3. Click **"Add New"** → **"Project"**
4. Import your repo
5. Settings:
   ```
   Framework: Create React App
   Root Directory: frontend
   Build Cmd: npm run build
   Output: build
   ```
6. **Environment Variables** (important!):
   ```
   REACT_APP_API_URL = https://voice-shopping-assistant-api.onrender.com
   ```
   (Copy from Step 2)

7. Click **"Deploy"** ✅

Done! Your frontend is live! 🎉

---

## Step 4: Update CORS (1 min)

Edit `backend/app/__init__.py`:

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://YOUR_PROJECT.vercel.app",  # <-- Your Vercel URL
            "http://localhost:3000"
        ]
    }
})
```

Push changes:
```powershell
git add .
git commit -m "Update CORS"
git push
```

Render auto-redeploys ✅

---

## 🎉 Done!

**Your app lives at:**
- Frontend: `https://YOUR_PROJECT.vercel.app`
- Backend API: `https://voice-shopping-assistant-api.onrender.com`

**Test it:**
```powershell
curl https://voice-shopping-assistant-api.onrender.com/health
```

Should return: `{"status":"ok"}`

---

## Costs

- **Vercel**: Free forever for static sites
- **Render**: Free (sleeps after 15 min idle)
- **Total**: $0/month

Upgrade Render to $7/mo for always-on if needed.

---

## Common Issues

**CORS errors?**
- Update CORS origins in backend
- Redeploy

**Can't find sources?**
- Wait 30 seconds after pushing
- Refresh browser

**Backend sleeping?**
- Free Tier: Inactive after 15 min
- Paid Tier: Always running ($7/mo)

---

See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for detailed guide.
