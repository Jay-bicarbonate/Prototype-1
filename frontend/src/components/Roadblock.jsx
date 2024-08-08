import React, { useState } from 'react';

function RoadIdInput() {
  const [roadId, setRoadId] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:5000/update-road', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ roadId }),
      });

      if (response.ok) {
        alert('Road ID updated successfully!');
      } else {
        alert('Error updating Road ID');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error updating Road ID');
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Enter Road ID:
          <input
            type="text"
            value={roadId}
            onChange={(e) => setRoadId(e.target.value)}
          />
        </label>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default RoadIdInput;
