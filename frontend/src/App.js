import React from 'react';
import GenerateMap from './components/MapGen';
import GetActivityGenData from './components/ActivityGen';

function App() {
  return (
    <div className="App">
      <h1>Finale Submission</h1>
      <GenerateMap/>
      <GetActivityGenData/>
    </div>
  );
}

export default App;
