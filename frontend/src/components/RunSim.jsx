// components/RunSim.jsx
import React from 'react';

class RunSim extends React.Component {
  runSimulation = async () => {
    try {
      const response = await fetch('http://localhost:5000/run-simulation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log(data); // Handle the response from the backend
    } catch (error) {
      console.error('There was an error running the simulation!', error);
    }
  };

  render() {
    return (
      <button onClick={this.runSimulation}>
        Run Simulation
      </button>
    );
  }
}

export default RunSim;
