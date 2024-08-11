import React, { useState } from 'react';

function LLMGenerator() {
  const [plotUrl, setPlotUrl] = useState('');
  const [plotData, setPlotData] = useState(null);
  const [inputText, setInputText] = useState('');

  const handleCreatePlot = async () => {
    try {
      const response = await fetch('http://localhost:5000/generate-image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });
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
      <h2>Visualisation</h2>
      <input
        type="text"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Enter text for plot"
      />
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

export default LLMGenerator;
