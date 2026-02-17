# Environment Configuration

## Development Environment

### Backend
Create `.env` file in backend/ directory:
```
FLASK_ENV=development
FLASK_DEBUG=1
API_PORT=5000
```

### Frontend
Create `.env` file in frontend/ directory:
```
REACT_APP_API_URL=http://localhost:5000/api
```

## Production Environment

### Backend
```
FLASK_ENV=production
API_PORT=8080
ENABLE_LOGGING=true
```

### Frontend
```
REACT_APP_API_URL=https://your-api-domain.com/api
```

## Required Dependencies

### Python 3.8+
- Flask 2.3.2
- Flask-CORS 4.0.0
- TextBlob 0.17.1
- NLTK 3.8.1
- python-dotenv 1.0.0

### Node.js 16+
- React 18.2.0
- React-DOM 18.2.0
- Axios 1.4.0
- React-Icons 4.10.1

## Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Voice Recognition Requirements
- Requires HTTPS in production
- Microphone permissions needed
- Internet connection for speech processing

## Database Configuration (Production)
Currently uses in-memory storage. For production:
1. Firebase Firestore
2. PostgreSQL with SQLAlchemy
3. MongoDB
4. Google Cloud Datastore
