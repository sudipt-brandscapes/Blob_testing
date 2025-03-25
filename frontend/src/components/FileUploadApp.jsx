import React, { useState } from 'react';
import axios from 'axios';

const FileUploadComponent = ({ onUploadSuccess }) => {
  const [title, setTitle] = useState('');
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!title || !file) {
      setError('Title and file are required');
      return;
    }

    setIsUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('title', title);
    formData.append('file', file);

    try {
      const response = await axios.post(
        'https://klarifai-backend-bbsr-cydgehd0hmgxcybk.centralindia-01.azurewebsites.net/api/documents/upload/',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      if (response.data.success) {
        onUploadSuccess(response.data.document);
        setTitle('');
        setFile(null);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to upload file');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="file-upload-container">
      <h2>Upload Document to Azure Blob Storage</h2>
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title:</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="file">File:</label>
          <input
            type="file"
            id="file"
            onChange={(e) => setFile(e.target.files[0])}
            required
          />
        </div>
        
        <button type="submit" disabled={isUploading}>
          {isUploading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
    </div>
  );
};

export default FileUploadComponent;