import React, { useState, useEffect } from 'react';
import './FileUploadApp.css';

const FileUploadApp = () => {
  const [title, setTitle] = useState('');
  const [file, setFile] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' }); // type: 'success' | 'error'
  const [retryCount, setRetryCount] = useState(0);

  const API_BASE_URL = 'https://klarifai-backend-bbsr-cydgehd0hmgxcybk.centralindia-01.azurewebsites.net';

  useEffect(() => {
    fetchDocuments();
  }, [retryCount]);

  const showMessage = (text, type = 'error') => {
    setMessage({ text, type });
    setTimeout(() => setMessage({ text: '', type: '' }), 5000);
  };

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/api/documents/`, {
        headers: {
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        throw new Error(`Expected JSON but got: ${text.substring(0, 100)}...`);
      }

      const data = await response.json();
      
      if (data.success) {
        setDocuments(data.documents);
      } else {
        throw new Error(data.message || 'Failed to fetch documents');
      }
    } catch (error) {
      console.error('Error fetching documents:', error);
      showMessage(`Failed to load documents: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    
    // Basic client-side validation
    if (selectedFile) {
      const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
      const maxSize = 10 * 1024 * 1024; // 10MB
      
      if (!validTypes.includes(selectedFile.type)) {
        showMessage('Invalid file type. Please upload PDF, DOC, DOCX, or TXT files.');
        e.target.value = ''; // Reset file input
        return;
      }
      
      if (selectedFile.size > maxSize) {
        showMessage('File size exceeds 10MB limit.');
        e.target.value = ''; // Reset file input
        return;
      }
      
      setFile(selectedFile);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!title.trim()) {
      showMessage('Please provide a document title');
      return;
    }
    
    if (!file) {
      showMessage('Please select a file to upload');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('title', title.trim());
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE_URL}/api/upload/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        throw new Error(`Expected JSON but got: ${text.substring(0, 100)}...`);
      }

      const data = await response.json();
      
      if (data.success) {
        showMessage('File uploaded successfully!', 'success');
        setTitle('');
        setFile(null);
        document.getElementById('file-input').value = '';
        await fetchDocuments();
      } else {
        throw new Error(data.message || 'Upload failed');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      showMessage(`Upload failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = () => {
    setRetryCount(prev => prev + 1);
  };

  return (
    <div className="file-upload-container">
      <h2 className="section-title">Document Management</h2>
      
      {/* Status Message */}
      {message.text && (
        <div className={`message-box ${message.type === 'success' ? 'success' : 'error'}`}>
          {message.text}
          {message.type === 'error' && (
            <button onClick={handleRetry} className="retry-button">Retry</button>
          )}
        </div>
      )}
      
      {/* Loading Overlay */}
      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <p>Processing...</p>
        </div>
      )}
      
      <div className="upload-section">
        <h3 className="subsection-title">Upload New Document</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Document Title *</label>
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
            <label htmlFor="file-input">File * (PDF, DOC, DOCX, TXT, max 10MB)</label>
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
                    <td>{new Date(doc.uploaded_at).toLocaleString()}</td>
                    <td>
                      <a
                        href={`${API_BASE_URL}/api/documents/${doc.id}/download/`}
                        className="download-link"
                        target="_blank"
                        rel="noopener noreferrer"
                        download
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