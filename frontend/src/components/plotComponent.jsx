import React, { useState } from 'react';

function PlotComponent() {
  const [plotUrl, setPlotUrl] = useState('');
  const [plotData, setPlotData] = useState(null);

  const handleCreatePlot = async () => {
    try {
      const response = await fetch('http://localhost:5000/create-plot');
      const data = await response.json();
      
      // Handle the base64 image and JSON data
      const imageUrl = `data:image/png;base64,${data.image}`;
      setPlotUrl(imageUrl);
      setPlotData(data.json_data);
    } catch (error) {
      console.error('Error creating plot:', error);
    }
  };

  return (
    <div>
      <button onClick={handleCreatePlot}>Create Plot</button>
      {plotUrl && <img src={plotUrl} alt="Generated Plot" />}
      {plotData && (
        <div>
          <h2>Plot Data:</h2>
          <pre>{JSON.stringify(plotData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default PlotComponent;