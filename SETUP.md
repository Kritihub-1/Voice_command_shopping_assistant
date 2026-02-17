# Setup & Installation Guide

## Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- Git

## Local Development Setup

### 1. Clone Repository
```bash
cd c:\Users\HP\Desktop\coding\voice-shopping-assistant
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (for NLP)
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

# Start development server
python run.py
```

Backend will be available at `http://localhost:5000`

### 3. Frontend Setup (in new terminal)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will open at `http://localhost:3000`

## Running with Docker

### Prerequisites
- Docker installed
- Docker Compose installed

### Start Both Services
```bash
# From project root
docker-compose up
```

- Backend: `http://localhost:5000`
- Frontend: `http://localhost:3000`

## Testing the Application

### 1. Test Voice Input
1. Open http://localhost:3000
2. Click the microphone button
3. Say commands like:
   - "Add milk"
   - "I need bread and eggs"
   - "Remove apples"

### 2. Test Text Search
1. Type in search box: "Add 2 bottles of water"
2. Press Enter or click search button

### 3. Test Recommendations
1. Add several items
2. Click "Recommendations" tab
3. See suggestions based on items

### 4. Test API Directly
```bash
# Add item
curl -X POST http://localhost:5000/api/shopping/add \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","command":"Add milk"}'

# Get shopping list
curl http://localhost:5000/api/shopping/list?user_id=test

# Get recommendations
curl http://localhost:5000/api/recommendations/personalized \
  -G --data-urlencode "user_id=test" \
  --data-urlencode "items=milk"
```

## Troubleshooting

### Flask Server Won't Start
```bash
# Check if port 5000 is in use
# Windows:
netstat -ano | findstr :5000
# Kill process: taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
# Kill process: kill -9 <PID>
```

### React App Won't Start
```bash
# Clear node modules and reinstall
rm -rf frontend/node_modules
npm install
npm start
```

### Speech Recognition Not Working
- Ensure you're using HTTPS (required for production)
- Check browser microphone permissions
- Try a different browser (Chrome works best)

### CORS Errors
- Ensure backend is running on port 5000
- Ensure frontend is pointing to correct API URL

## Development Workflow

### Adding a New Feature

1. **Create backend endpoint**
   - Add method to service in `backend/app/services/`
   - Create route in `backend/app/routes/`

2. **Create frontend component**
   - Add component in `frontend/src/components/`
   - Add styling in `frontend/src/styles/`
   - Integrate in main App.js

3. **Test thoroughly**
   - Manual testing in browser
   - API testing with curl

4. **Commit changes**
   ```bash
   git add .
   git commit -m "Add new feature"
   git push
   ```

## Environment Variables

Create `.env` files:

### Backend (.env in backend/)
```
FLASK_ENV=development
FLASK_DEBUG=1
API_PORT=5000
```

### Frontend (.env in frontend/)
```
REACT_APP_API_URL=http://localhost:5000/api
```

## Project Structure

```
voice-shopping-assistant/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── services/
│   │   └── routes/
│   ├── requirements.txt
│   ├── run.py
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── styles/
│   │   └── App.js
│   ├── package.json
│   └── .env
├── docker-compose.yml
└── README.md
```

## Next Steps

1. ✅ Set up local development environment
2. ✅ Test basic functionality
3. [] Deploy to cloud platform
4. [] Set up database
5. [] Add user authentication
6. [] Implement advanced features

## Getting Help

Check the README.md for API documentation and feature details.
