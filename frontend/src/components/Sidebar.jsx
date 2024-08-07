import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Sidebar.css'; // Ensure this path is correct

function Sidebar() {
  return (
    <nav className="sidebar">
      <ul>
        <li><Link to="/map">Generate Map</Link></li>
        <li><Link to="/demographics">Demographic Input</Link></li>
        <li><Link to="/run-simulation">Run Simulation</Link></li>
        <li><Link to="/visualizer">Visualizer</Link></li>
        <li><Link to="/whatif">What-If</Link></li>
        <li><Link to="/rlexperiment">Reinforcement Learning</Link></li>
      </ul>
    </nav>
  );
}

export default Sidebar;
