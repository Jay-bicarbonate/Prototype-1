import React from 'react';
import GenerateMap from './components/MapGen';
import GetActivityGenData from './components/ActivityGen';
import RunSim from './components/RunSim';

function App() {
  return (
    <div className="App">
      <h1>Finale Submission</h1>
      <GenerateMap/>
      <GetActivityGenData/>
      <RunSim/>
    </div>
  );
}

export default App;
