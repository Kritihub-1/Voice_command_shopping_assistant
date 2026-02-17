# Quick Deploy to Google Cloud (5 Minutes)

## ⚡ Quick Setup

**Step 1: Install Google Cloud CLI**
```powershell
# Download from: https://cloud.google.com/sdk/docs/install
# Or use Chocolatey:
choco install google-cloud-sdk
```

**Step 2: Authenticate**
```powershell
gcloud auth login
# Browser opens for Google sign-in
```

**Step 3: Create Project**
```powershell
gcloud projects create voice-shopping-assistant --name="Voice Shopping Assistant"
gcloud config set project voice-shopping-assistant
```

**Step 4: Enable APIs**
```powershell
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

---

## 🚀 Deploy Backend (App Engine)

```powershell
cd c:\Users\HP\Desktop\coding\voice-shopping-assistant\backend
gcloud app deploy
```

**When prompted:**
- Choose region: `12` (us-central1)
- Confirm: `Y`

**Get your backend URL:**
```
https://voice-shopping-assistant.appspot.com
```

---

## 🎨 Deploy Frontend (Firebase)

**Step 1: Install Firebase CLI**
```powershell
npm install -g firebase-tools
```

**Step 2: Login**
```powershell
firebase login
```

**Step 3: Initialize Firebase**
```powershell
cd c:\Users\HP\Desktop\coding\voice-shopping-assistant
firebase init hosting
# Use existing project: voice-shopping-assistant
# Build directory: frontend/build
# Configure SPA: Y
```

**Step 4: Build and Deploy**
```powershell
cd frontend
npm run build
firebase deploy
```

**Get your frontend URL:**
```
https://voice-shopping-assistant.web.app
```

---

## 🔗 Connect Frontend to Backend

Edit `frontend/.env` or `frontend/src/services/*`:

```javascript
const API_BASE_URL = "https://voice-shopping-assistant.appspot.com";
```

Then redeploy frontend:
```powershell
cd frontend
npm run build
firebase deploy
```

---

## ✅ Verify Deployment

**Backend health check:**
```powershell
# Should return {"status": "ok"}
curl https://voice-shopping-assistant.appspot.com/health
```

**View logs:**
```powershell
gcloud app logs read -n 50
```

---

## 📊 Monitor Your App

```powershell
# View backend logs
gcloud app logs read

# View deployed versions
gcloud app versions list

# View instances
gcloud app instances list

# Traffic splitting
gcloud app traffic-split --split-by ip
```

---

## 💰 Cost (Very Cheap)

- Backend: Free tier covers ~28 F1 instance hours/day
- Frontend: Firebase free tier (50GB CDN)
- **Total: ~$0-5/month after free tier**

---

## 🆘 Troubleshooting

**Backend won't deploy?**
```powershell
# Check logs
gcloud app logs read
```

**CORS errors in app?**
- Ensure CORS is configured in `backend/app/__init__.py`
- Update with your frontend URL

**Frontend not loading?**
- Ensure API_BASE_URL points to your Google Cloud backend

---

**That's it! Your app is now live on Google Cloud! 🎉**

See [GOOGLE_CLOUD_DEPLOYMENT.md](GOOGLE_CLOUD_DEPLOYMENT.md) for detailed guide.
