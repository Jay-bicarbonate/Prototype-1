import React, { useState } from 'react';

function PlotComponent() {
  const [plotUrl, setPlotUrl] = useState('');

  const handleCreatePlot = async () => {
    try {
      const response = await fetch('http://localhost:5000/create-plot');
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setPlotUrl(url);
    } catch (error) {
      console.error('Error creating plot:', error);
    }
  };

  return (
    <div>
      <button onClick={handleCreatePlot}>Create Plot</button>
      {plotUrl && <img src={plotUrl} alt="Generated Plot" />}
    </div>
  );
}

export default PlotComponent;
