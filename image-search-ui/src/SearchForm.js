import React, { useState } from 'react';
import './SearchForm.css';

const SearchForm = ({ onSearch }) => {
  const [textQuery, setTextQuery] = useState('');
  const [k, setK] = useState(10);
  const [modelType, setModelType] = useState('CLIP V2');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch({ text: textQuery, k, model_type: modelType });
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="search-form">
      <div className="form-group">
        <label htmlFor="textQuery">Text Query:</label>
        <textarea
          id="textQuery"
          value={textQuery}
          onChange={(e) => setTextQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          required
          rows="6"
          placeholder="Enter your text query here (up to 200 words)"
          maxLength="1000"
        />
      </div>
      <div className="form-row">
        <div className="form-group">
          <label htmlFor="k">K:</label>
          <input
            type="number"
            id="k"
            value={k}
            onChange={(e) => setK(parseInt(e.target.value))}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="modelType">Model Type:</label>
          <select
            id="modelType"
            value={modelType}
            onChange={(e) => setModelType(e.target.value)}
          >
            <option value="CLIP V2">CLIP V2</option>
            <option value="Other Model">Other Model</option>
          </select>
        </div>
      </div>
      <button type="submit" className="search-button">Search</button>
    </form>
  );
};

export default SearchForm;