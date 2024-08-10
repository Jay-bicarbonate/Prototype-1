import React, { useState, useEffect } from 'react';
import axios from 'axios';

const RoadIDdrop = () => {
  const [roadIds, setRoadIds] = useState([]);
  const [selectedRoadId, setSelectedRoadId] = useState('');
  const [imageSrc, setImageSrc] = useState('');

  useEffect(() => {
    const fetchRoadIds = async () => {
      try {
        const response = await axios.get('http://localhost:5000/road_ids');
        setRoadIds(response.data);
      } catch (error) {
        console.error('Error fetching road IDs:', error);
      }
    };

    fetchRoadIds();
  }, []);

  const handleRoadIdChange = async (event) => {
    const roadId = event.target.value;
    setSelectedRoadId(roadId);

    try {
      const response = await axios.post('http://localhost:5000/select_road', { road_id: roadId }, { responseType: 'blob' });
      const url = URL.createObjectURL(response.data);
      setImageSrc(url);
    } catch (error) {
      console.error('Error fetching plot image:', error);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '20px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h1>Select a Road ID</h1>
        <select
          value={selectedRoadId}
          onChange={handleRoadIdChange}
          style={{ padding: '10px', fontSize: '16px' }}
        >
          <option value="">Select a road ID</option>
          {roadIds.map((roadId) => (
            <option key={roadId} value={roadId}>
              {roadId}
            </option>
          ))}
        </select>
      </div>
      {imageSrc && (
        <div style={{ maxWidth: '100%', textAlign: 'center' }}>
          <img
            src={imageSrc}
            alt="Highlighted Roads"
            style={{ maxWidth: '100%', height: 'auto', border: '1px solid #ddd', borderRadius: '4px' }}
          />
        </div>
      )}
    </div>
  );
};

export default RoadIDdrop;
