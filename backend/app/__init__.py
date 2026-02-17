from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # Production configuration
    if os.environ.get('FLASK_ENV') == 'production':
        app.config['ENV'] = 'production'
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
        # Stricter CORS for production (update to your domain)
        CORS(app, resources={r"/api/*": {"origins": ["https://yourdomain.com"]}})
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
