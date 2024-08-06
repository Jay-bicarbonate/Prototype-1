document.getElementById('demographicForm').addEventListener('submit', async function(e) {
        e.preventDefault();
    
        const formData = {
            inhabitants: document.getElementById('inhabitants').value,
            households: document.getElementById('households').value,
            childrenAgeLimit: document.getElementById('childrenAgeLimit').value,
            retirementAgeLimit: document.getElementById('retirementAgeLimit').value,
            carRate: document.getElementById('carRate').value,
            unemploymentRate: document.getElementById('unemploymentRate').value,
            footDistanceLimit: document.getElementById('footDistanceLimit').value,
            incomingTraffic: document.getElementById('incomingTraffic').value,
            outgoingTraffic: document.getElementById('outgoingTraffic').value
        };
    
        try {
            const response = await fetch('http://localhost:5000/generatetraffic', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
    
            const result = await response.json();
            console.log(result);
        } catch (error) {
            console.error('Error:', error);
        }
    });
    
    const syncSliderWithInput = (inputId, sliderId) => {
        const input = document.getElementById(inputId);
        const slider = document.getElementById(sliderId);
    
        input.addEventListener('input', () => {
            slider.value = input.value;
        });
    
        slider.addEventListener('input', () => {
            input.value = slider.value;
        });
    };
    
    syncSliderWithInput('inhabitants', 'inhabitantsSlider');
    syncSliderWithInput('households', 'householdsSlider');
    syncSliderWithInput('childrenAgeLimit', 'childrenAgeLimitSlider');
    syncSliderWithInput('retirementAgeLimit', 'retirementAgeLimitSlider');
    syncSliderWithInput('carRate', 'carRateSlider');
    syncSliderWithInput('unemploymentRate', 'unemploymentRateSlider');
    syncSliderWithInput('footDistanceLimit', 'footDistanceLimitSlider');
    syncSliderWithInput('incomingTraffic', 'incomingTrafficSlider');
    syncSliderWithInput('outgoingTraffic', 'outgoingTrafficSlider');
    