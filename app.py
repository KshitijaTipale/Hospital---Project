from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__)

# --- Mock Prediction Logic ---
def mock_predict_yield(taluk, rainfall, temperature, humidity, ndvi):
    """
    Simulated Model Logic. 
    Replace this function body with actual model loading and inference.
    """
    # Base yield assumption
    base_yield = 80.0
    
    # Factors (Simplified Heuristics)
    # Rainfall: More is generally better up to a point
    rain_factor = (rainfall / 1000.0) * 10.0 
    
    # NDVI: Higher is better (0-1)
    ndvi_factor = ndvi * 25.0
    
    # Temperature: Penalize extremes (Ideal ~30)
    temp_penalty = abs(30 - temperature) * 0.8
    
    # Humidity: Minor positive factor
    humidity_factor = (humidity / 100.0) * 5.0
    
    # Taluk specific adjustments (arbitrary for demo)
    taluk_modifiers = {
        "Ahmednagar": 0, "Rahata": 5, "Rahuri": 8, 
        "Sangamner": 2, "Shrigonda": -2, "Pathardi": -5, "Parner": -3
    }
    region_mod = taluk_modifiers.get(taluk, 0)
    
    final_yield = base_yield + rain_factor + ndvi_factor + humidity_factor + region_mod - temp_penalty
    
    # Add random noise for realism
    final_yield += random.uniform(-3, 3)
    
    # Clamp results
    return max(10.0, min(150.0, final_yield))

# --- Routes ---

@app.route('/')
def home():
    """Serves the main HTML page."""
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """API Endpoint for prediction and serving the prediction page."""
    if request.method == 'GET':
        return render_template('predict.html')

    try:
        data = request.json
        
        # simulated processing delay
        time.sleep(1.0) 
        
        taluk = data.get('taluk', 'Ahmednagar')
        rainfall = float(data.get('rainfall', 0))
        temperature = float(data.get('temperature', 30))
        humidity = float(data.get('humidity', 50))
        ndvi = float(data.get('ndvi', 0.5))
        
        result = mock_predict_yield(taluk, rainfall, temperature, humidity, ndvi)
        
        return jsonify({
            'success': True,
            'yield': result,
            'message': 'Prediction successful'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    # Running in debug mode for development
    app.run(debug=True, port=5000)
