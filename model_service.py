from flask import Flask, request, jsonify
import pickle
import os

app = Flask(__name__)

# Load the models
MODEL_PATH = "./models"
models = {
    "ph": pickle.load(open(os.path.join(MODEL_PATH, "pH_model.pkl"), "rb")),
    "do": pickle.load(open(os.path.join(MODEL_PATH, "DO_model.pkl"), "rb")),
    "bod": pickle.load(open(os.path.join(MODEL_PATH, "BOD_model.pkl"), "rb")),
    "total_coliform": pickle.load(open(os.path.join(MODEL_PATH, "TC_model.pkl"), "rb")),
    "fecal_coliform": pickle.load(open(os.path.join(MODEL_PATH, "FC_model.pkl"), "rb")),
}

@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict water quality parameters based on temperature and precipitation.
    """
    data = request.json

    # Validate input
    if not data or "temperature" not in data or "precipitation" not in data:
        return jsonify({"error": "Invalid input. Provide 'temperature' and 'precipitation'."}), 400

    temperature = data["temperature"]
    precipitation = data["precipitation"]

    # Ensure inputs are valid numbers
    try:
        temperature = float(temperature)
        precipitation = float(precipitation)
    except ValueError:
        return jsonify({"error": "Temperature and precipitation must be numeric values."}), 400

    # Predict using each model and round to 1 decimal place
    predictions = {}
    for parameter, model in models.items():
        prediction = model.predict([[temperature, precipitation]])[0]
        predictions[parameter] = round(prediction, 1)  # Round to 1 decimal place

    return jsonify(predictions)

@app.route("/", methods=["GET"])
def home():
    """
    Health check endpoint for the API.
    """
    return jsonify({"message": "Model service is running!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
