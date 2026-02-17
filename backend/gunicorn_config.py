"""
Gunicorn configuration for production deployment
"""
import multiprocessing
import os

# Server socket
bind = os.getenv('GUNICORN_BIND', "0.0.0.0:8000")
backlog = 2048

# Worker processes
workers = int(os.getenv('GUNICORN_WORKERS', max(multiprocessing.cpu_count() - 1, 2)))
worker_class = "sync"
worker_connections = 1000
timeout = int(os.getenv('GUNICORN_TIMEOUT', 60))
keepalive = 5

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = os.getenv('GUNICORN_LOG_LEVEL', "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "voice-assistant"

# SSL (configure if using HTTPS)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Application
wsgi_app = "wsgi:app"
