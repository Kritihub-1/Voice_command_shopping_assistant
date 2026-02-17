# Google Cloud Deployment Guide

## Prerequisites

1. **Google Cloud Account**
   - Sign up at https://cloud.google.com
   - Free $300 credit for 90 days
   - Always-free tier available

2. **Install Google Cloud CLI**
   ```powershell
   # Download from https://cloud.google.com/sdk/docs/install
   # Or use Chocolatey (if installed)
   choco install google-cloud-sdk
   ```

3. **Verify Installation**
   ```powershell
   gcloud --version
   ```

---

## 1. Initialize Google Cloud Project

### Step 1: Login to Google Cloud
```powershell
gcloud auth login
```
This opens your browser to sign into Google Cloud.

### Step 2: Create a Project (if you don't have one)
```powershell
gcloud projects create voice-shopping-assistant --name="Voice Shopping Assistant"
```

### Step 3: Set Default Project
```powershell
gcloud config set project voice-shopping-assistant
```

### Step 4: Enable Required APIs
```powershell
# App Engine
gcloud services enable appengine.googleapis.com

# Cloud Run (alternative option)
gcloud services enable run.googleapis.com

# Cloud Build (for automated deployments)
gcloud services enable cloudbuild.googleapis.com

# Cloud Storage (for frontend)
gcloud services enable storage-component.googleapis.com
```

---

## 2. Deploy Backend

### Option A: Google Cloud App Engine (Recommended - Easiest)

**1. Deploy from your project root**
```powershell
cd c:\Users\HP\Desktop\coding\voice-shopping-assistant
cd backend
gcloud app deploy
```

**2. Choose region** (select one, e.g., `12` for us-central1)
```
us-central1 (Iowa)
us-east1 (South Carolina)
us-west2 (Los Angeles)
europe-west1 (Belgium)
asia-northeast1 (Tokyo)
```

**3. Confirm deployment**
```
Do you want to continue (Y/n)? Y
```

**4. Get your backend URL**
```powershell
gcloud app describe
# Your app URL will be shown (e.g., https://voice-shopping-assistant.appspot.com)
```

### Option B: Google Cloud Run (More Control, Recommended for Docker)

**1. Build and deploy**
```powershell
cd backend
gcloud run deploy voice-shopping-assistant `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --memory 512Mi `
  --timeout 60s `
  --cpu 2
```

**2. Get your service URL** (provided in output)
```
Service URL: https://voice-shopping-assistant-xxxxx.run.app
```

---

## 3. Deploy Frontend

### Option A: Google Cloud Storage + CDN (Easiest)

**1. Build React app**
```powershell
cd frontend
npm run build
```

**2. Create a bucket**
```powershell
$BUCKET_NAME = "voice-shopping-assistant-frontend"
gsutil mb gs://$BUCKET_NAME
```

**3. Upload build files**
```powershell
gsutil -m -r cp .\build\* gs://$BUCKET_NAME/
```

**4. Configure for single-page app**
```powershell
# For SPA routing (index.html fallback)
gsutil web set -m index.html -e index.html gs://$BUCKET_NAME
```

**5. Make bucket public**
```powershell
gsutil iam ch allUsers:objectViewer gs://$BUCKET_NAME
```

**6. Get your frontend URL**
```powershell
gsutil ls -L gs://$BUCKET_NAME
# URL will be: https://storage.googleapis.com/bucket-name/
```

### Option B: Firebase Hosting (Better - Includes CDN)

**1. Install Firebase CLI**
```powershell
npm install -g firebase-tools
```

**2. Initialize Firebase**
```powershell
firebase login
firebase init hosting
# Select: Use an existing project (voice-shopping-assistant)
# Deploy directory: frontend/build
```

**3. Build and deploy**
```powershell
cd frontend
npm run build
firebase deploy
```

**4. Get your frontend URL**
```
Hosting URL: https://voice-shopping-assistant.web.app
```

---

## 4. Connect Frontend to Backend

**Update API endpoint in frontend**

Edit `frontend/src/services/` or similar API configuration files:

```javascript
// For App Engine backend
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  "https://voice-shopping-assistant.appspot.com";

// For Cloud Run backend
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  "https://voice-shopping-assistant-xxxxx.run.app";
```

**Set CORS in backend** (`backend/app/__init__.py`):

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://voice-shopping-assistant.web.app",
            "https://storage.googleapis.com/voice-shopping-assistant-frontend/"
        ]
    }
})
```

