import React from 'react';
import { FaTrash } from 'react-icons/fa';
import '../styles/ShoppingList.css';

const ShoppingList = ({ items, onRemoveItem, onClearList, loading }) => {
  const calculateTotal = () => {
    return items.reduce((sum, item) => sum + (item.price_estimate || 0), 0).toFixed(2);
  };

  const groupByCategory = () => {
    const grouped = {};
    items.forEach(item => {
      const cat = item.category || 'uncategorized';
      if (!grouped[cat]) grouped[cat] = [];
      grouped[cat].push(item);
    });
    return grouped;
  };

  if (items.length === 0) {
    return (
      <div className="shopping-list empty">
        <div className="empty-state">
          <h2>📋 Your shopping list is empty</h2>
          <p>Use the microphone or search to add items!</p>
        </div>
      </div>
    );
  }

  const grouped = groupByCategory();

  return (
    <div className="shopping-list">
      <div className="list-header">
        <h2>Shopping List ({items.length} items)</h2>
        <button 
          className="clear-btn"
          onClick={onClearList}
          disabled={loading}
        >
          Clear All
        </button>
      </div>

      <div className="summary">
        <span className="item-count">Items: {items.length}</span>
        <span className="total-price">Estimated: ${calculateTotal()}</span>
      </div>

      {Object.entries(grouped).map(([category, categoryItems]) => (
        <div key={category} className="category-group">
          <h3 className="category-name">
            {category.charAt(0).toUpperCase() + category.slice(1)}
          </h3>
          <ul className="items">
            {categoryItems.map(item => (
              <li key={item.id} className="item">
                <div className="item-info">
                  <span className="item-name">{item.name}</span>
                  <span className="item-qty">
                    {item.quantity} {item.unit}
                  </span>
                  {item.price_estimate > 0 && (
                    <span className="item-price">${item.price_estimate.toFixed(2)}</span>
                  )}
                </div>
                <button
                  className="remove-btn"
                  onClick={() => onRemoveItem(item.id)}
                  disabled={loading}
                  title="Remove item"
                >
                  <FaTrash size={16} />
                </button>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default ShoppingList;
