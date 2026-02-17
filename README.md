# Voice Command Shopping Assistant
## Tech Stack

### Backend
- **Framework**: Flask (Python)
- **NLP**: TextBlob, NLTK
- **Voice Processing**: Google Speech Recognition
- **Architecture**: RESTful API with microservices-ready design

### Frontend
- **Framework**: React 18
- **Styling**: CSS3 with responsive design
- **Voice**: Web Speech API
- **HTTP Client**: Axios

### Deployment
- **Backend**: Google Cloud Run (serverless)
- **Frontend**: Firebase Hosting or Vercel
- **Database**: Firebase/Cloud Firestore (production)

## API Endpoints

### Shopping List
- `GET /api/shopping/list` - Get user's shopping list
- `POST /api/shopping/add` - Add items via voice command
- `POST /api/shopping/remove` - Remove item
- `POST /api/shopping/clear` - Clear all items
- `GET /api/shopping/category/<category>` - Get items by category

### Voice Processing
- `POST /api/voice/process-command` - Process voice command
- `POST /api/voice/extract-items` - Extract items from text
- `GET /api/voice/supported-languages` - Get supported languages

### Recommendations
- `GET /api/recommendations/personalized` - Get personalized recommendations
- `POST /api/recommendations/alternatives` - Get alternative products
- `GET /api/recommendations/price-range` - Get price data
- `GET /api/recommendations/seasonal` - Get seasonal suggestions

## NLP Engine Features

The NLP processor handles:
- **Intent Recognition**: ADD, REMOVE, SEARCH, LIST commands
- **Entity Extraction**: Item names, quantities, units
- **Categorization**: Automatic category assignment (20+ categories)
- **Alternative Suggestions**: Product substitutes and recommendations

## Recommendations Engine

Smart features:
- Frequently Bought Together (2-hop association)
- Seasonal items (4 seasons)
- Restock frequency tracking
- Price range estimation
- User history tracking

## Development

### Adding a New Feature

1. **Backend**: Add method to service class
2. **Route**: Create endpoint in routes/
3. **Frontend**: Add component or page
4. **Test**: Add unit tests

### Project Development Checklist
- [x] Backend API structure
- [x] NLP processing
- [x] Recommendation engine
- [x] Frontend React app
- [x] Voice input integration
- [x] Shopping list UI
- [ ] Database integration
- [ ] User authentication
- [ ] Deployment configuration
- [ ] Comprehensive testing

## Error Handling

The app includes:
- Graceful speech recognition fallback
- Command parsing error handling
- Loading states and user feedback
- Input validation

## Performance Optimization

- API response caching
- Voice recognition debouncing
- Recommendation caching
- Lazy loading of components

## Production Deployment

### Backend (Google Cloud Run)
```bash
gcloud run deploy voice-shopping-api \
  --source . \
  --platform managed \
  --region us-central1
```

### Frontend (Firebase Hosting)
```bash
npm run build
firebase deploy
```

## Environment Variables

Backend (.env):
```
FLASK_ENV=production
API_PORT=5000
GOOGLE_SPEECH_API_KEY=<your-key>
```

Frontend (.env):
```
REACT_APP_API_URL=https://api.example.com
```

## Testing

```bash
# Backend
python -m pytest tests/

# Frontend
npm test
```
