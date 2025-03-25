import React, { useState, useEffect } from 'react';
import './FileUploadApp.css';

const FileUploadApp = () => {
  const [title, setTitle] = useState('');
  const [file, setFile] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });
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
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        // Ensure all document URLs point to the correct Blob Storage container
        const processedDocs = data.documents.map(doc => ({
          ...doc,
          file_url: doc.file_url.replace('/media/', '/documents/') // Adjust path if needed
        }));
        setDocuments(processedDocs);
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
    
    // Enhanced client-side validation
    if (selectedFile) {
      const validTypes = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain'
      ];
      const validExtensions = ['.pdf', '.doc', '.docx', '.txt'];
      const maxSize = 10 * 1024 * 1024; // 10MB
      
      // Check both MIME type and file extension
      const fileExt = selectedFile.name.split('.').pop().toLowerCase();
      if (!validTypes.includes(selectedFile.type) || !validExtensions.includes(`.${fileExt}`)) {
        showMessage('Invalid file type. Please upload PDF, DOC, DOCX, or TXT files.');
        e.target.value = '';
        return;
      }
      
      if (selectedFile.size > maxSize) {
        showMessage('File size exceeds 10MB limit.');
        e.target.value = '';
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
        credentials: 'include',
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        showMessage('File uploaded successfully to Azure Blob Storage!', 'success');
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
      <h2 className="section-title">Azure Blob Storage Document Management</h2>
      
      {message.text && (
        <div className={`message-box ${message.type === 'success' ? 'success' : 'error'}`}>
          {message.text}
          {message.type === 'error' && (
            <button onClick={handleRetry} className="retry-button">Retry</button>
          )}
        </div>
      )}
      
      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <p>Connecting to Azure Blob Storage...</p>
        </div>
      )}
      
      <div className="upload-section">
        <h3 className="subsection-title">Upload to Azure Blob Storage</h3>
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
            {loading ? 'Uploading to Azure...' : 'Upload to Blob Storage'}
          </button>
        </form>
      </div>
      
      <div className="documents-section">
        <h3 className="subsection-title">Documents in Azure Container</h3>
        {documents.length === 0 ? (
          <p className="no-documents">No documents found in the 'documents' container.</p>
        ) : (
          <div className="table-container">
            <table className="documents-table">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Uploaded At</th>
                  <th>File Size</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {documents.map((doc) => (
                  <tr key={doc.id}>
                    <td>{doc.title}</td>
                    <td>{new Date(doc.uploaded_at).toLocaleString()}</td>
                    <td>{(doc.file_size / (1024 * 1024)).toFixed(2)} MB</td>
                    <td>
                      <a
                        href={`${doc.file_url}${doc.file_url.includes('?') ? '&' : '?'}download=true`}
                        className="download-link"
                        target="_blank"
                        rel="noopener noreferrer"
                        download
                      >
                        Download from Azure
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