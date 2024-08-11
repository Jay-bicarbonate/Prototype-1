import React from 'react';
import GenerateMap from './components/MapGen';
import GetActivityGenData from './components/ActivityGen';
import RunSim from './components/RunSim';
import RoadIdInput from './components/Roadblock';
import GenerateConfigButton from './components/GenConfigFiles';
import PlotComponent from './components/plotComponent';
import RoadIDdrop from './components/RoadIDselector';
import LLMGenerator from './components/LLMvis';

function App() {
  return (
    <div className="App">
      <h1>Finale Submission</h1>
      <GenerateMap/>
      <GetActivityGenData/>
      <RunSim/>
      <PlotComponent/>
      <LLMGenerator/>
      <RoadIDdrop/>
      <RoadIdInput/>
    </div>
  );
}

export default App;