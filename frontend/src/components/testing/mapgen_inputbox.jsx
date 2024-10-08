import React, { useState } from 'react';

// 24.072170688204157, south: 23.981233711026714, east: 74.81498427757113, west: 74.69477235202582

function GenerateMap() {
  const [north, setNorth] = useState('22.7298');
  const [south, setSouth] = useState('22.7198');
  const [east, setEast] = useState('75.8903');
  const [west, setWest] = useState('75.8717');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = { north, south, east, west };

    const response = await fetch('http://localhost:5000/generatemap', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    console.log(result);
  };

  return (
    <div className='mapGen'>
      <h2>Map Generator</h2>
      <form onSubmit={handleSubmit}>
        <label>
          North:
          <input type="text" value={north} onChange={(e) => setNorth(e.target.value)} />
        </label>
        <br />
        <label>
          South:
          <input type="text" value={south} onChange={(e) => setSouth(e.target.value)} />
        </label>
        <br />
        <label>
          East:
          <input type="text" value={east} onChange={(e) => setEast(e.target.value)} />
        </label>
        <br />
        <label>
          West:
          <input type="text" value={west} onChange={(e) => setWest(e.target.value)} />
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default GenerateMap;
