import React, { useState, useEffect } from 'react';
import './FileUploadApp.css';

const API_BASE_URL = 'https://klarifai-backend-bbsr-cydgehd0hmgxcybk.centralindia-01.azurewebsites.net';

const FileUploadApp = ({ onUploadSuccess }) => {
  const [title, setTitle] = useState('');
  const [file, setFile] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/documents/`);
      if (!response.ok) throw new Error('Network response was not ok');
      
      const data = await response.json();
      if (data.success) {
        setDocuments(data.documents);
      } else {
        setMessage(data.message || 'Failed to load documents');
      }
    } catch (error) {
      console.error('Error fetching documents:', error);
      setMessage('Failed to fetch documents. Please try again later.');
    } finally {
      setInitialLoading(false);
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage(''); // Clear previous messages when new file is selected
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title || !file) {
      setMessage('Please provide both title and file');
      return;
    }
    
    setLoading(true);
    const formData = new FormData();
    formData.append('title', title);
    formData.append('file', file);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/upload/`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) throw new Error('Upload failed');
      
      const data = await response.json();
      if (data.success) {
        setMessage('File uploaded successfully!');
        setTitle('');
        setFile(null);
        document.getElementById('file-input').value = '';
        fetchDocuments();
        if (onUploadSuccess) onUploadSuccess();
      } else {
        setMessage(data.message || 'Upload failed. Please try again.');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setMessage('An error occurred while uploading the file');
    } finally {
      setLoading(false);
    }
  };

  if (initialLoading) {
    return <div className="loading">Loading documents...</div>;
  }

  return (
    <div className="file-upload-container">
      <h2 className="section-title">Document Management</h2>
      
      {message && (
        <div className={`message-box ${message.includes('success') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}
      
      <div className="upload-section">
        <h3 className="subsection-title">Upload New Document</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Document Title</label>
            <input
              type="text"
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter document title"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="file-input">File</label>
            <input
              id="file-input"
              type="file"
              onChange={handleFileChange}
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
      </div>
      
      <div className="documents-section">
        <h3 className="subsection-title">Uploaded Documents</h3>
        
        {documents.length === 0 ? (
          <p className="no-documents">No documents uploaded yet.</p>
        ) : (
          <div className="table-container">
            <table className="documents-table">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Uploaded At</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {documents.map((doc) => (
                  <tr key={doc.id}>
                    <td>{doc.title}</td>
                    <td>{doc.uploaded_at}</td>
                    <td>
                      <a
                        href={`${API_BASE_URL}/api/documents/${doc.id}/download/`}
                        className="download-link"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        Download
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUploadApp;