import React, { useState } from 'react';
import SearchForm from './SearchForm';
import './App.css';

const App = () => {
  const [rankedImagePaths, setRankedImagePaths] = useState([]);  // Initialize as empty array
  const [selectedImages, setSelectedImages] = useState({});
  const [youtubeLinks, setYoutubeLinks] = useState({});

  const handleSearch = async (searchParams) => {
    try {
      const response = await fetch('http://localhost:8000/text_search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchParams),
      });
      const data = await response.json();
      setRankedImagePaths(data.ranked_image_paths || []);  // Use empty array as fallback
      setSelectedImages({});
      setYoutubeLinks(data.meta_data || {});
      console.log('Ranked image paths:', data.ranked_image_paths);
      console.log('YouTube links:', data.meta_data);
    } catch (error) {
      console.error('Error fetching search results:', error);
      setRankedImagePaths([]);  // Reset to empty array on error
      setYoutubeLinks({});
    }
  };

  const handleCheckboxChange = (path) => {
    setSelectedImages(prev => ({
      ...prev,
      [path]: !prev[path]
    }));
  };

  const handleSubmit = () => {
    const selectedPaths = Object.keys(selectedImages).filter(path => selectedImages[path]);
    const csvContent = "data:text/csv;charset=utf-8," 
      + selectedPaths.join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "selected_images.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleImageClick = (path) => {
    if (youtubeLinks[path]) {
      window.open(youtubeLinks[path], '_blank');
    } else {
      console.log('No YouTube link available for this image');
    }
  };

  const getDisplayPath = (path) => {
    const parts = path.split('/');
    return parts.slice(-3).join('/');
  };

  return (
    <div className="container">
      <h1 className="title">Image Search</h1>
      <SearchForm onSearch={handleSearch} />
      <button 
        onClick={handleSubmit} 
        disabled={!Object.values(selectedImages).some(Boolean)}
        className="submit-button"
      >
        Submit Selected Images
      </button>
      {rankedImagePaths.length > 0 ? (
        <div className="image-grid">
          {rankedImagePaths.map((path, index) => (
            <div key={index} className="image-container">
              <input
                type="checkbox"
                checked={selectedImages[path] || false}
                onChange={() => handleCheckboxChange(path)}
                className="image-checkbox"
              />
              <img 
                src={path} 
                alt={`Ranked ${index}`} 
                className="image"
                onClick={() => handleImageClick(path)}
                style={{ cursor: 'pointer' }}
              />
              <div className="image-path">{getDisplayPath(path)}</div>
            </div>
          ))}
        </div>
      ) : (
        <p>No images to display. Please perform a search.</p>
      )}
    </div>
  );
};

export default App;