import React, { useState } from 'react';

function GetActivityGenData() {
  const [formData, setFormData] = useState({
    inhabitants: '56000',
    households: '12000',
    childrenAgeLimit: '18',
    retirementAgeLimit: '60',
    carRate: '0.075',
    unemploymentRate: '0.071',
    footDistanceLimit: '1.5',
    incomingTraffic: '5726',
    outgoingTraffic: '5726'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://localhost:5000/generatetraffic', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    });
    const result = await response.json();
    console.log(result);
  };

  return (
    <div className="demographicInput">
        <h2>demographic Input</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Inhabitants:
          <input type="number" name="inhabitants" value={formData.inhabitants} onChange={handleChange} />
        </label>
        <label>
          Households:
          <input type="number" name="households" value={formData.households} onChange={handleChange} />
        </label>
        <label>
          Children Age Limit:
          <input type="number" name="childrenAgeLimit" value={formData.childrenAgeLimit} onChange={handleChange} />
        </label>
        <label>
          Retirement Age Limit:
          <input type="number" name="retirementAgeLimit" value={formData.retirementAgeLimit} onChange={handleChange} />
        </label>
        <label>
          Car Rate:
          <input type="number" name="carRate" value={formData.carRate} onChange={handleChange} />
        </label>
        <label>
          Unemployment Rate:
          <input type="number" name="unemploymentRate" value={formData.unemploymentRate} onChange={handleChange} />
        </label>
        <label>
          Foot Distance Limit:
          <input type="number" name="footDistanceLimit" value={formData.footDistanceLimit} onChange={handleChange} />
        </label>
        <label>
          Incoming Traffic:
          <input type="number" name="incomingTraffic" value={formData.incomingTraffic} onChange={handleChange} />
        </label>
        <label>
          Outgoing Traffic:
          <input type="number" name="outgoingTraffic" value={formData.outgoingTraffic} onChange={handleChange} />
        </label>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default GetActivityGenData;
