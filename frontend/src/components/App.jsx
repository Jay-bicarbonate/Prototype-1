import React from 'react';
import Sidebar from './components/Sidebar';
import GenerateMap from './components/GenerateMap';

function App() {
  return (
    <div className="app">
      <Sidebar />
      <main className="main-content">
        <GenerateMap />
      </main>
    </div>
  );
}

export default App;
