document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    const resultSection = document.getElementById('resultSection');
    const resultCard = document.getElementById('resultCard');
    const placeholderState = document.getElementById('placeholderState');

    // UI Elements to update
    const yieldValueElement = document.getElementById('yieldValue');
    const yieldBar = document.getElementById('yieldBar');
    const yieldBarValue = document.getElementById('yieldBarValue');

    // Slider Value Update
    const ndviInput = document.getElementById('ndvi');
    const ndviValue = document.getElementById('ndviValue');

    ndviInput.addEventListener('input', (e) => {
        ndviValue.textContent = e.target.value;
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show Loading State (Spinner is already there in placeholder, we just need to indicate processing)
        const submitBtn = form.querySelector('.predict-btn');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = 'Analyzing... <span class="btn-icon">⚙️</span>';
        submitBtn.disabled = true;

        // Prepare Data
        const formData = {
            taluk: document.getElementById('taluk').value,
            rainfall: parseFloat(document.getElementById('rainfall').value),
            temperature: parseFloat(document.getElementById('temperature').value),
            humidity: parseFloat(document.getElementById('humidity').value),
            ndvi: parseFloat(document.getElementById('ndvi').value)
        };

        try {
            // Make API Request
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (data.success) {
                // Formatting
                const predictedYield = data.yield.toFixed(2);

                // Update UI
                yieldValueElement.textContent = predictedYield;

                // Logarithm or simple mapping for bar chart width (Max assumed ~150)
                const percentage = Math.min((predictedYield / 150) * 100, 100);
                yieldBar.style.width = `${percentage}%`;
                yieldBarValue.textContent = Math.round(predictedYield);

                // Switch View
                placeholderState.classList.add('hidden');
                resultCard.classList.remove('hidden');

                // Animation for number counter could be added here
            } else {
                alert('Prediction failed: ' + (data.error || 'Unknown error'));
            }

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while connecting to the server.');
        } finally {
            // Reset Button
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
        }
    });
});
