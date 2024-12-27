from flask import Flask, request, jsonify
import json

# Initialize Flask app
app = Flask(__name__)

# Example route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Input data (temperature, precipitation)
    
    # Example model prediction code
    temperature = data.get("temperature")
    precipitation = data.get("precipitation")
    
    # Model prediction logic (example)
    prediction = f"Prediction based on {temperature}°C temperature and {precipitation}mm precipitation"
    
    return jsonify({"prediction": prediction})

# For Vercel to work, we need to define a serverless function handler
def handler(request):
    return app(request)
