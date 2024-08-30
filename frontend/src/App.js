import React, { useState } from 'react';
import './App.css';

import GenerateMap from './components/MapGen';
import RunSim from './components/RunSim';
import MapViewHeat from './components/heatmap';
import MapView from './components/OSMinteractive';

function App() {
  const [selectedPage, setSelectedPage] = useState('GenerateMap');

  const renderComponent = () => {
    switch (selectedPage) {
      case 'GenerateMap':
        return <GenerateMap />;
      case 'RunSim':
        return <RunSim />;
      case 'RoadIdInput':
        return <MapView/>;
      case 'Visulaisation':
        return <MapViewHeat/>;
    }
  };

  return (
    <div className="App" style={{ display: 'flex' }}>
      <div className="Sidebar" style={{ width: '200px', marginRight: '20px' }}>
        <button onClick={() => setSelectedPage('GenerateMap')}>Generate Map</button>
        <button onClick={() => setSelectedPage('RunSim')}>Run Simulation</button>
        <button onClick={() => setSelectedPage('Visulaisation')}>Visulaisation</button>
        <button onClick={() => setSelectedPage('RoadIdInput')}>Block Road</button>
      </div>
      <div className="Content" style={{ flexGrow: 1 }}>
        <h1>Finale Submission</h1>
        {renderComponent()}
      </div>
    </div>
  );
}

export default App;