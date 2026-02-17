"""
WSGI entry point for production deployment with Gunicorn
"""
import os
from app import create_app

# Create Flask app
app = create_app()

# Set production environment variables
os.environ.setdefault('FLASK_ENV', 'production')

@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'ok'}, 200

if __name__ == "__main__":
    app.run()
