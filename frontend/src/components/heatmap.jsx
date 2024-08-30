import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import chroma from 'chroma-js';
// import './heatmap.css';

const MapViewHeat = () => {
  const [geojsonData, setGeojsonData] = useState(null);
  const [densityData, setDensityData] = useState(null);
  const [lowerBound, setLowerBound] = useState(0);
  const [upperBound, setUpperBound] = useState(1);

  useEffect(() => {
    // Fetch GeoJSON data
    fetch('/map.geojson')
      .then(response => response.json())
      .then(data => setGeojsonData(data))
      .catch(error => console.error('Error fetching the GeoJSON file:', error));

    // Fetch density data from Flask API
    fetch('http://localhost:5000/get-density-data')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response
      })
      .then(data => {
        setDensityData(data);

        // Calculate percentiles for normalization
        const densities = Object.values(data);
        densities.sort((a, b) => a - b); // Sort the density values

        const lowerPercentileIndex = Math.floor(densities.length * 0.05); // 3rd percentile
        const upperPercentileIndex = Math.ceil(densities.length * 0.95) - 1; // 96th percentile

        setLowerBound(densities[lowerPercentileIndex]);
        setUpperBound(densities[upperPercentileIndex]);
      })
      .catch(error => {
        console.error('Error fetching the density data:', error);
      });
  }, []);

  const getColor = (density) => {
    if (density === undefined) return '#000000'; // No vehicle, use black color or any other fallback color

    // Clamp density values between the lower and upper bounds
    const clampedDensity = Math.max(lowerBound, Math.min(density, upperBound));
    const normalizedDensity = (clampedDensity - lowerBound) / (upperBound - lowerBound);

    return chroma.scale(['blue', 'red'])(normalizedDensity).hex();
  };

  const style = (feature) => {
    const roadId = feature.properties.id;
    const density = densityData ? densityData[roadId] : undefined;
    return {
      color: getColor(density),
      weight: 5,
      opacity: 0.8,
    };
  };

  const onEachFeature = (feature, layer) => {
    const roadId = feature.properties.id;
    const density = densityData ? densityData[roadId] : 'No Data';

    if (densityData) {
      layer.bindTooltip(`Road ID: ${roadId}<br>Density: ${density}`);
    }
  };

  // // Function to create a legend
  // const Legend = () => {
  //   const legendColors = chroma.scale(['blue', 'red']).colors(5); // 5 color steps
  //   const legendSteps = [
  //     lowerBound, 
  //     lowerBound + (upperBound - lowerBound) * 0.25, 
  //     lowerBound + (upperBound - lowerBound) * 0.5, 
  //     lowerBound + (upperBound - lowerBound) * 0.75, 
  //     upperBound
  //   ];

  //   return (
  //     <div className="legend">
  //       <h4>Density Legend</h4>
  //       {legendSteps.map((step, index) => (
  //         <div key={index}>
  //           <span style={{ background: legendColors[index], width: '30px', height: '10px', display: 'inline-block', marginRight: '10px' }}></span>
  //           {Math.round(step)}
  //         </div>
  //       ))}
  //     </div>
  //   );
  // };

  return (
    <div style={{ position: 'relative' }}>
      <MapContainer
        style={{ height: "600px", width: "100%" }}
        center={[22.722624, 75.889484]}
        zoom={13}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        {geojsonData && densityData && (
          <GeoJSON data={geojsonData} style={style} onEachFeature={onEachFeature} />
        )}
      </MapContainer>
    </div>
  );
};

export default MapViewHeat;
