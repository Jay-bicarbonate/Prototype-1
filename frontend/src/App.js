import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import GenerateMap from './components/GenerateMap';
import GetActivityGenData from './components/GetActivityGenData';
import RunSim from './components/RunSim';
import Visualiser from './components/Visualiser';
import WhatIf from './components/WhatIf';
import RLExperiment from './components/RLExperiment';
import Sidebar from './components/Sidebar';
import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/generate-map" element={<GenerateMap />} />
            <Route path="/demographic-input" element={<GetActivityGenData />} />
            <Route path="/run-simulation" element={<RunSim />} />
            <Route path="/visualiser" element={<Visualiser />} />
            <Route path="/what-if" element={<WhatIf />} />
            <Route path="/rl-experiment" element={<RLExperiment />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
