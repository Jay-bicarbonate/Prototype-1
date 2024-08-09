import React from 'react';
import axios from 'axios';

const GenerateConfigButton = () => {
    const handleGenerateConfig = () => {
        axios.post('http://localhost:5000/generate-config')
            .then(response => {
                alert(response.data.message);
            })
            .catch(error => {
                console.error('There was an error!', error);
            });
    };

    return (
        <button onClick={handleGenerateConfig}>
            Generate Config
        </button>
    );
};

export default GenerateConfigButton;
