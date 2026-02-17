# Production Deployment Guide

## Backend Deployment

### Prerequisites
- Python 3.8+
- Virtual environment activated
- All dependencies installed: `pip install -r requirements.txt`

### Production Server Setup

#### Option 1: Gunicorn (Recommended)

**1. Install Gunicorn (already in requirements.txt)**
```powershell
pip install -r requirements.txt
```

**2. Run with Gunicorn**
```powershell
# Basic (4 workers, single process)
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app

# With more workers (8 workers for better concurrency)
gunicorn -w 8 -b 0.0.0.0:8000 wsgi:app

# With custom timeout (60 seconds)
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 60 wsgi:app

# Background mode (using start /B on Windows)
start /B gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

**3. Environment Setup**
```powershell
# Load production environment variables
$env:FLASK_ENV = "production"
$env:FLASK_DEBUG = "0"
```

#### Option 2: Docker Deployment

```powershell
# Build Docker image
docker build -f ../Dockerfile -t voice-assistant-backend .

# Run container
docker run -p 8000:8000 -e FLASK_ENV=production voice-assistant-backend
```

### Gunicorn Configuration

For better performance, create `gunicorn_config.py`:

```python
import multiprocessing
import os

# Server config
bind = "0.0.0.0:8000"
workers = max(multiprocessing.cpu_count() - 1, 2)
worker_class = "sync"
worker_connections = 1000
timeout = 60
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "voice-assistant"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None
```

Then run:
```powershell
gunicorn -c gunicorn_config.py wsgi:app
```

### Performance Tuning

**CPU-Bound Settings** (NLP Processing):
- Workers = CPU cores * 2
- Worker class = "sync"

**Memory Considerations**:
- Monitor memory usage
- Set resource limits if needed
- Consider load balancing at 4-8 workers

### Monitoring

**Health Check Endpoint**:
```
GET http://your-server:8000/health
Response: {"status": "ok"}
```

**Log Monitoring**:
```powershell
# Monitor Gunicorn output
# Logs appear in console or configured log file
```

## Frontend Deployment

### Production Build

**1. Create Optimized Build**
```powershell
cd ../frontend
npm run build
```
Creates `build/` folder with optimized assets.

**2. Configure API Endpoint**

Update `frontend/src/services/` to use production backend URL:

```javascript
// Change from localhost:5000 to your production URL
const API_BASE_URL = process.env.REACT_APP_API_URL || "https://your-domain.com/api";
```

**3. Deploy Frontend**

**Option A: Static Hosting (Recommended)**
- Upload `frontend/build/` to:
  - Vercel
  - Netlify
  - AWS S3 + CloudFront
  - GitHub Pages

**Option B: Node Server**
```powershell
npm install -g serve
serve -s build -l 3000
```

## Full Stack with Docker Compose

```powershell
# Production deployment
docker-compose -f docker-compose.yml up -d
```

## Security Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=0`
- [ ] Use HTTPS/TLS
- [ ] Set secure CORS origins (not * )
- [ ] Add authentication/authorization if needed
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Set up log rotation
- [ ] Configure firewall rules
- [ ] Monitor system resources

## Troubleshooting

**Port Already in Use**:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000
# Kill process by PID
taskkill /PID <PID> /F
```

**Memory Issues**:
```powershell
# Reduce workers
gunicorn -w 2 -b 0.0.0.0:8000 wsgi:app
```

**CORS Issues**:
- Ensure REACT_APP_API_URL matches backend origin
- Backend has CORS configured for frontend domain

## Performance Metrics

Monitor in production:
- Response time (target: <200ms for API calls)
- Error rate (target: <0.1%)
- Worker utilization
- Memory usage per worker
- CPU usage