**Redeploy with updated settings**

---

## 5. Monitoring & Logs

### View Logs
```powershell
# App Engine logs
gcloud app logs read -n 50

# Cloud Run logs
gcloud run logs read voice-shopping-assistant --limit 50 --region us-central1
```

### Monitor Performance
```powershell
# Create dashboard
gcloud monitoring dashboards create --config-from-file=- << 'EOF'
{
  "displayName": "Voice Shopping Assistant",
  "mosaicLayout": {
    "columns": 12,
    "tiles": []
  }
}
EOF
```

### Check Resource Usage
```powershell
# App Engine instances
gcloud app instances list

# Cloud Run metrics
gcloud run services describe voice-shopping-assistant --region us-central1
```

---

## 6. Custom Domain (Optional)

**1. Add custom domain**
```powershell
gcloud app custom-domains create yourdomain.com
```

**2. Update DNS records**
Follow Google's instructions to add DNS records for your domain.

**3. Verify**
```powershell
gcloud app custom-domains describe yourdomain.com
```

---

## 7. Environment Variables & Secrets

### Set environment variables
```powershell
# For App Engine
gcloud app deploy --set-env-vars FLASK_ENV=production,API_KEY=your_key

# For Cloud Run
gcloud run deploy voice-shopping-assistant \
  --set-env-vars FLASK_ENV=production,API_KEY=your_key
```

### Use Secret Manager (for sensitive data)
```powershell
# Create secret
echo -n "your-secret-value" | gcloud secrets create api-key --data-file=-

# Grant access to App Engine
gcloud secrets add-iam-policy-binding api-key \
  --member serviceAccount:your-project@appspot.gserviceaccount.com \
  --role roles/secretmanager.secretAccessor
```

---

## 8. Scaling Configuration

### Modify autoscaling (App Engine)

Edit `backend/app.yaml`:
```yaml
automatic_scaling:
  min_instances: 1      # Minimum running instances
  max_instances: 10     # Maximum scaling limit
  min_pending_latency: 30ms
  max_pending_latency: 100ms
```

### Cloud Run scaling
```powershell
gcloud run deploy voice-shopping-assistant \
  --min-instances 1 \
  --max-instances 10 \
  --memory 512Mi
```

---

## 9. Clean Up & Cost Management

### View current costs
```powershell
gcloud billing accounts list
```

### Stop backend service
```powershell
# App Engine
gcloud app services delete default

# Cloud Run
gcloud run services delete voice-shopping-assistant --region us-central1
```

### Delete storage bucket
```powershell
gsutil -m rm -r gs://voice-shopping-assistant-frontend
```

---

## 10. Troubleshooting

### Common Issues

**Port binding error**
- Ensure `$PORT` environment variable is used
- In Dockerfile: `--bind :$PORT` instead of `:8080`

**CORS errors in frontend**
- Update CORS origins in `backend/app/__init__.py`
- Redeploy backend

**Large deployment size**
- Check `.gcloudignore` is excluding unnecessary files
- Remove node_modules: `npm ci --production`

**Health check failing**
- Ensure `/health` endpoint is implemented
- Check timeout settings in app.yaml

**Environment variables not loading**
- Use `gcloud app deploy --set-env-vars KEY=value`
- Verify in Cloud Console

---

## Commands Cheat Sheet

```powershell
# Setup
gcloud auth login
gcloud config set project voice-shopping-assistant

# Deploy
gcloud app deploy                              # App Engine backend
gcloud run deploy [SERVICE] --source .         # Cloud Run backend
firebase deploy                                # Firebase frontend

# Monitor
gcloud app logs read                           # View logs
gcloud app instances list                      # View instances

# Scaling
gcloud app update --splitting-algorithm random # Load balancing

# Cleanup
gcloud app services delete default             # Delete service
gsutil rm -r gs://bucket-name                  # Delete bucket
```

---

## Cost Estimate (Free Tier)

- **Backend**: Free tier covers ~28 F1 instance hours/day
- **Frontend Storage**: 1 GB free storage
- **Cloud Build**: 120 build minutes/day free
- **Total for Small App**: ~$0-5/month after free tier

---

## Next Steps

1. Deploy backend: `gcloud app deploy`
2. Get backend URL from console
3. Update frontend API endpoint
4. Deploy frontend: `firebase deploy`
5. Test your app
6. Monitor logs and performance
7. Set up custom domain (optional)

