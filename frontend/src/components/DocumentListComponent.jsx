import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DocumentListComponent = () => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const response = await axios.get(
          'https://klarifai-backend-bbsr-cydgehd0hmgxcybk.centralindia-01.azurewebsites.net/api/documents/'
        );
        
        if (response.data.success) {
          setDocuments(response.data.documents);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDocuments();
  }, []);

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i];
  };

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  if (loading) return <div>Loading documents...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="document-list-container">
      <h2>Documents in Azure Blob Storage</h2>
      
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>File Name</th>
            <th>Size</th>
            <th>Uploaded At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {documents.length > 0 ? (
            documents.map((doc) => (
              <tr key={doc.id}>
                <td>{doc.title}</td>
                <td>{doc.file_name}</td>
                <td>{formatFileSize(doc.file_size)}</td>
                <td>{formatDate(doc.uploaded_at)}</td>
                <td>
                  <a 
                    href={doc.file_url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="download-link"
                  >
                    Download
                  </a>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5">No documents found</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default DocumentListComponent;