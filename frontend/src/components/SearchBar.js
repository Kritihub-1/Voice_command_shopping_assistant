import React, { useState } from 'react';
import { FaSearch } from 'react-icons/fa';
import '../styles/SearchBar.css';

const SearchBar = ({ onSearch, loading }) => {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      onSearch(searchQuery);
      setSearchQuery('');
    }
  };

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Type items (e.g., 'Add 2 bottles of milk')"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        disabled={loading}
      />
      <button 
        type="submit"
        disabled={loading || !searchQuery.trim()}
        title="Search"
      >
        <FaSearch />
      </button>
    </form>
  );
};

export default SearchBar;
