import React, { useState } from 'react';
import FileUploadComponent from './FileUploadComponent';
import DocumentListComponent from './DocumentListComponent';
import './App.css';

function App() {
  const [refreshList, setRefreshList] = useState(false);

  const handleUploadSuccess = () => {
    setRefreshList(prev => !prev);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Azure Blob Storage with Django and React</h1>
      </header>
      
      <main>
        <FileUploadComponent onUploadSuccess={handleUploadSuccess} />
        <DocumentListComponent key={refreshList} />
      </main>
    </div>
  );
}

export default App;