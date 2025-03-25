import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FileUploadApp.css';

const FileUploadApp = () => {
  const [title, setTitle] = useState('');
  const [file, setFile] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Configure base URL and axios instance
  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'https://klarifai-backend-bbsr-cydgehd0hmgxcybk.centralindia-01.azurewebsites.net';
  const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,  // 10 seconds timeout
    headers: {
      'Content-Type': 'multipart/form-data',
      'Accept': 'application/json',
    },
  });

  // Fetch documents on component mount
  useEffect(() => {
    fetchDocuments();
  }, []);

  // Fetch documents from backend
  const fetchDocuments = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axiosInstance.get('/api/documents/');
      
      if (response.data.success) {
        setDocuments(response.data.documents);
      } else {
        throw new Error(response.data.message || 'Failed to fetch documents');
      }
    } catch (err) {
      console.error('Document fetch error:', err);
      setError(err.message || 'Unable to fetch documents');
    } finally {
      setLoading(false);
    }
  };

  // File validation
  const validateFile = (file) => {
    const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    const maxSize = 10 * 1024 * 1024; // 10MB

    if (!allowedTypes.includes(file.type)) {
      throw new Error('Invalid file type. Please upload PDF, DOC, DOCX, or TXT files.');
    }

    if (file.size > maxSize) {
      throw new Error('File size must be under 10MB');
    }
  };

  // Handle file selection
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    
    try {
      if (selectedFile) {
        validateFile(selectedFile);
        setFile(selectedFile);
        setError(null);
      }
    } catch (err) {
      setError(err.message);
      e.target.value = null;
    }
  };

  // Submit file upload
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Please provide a document title');
      return;
    }

    if (!file) {
      setError('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('title', title.trim());
    formData.append('file', file);

    try {
      setLoading(true);
      setError(null);

      const response = await axiosInstance.post('/api/upload/', formData);

      if (response.data.success) {
        // Reset form and refresh documents
        setTitle('');
        setFile(null);
        document.getElementById('file-input').value = null;
        
        // Fetch updated document list
        await fetchDocuments();
        
        alert('File uploaded successfully!');
      } else {
        throw new Error(response.data.message || 'Upload failed');
      }
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.message || 'Unable to upload file');
    } finally {
      setLoading(false);
    }
  };

  // Download document
  const handleDownload = (fileUrl) => {
    window.open(fileUrl, '_blank');
  };

  return (
    <div className="file-upload-container">
      <h2>Document Upload Management</h2>

      {/* Error Display */}
      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      {/* Upload Form */}
      <form onSubmit={handleSubmit} className="upload-form">
        <div className="form-group">
          <label>Document Title</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter document title"
            required
          />
        </div>

        <div className="form-group">
          <label>File Upload (PDF, DOC, DOCX, TXT)</label>
          <input
            id="file-input"
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.doc,.docx,.txt"
            required
          />
        </div>

        <button 
          type="submit" 
          disabled={loading}
          className="submit-button"
        >
          {loading ? 'Uploading...' : 'Upload Document'}
        </button>
      </form>

      {/* Documents List */}
      <div className="documents-list">
        <h3>Uploaded Documents</h3>
        {loading ? (
          <p>Loading documents...</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Uploaded At</th>
                <th>File Size</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {documents.map((doc) => (
                <tr key={doc.id}>
                  <td>{doc.title}</td>
                  <td>{new Date(doc.uploaded_at).toLocaleString()}</td>
                  <td>{(doc.file_size / 1024 / 1024).toFixed(2)} MB</td>
                  <td>
                    <button 
                      onClick={() => handleDownload(doc.file_url)}
                      className="download-button"
                    >
                      Download
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default FileUploadApp;