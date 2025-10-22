import flask
from flask import Flask, jsonify, request, render_template
import json
from data_input import data_in
import numpy as np
import pickle



def load_models():
    file_name = "models/model_file.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
        feature_names = data.get('feature_names', None)
    return model, feature_names

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    try:
        # Get input features from request
        request_json = request.get_json()
        x = request_json['input']
        x_in = np.array(x).reshape(1,-1)
        # load model
        model, feature_names = load_models()
        prediction = model.predict(x_in)[0]
        return jsonify({'response': float(prediction)}), 200
    except Exception as e:
        print(f"Error: {str(e)}")  # Print to console for debugging
        return jsonify({'error': str(e)}), 400

@app.route('/predict_simple', methods=['POST'])
def predict_simple():
    try:
        # Get simple form inputs
        data = request.get_json()

        # Load model and feature names
        model, feature_names = load_models()

        # Create a zero array with all 165 features
        x_input = np.zeros(len(feature_names))

        # Map numeric features (these are not one-hot encoded)
        feature_mapping = {
            'Rating': data.get('rating', 4.0),
            'age': data.get('age', 20),
            'desc_len': data.get('desc_len', 4000),
            'python': 1.0 if data.get('python', False) else 0.0,
            'excel': 1.0 if data.get('excel', False) else 0.0,
            'sql': 1.0 if data.get('sql', False) else 0.0,
            'tableau': 1.0 if data.get('tableau', False) else 0.0,
            'spark': 1.0 if data.get('spark', False) else 0.0,
            'aws': 1.0 if data.get('aws', False) else 0.0,
            'machine learning': 1.0 if data.get('ml', False) else 0.0
        }

        # Set the feature values
        for i, feature_name in enumerate(feature_names):
            if feature_name in feature_mapping:
                x_input[i] = feature_mapping[feature_name]

        # Make prediction
        x_in = x_input.reshape(1, -1)
        prediction = model.predict(x_in)[0]

        return jsonify({'response': float(prediction)}), 200
    except Exception as e:
        print(f"Error in predict_simple: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)