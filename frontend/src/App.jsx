import React from 'react';
import FileUploadApp from './components/FileUploadApp';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Azure Blob Storage with Django and React</h1>
      </header>
      <main>
        <FileUploadApp />
      </main>
    </div>
  );
}

export default App;