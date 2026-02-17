import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './styles/App.css';
import VoiceInput from './components/VoiceInput';
import ShoppingList from './components/ShoppingList';
import Recommendations from './components/Recommendations';
import SearchBar from './components/SearchBar';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [shoppingList, setShoppingList] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [userId] = useState('default_user');
  const [activeTab, setActiveTab] = useState('list');

  useEffect(() => {
    fetchShoppingList();
    fetchRecommendations();
  }, []);

  const fetchShoppingList = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/shopping/list`, {
        params: { user_id: userId }
      });
      setShoppingList(response.data.items || []);
      setError('');
    } catch (err) {
      setError('Failed to fetch shopping list');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchRecommendations = async () => {
    try {
      const items = shoppingList.map(item => item.name);
      const response = await axios.get(`${API_BASE_URL}/recommendations/personalized`, {
        params: {
          user_id: userId,
          items: items
        }
      });
      setRecommendations(response.data.recommendations || []);
    } catch (err) {
      console.error('Failed to fetch recommendations:', err);
    }
  };

  const handleVoiceCommand = async (command) => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE_URL}/shopping/add`, {
        user_id: userId,
        command: command
      });
      
      if (response.data.success) {
        setShoppingList(response.data.shopping_list.items);
        setError('');
        // Refresh recommendations
        await fetchRecommendations();
      }
    } catch (err) {
      setError('Failed to process command');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveItem = async (itemId) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/shopping/remove`, {
        user_id: userId,
        item_id: itemId
      });
      
      if (response.data.success) {
        setShoppingList(response.data.shopping_list.items);
        await fetchRecommendations();
      }
    } catch (err) {
      setError('Failed to remove item');
      console.error(err);
    }
  };

  const handleClearList = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/shopping/clear`, {
        user_id: userId
      });
      
      if (response.data.success) {
        setShoppingList([]);
        setRecommendations([]);
      }
    } catch (err) {
      setError('Failed to clear list');
      console.error(err);
    }
  };

  const handleSearch = async (query) => {
    await handleVoiceCommand(query);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🛒 Voice Shopping Assistant</h1>
        <p>Add items using voice commands or text search</p>
      </header>

      {error && <div className="error-message">{error}</div>}

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'list' ? 'active' : ''}`}
          onClick={() => setActiveTab('list')}
        >
          Shopping List ({shoppingList.length})
        </button>
        <button 
          className={`tab ${activeTab === 'recommendations' ? 'active' : ''}`}
          onClick={() => setActiveTab('recommendations')}
        >
          Recommendations ({recommendations.length})
        </button>
      </div>

      <div className="main-content">
        <div className="input-section">
          <VoiceInput 
            onCommand={handleVoiceCommand}
            loading={loading}
          />
          <SearchBar 
            onSearch={handleSearch}
            loading={loading}
          />
        </div>

        {activeTab === 'list' && (
          <ShoppingList
            items={shoppingList}
            onRemoveItem={handleRemoveItem}
            onClearList={handleClearList}
            loading={loading}
          />
        )}

        {activeTab === 'recommendations' && (
          <Recommendations
            recommendations={recommendations}
          />
        )}
      </div>
    </div>
  );
}

export default App;
