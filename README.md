# Voice Command Shopping Assistant

A modern, production-ready voice-based shopping list manager with smart AI-powered recommendations.

## Features

### 1. Voice Input & Commands ✨
- **Voice Recognition**: Google Speech-to-Text integration for accurate voice input
- **Natural Language Processing**: Understands various phrases (e.g., "Add milk", "I need bread", "Remove apples")
- **Multilingual Support**: English, Spanish, French, German, Hindi
- **Real-time Feedback**: Live transcript display and listening indicators

### 2. Smart Shopping List Management 📋
- **Add/Remove/Clear items** using voice or text
- **Automatic Categorization**: Items organized by category (dairy, produce, meat, etc.)
- **Quantity Management**: Specify quantities and units ("2 bottles of milk", "5 apples")
- **Price Estimation**: Basic price tracking and total calculation

### 3. Intelligent Recommendations 💡
- **Frequently Bought Together**: Suggests complementary items
- **Seasonal Recommendations**: Contextual suggestions based on season
- **Restock Alerts**: Reminds when it's time to rebuy frequently used items
- **Product Substitutes**: Alternative options for unavailable items

### 4. Modern UI/UX 🎨
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Voice-First Interface**: Optimized for voice interactions
- **Visual Feedback**: Real-time updates and loading states
- **Tabbed Navigation**: Switch between list and recommendations

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

## Project Structure

```
voice-shopping-assistant/
├── backend/                    # Python Flask API
│   ├── app/
│   │   ├── models/            # Data models
│   │   ├── services/          # Business logic
│   │   │   ├── nlp_processor.py      # NLP & command processing
│   │   │   ├── recommendation_engine.py  # Smart recommendations
│   │   │   └── voice_processor.py    # Voice input handling
│   │   └── routes/            # API endpoints
│   ├── requirements.txt        # Python dependencies
│   └── run.py                 # Start server
│
├── frontend/                   # React web app
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   ├── styles/           # CSS files
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
│
├── docker/                     # Docker configurations
├── deployment/                 # Cloud deployment configs
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python run.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`

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

## Usage Examples

### Voice Commands
```
"Add milk"
"I need 2 bottles of water"
"Remove apples from my list"
"Show me my shopping list"
"Find alternative for bread"
```

### API Examples

Add items via voice:
```bash
curl -X POST http://localhost:5000/api/shopping/add \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "command": "Add milk and bread"
  }'
```

Get personalized recommendations:
```bash
curl http://localhost:5000/api/recommendations/personalized \
  -G --data-urlencode "user_id=user123" \
  --data-urlencode "items=milk" \
  --data-urlencode "items=bread"
```

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

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing`
5. Open Pull Request

## Future Enhancements

- [ ] Social sharing of lists
- [ ] Multi-user collaboration
- [ ] Integration with e-commerce platforms
- [ ] Advanced ML-based recommendations
- [ ] Barcode scanning
- [ ] Real-time price comparison
- [ ] Store location integration
- [ ] Budget tracking and analytics
- [ ] Community recipe suggestions
- [ ] Allergy/dietary restriction filtering

## License

MIT License - feel free to use this project for your own purposes.

## Support

For issues, feature requests, or questions: [Create an issue](https://github.com/yourusername/voice-shopping-assistant/issues)

---

**Built with ❤️ for smarter shopping**
