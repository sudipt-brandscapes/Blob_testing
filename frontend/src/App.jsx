import React from 'react';
import FileUploadApp from './components/FileUploadApp';
import './App.css';
 
function App() {
  return (
<div className="app">
<nav className="navbar">
<div className="navbar-container">
<h1 className="app-title">Document Manager</h1>
</div>
</nav>
<main className="main-content">
<div className="container">
<FileUploadApp />
</div>
</main>
<footer className="footer">
<div className="container">
<p className="copyright">
&copy; {new Date().getFullYear()} Document Management System
</p>
</div>
</footer>
</div>
  );
}
 
export default App;