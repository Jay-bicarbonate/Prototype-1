import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

function MapComponent() {
  const [markers, setMarkers] = useState([]);
  const [cursorPosition, setCursorPosition] = useState(null);

  const handleMapClick = (event) => {
    if (markers.length < 2) {
      setMarkers([...markers, event.latlng]);
    }
  };

  const handleMouseMove = (event) => {
    setCursorPosition(event.latlng);
  };

  return (
    <div className="map-container">
      <MapContainer
        center={[20.5937, 78.9629]} // Default center (India)
        zoom={5}
        style={{ height: '400px', width: '100%' }}
        onClick={handleMapClick}
        onMousemove={handleMouseMove}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {markers.map((position, idx) => (
          <Marker key={idx} position={position}>
            <Popup>
              Marker {idx + 1}: {position.lat.toFixed(4)}, {position.lng.toFixed(4)}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
      <div className="coordinates">
        {cursorPosition && `Latitude: ${cursorPosition.lat}, Longitude: ${cursorPosition.lng}`}
      </div>
    </div>
  );
}

export default MapComponent;
