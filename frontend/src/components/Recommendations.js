import React, { useState } from 'react';
import { FaLightbulb, FaChevronDown, FaChevronUp } from 'react-icons/fa';
import '../styles/Recommendations.css';

const Recommendations = ({ recommendations }) => {
  const [expanded, setExpanded] = useState(null);

  const getIcon = (type) => {
    switch (type) {
      case 'frequently_together':
        return '🤝';
      case 'seasonal':
        return '🌱';
      case 'restock':
        return '⏰';
      default:
        return '💡';
    }
  };

  if (recommendations.length === 0) {
    return (
      <div className="recommendations empty">
        <div className="empty-state">
          <FaLightbulb size={48} />
          <h2>No Recommendations Yet</h2>
          <p>Add items to your list to get personalized suggestions!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="recommendations">
      <h2>Smart Suggestions 💡</h2>
      <div className="recommendations-list">
        {recommendations.map((rec, index) => (
          <div 
            key={index} 
            className={`recommendation-card ${expanded === index ? 'expanded' : ''}`}
          >
            <div 
              className="recommendation-header"
              onClick={() => setExpanded(expanded === index ? null : index)}
            >
              <span className="rec-icon">{getIcon(rec.type)}</span>
              <div className="rec-content">
                <h3>{rec.item}</h3>
                <p className="rec-reason">{rec.reason}</p>
              </div>
              <span className="confidence">
                {Math.round(rec.confidence * 100)}%
              </span>
              <button className="expand-btn">
                {expanded === index ? <FaChevronUp /> : <FaChevronDown />}
              </button>
            </div>
            
            {expanded === index && (
              <div className="recommendation-details">
                <p><strong>Type:</strong> {rec.type.replace('_', ' ')}</p>
                <p><strong>Confidence:</strong> {Math.round(rec.confidence * 100)}%</p>
                <button className="add-btn">
                  + Add to List
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recommendations;
