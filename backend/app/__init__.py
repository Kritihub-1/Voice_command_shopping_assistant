from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # CORS Configuration
    if os.environ.get('FLASK_ENV') == 'production':
        app.config['ENV'] = 'production'
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
        # Allow Vercel frontend and localhost for production
        allowed_origins = [
            "http://localhost:3000",
            "http://localhost:5000",
        ]
        # Add Vercel frontend URL if available
        vercel_url = os.environ.get('VERCEL_URL')
        if vercel_url:
            allowed_origins.append(f"https://{vercel_url}")
        CORS(app, resources={r"/api/*": {"origins": allowed_origins}})
    else:
        # Development configuration
        app.config['ENV'] = 'development'
        app.config['DEBUG'] = True
        CORS(app)  # Allow all origins in development
    
    # Register blueprints
    from app.routes import shopping_routes, recommendation_routes, voice_routes
    app.register_blueprint(shopping_routes.bp)
    app.register_blueprint(recommendation_routes.bp)
    app.register_blueprint(voice_routes.bp)
    
    return app
