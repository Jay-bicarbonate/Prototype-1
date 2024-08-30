import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const MapView = () => {
  const [geojsonData, setGeojsonData] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('/map.geojson')
      .then(response => response.json())
      .then(data => setGeojsonData(data))
      .catch(error => console.error('Error fetching the GeoJSON file:', error));
  }, []);

  const onEachFeature = (feature, layer) => {
    if (feature.properties && feature.properties.id) {
      layer.on({
        click: () => {
          const roadId = feature.properties.id;
          setSelectedId(roadId);
          updateRoad(roadId);
        }
      });
    }
  };

  const updateRoad = async (roadId) => {
    try {
      const response = await fetch('http://localhost:5000/update-road', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ roadId }),
      });
      const result = await response.json();
      
      if (response.ok) {
        setMessage(`Road ID ${roadId} successfully Blocked.`);
      } else {
        setMessage(`Error: ${result.error}`);
      }
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  return (
    <div>
      <MapContainer
        style={{ height: "600px", width: "100%" }}
        center={[22.722624, 75.889484]}
        zoom={13}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        {geojsonData && <GeoJSON data={geojsonData} onEachFeature={onEachFeature} />}
      </MapContainer>
      {message && (
        <div style={{ marginTop: "10px", color: "green" }}>
          {message}
        </div>
      )}
    </div>
  );
};

export default MapView;
