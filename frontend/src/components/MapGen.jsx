import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import 'leaflet-draw';

const GenerateMap = () => {
  const mapRef = useRef(null);
  const drawnItemsRef = useRef(null);
  const [vehicleTrips, setVehicleTrips] = useState('');

  useEffect(() => {
    // Initialize map
    const map = L.map(mapRef.current).setView([20.5937, 78.9629], 5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Initialize FeatureGroup for drawn items
    const drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);
    drawnItemsRef.current = drawnItems;

    // Initialize draw control
    const drawControl = new L.Control.Draw({
      edit: {
        featureGroup: drawnItems
      },
      draw: {
        polygon: false,
        polyline: false,
        circle: false,
        marker: false,
        circlemarker: false
      }
    });
    map.addControl(drawControl);

    // Event listener for draw:created
    map.on(L.Draw.Event.CREATED, (e) => {
      const layer = e.layer;
      drawnItems.clearLayers();
      drawnItems.addLayer(layer);
    });

    return () => {
      map.remove();
    };
  }, []);

  const handleReset = () => {
    if (drawnItemsRef.current) {
      drawnItemsRef.current.clearLayers();
    }
  };

  const handleConfirm = async () => {
    if (drawnItemsRef.current && drawnItemsRef.current.getLayers().length > 0) {
      const bounds = drawnItemsRef.current.getBounds();
      const data = {
        north: bounds.getNorth(),
        south: bounds.getSouth(),
        east: bounds.getEast(),
        west: bounds.getWest(),
        trips: vehicleTrips // Include vehicle trips in the data
      };

      console.log('Sending data:', data);

      try {
        const response = await fetch('http://localhost:5000/generatemap', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const result = await response.json();
        console.log('Response:', result);
      } catch (error) {
        console.error('Error:', error);
      }
    } else {
      console.log('No area selected');
    }
  };

  return (
    <div>
      <div ref={mapRef} style={{ height: '400px' }}></div>
      <div>
        <label htmlFor="vehicleTrips">Vehicle Trips: </label>
        <input
          type="text"
          id="vehicleTrips"
          value={vehicleTrips}
          onChange={(e) => setVehicleTrips(e.target.value)}
        />
      </div>
      <button onClick={handleReset}>Reset</button>
      <button onClick={handleConfirm}>Confirm</button>
    </div>
  );
};

export default GenerateMap;
