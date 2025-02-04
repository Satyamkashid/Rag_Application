# app.py

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from routes import upload_routes, process_routes, llumo_routes
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

# Load environment variables
load_dotenv()

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Set upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Register routes
app.register_blueprint(upload_routes)
app.register_blueprint(process_routes)
app.register_blueprint(llumo_routes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)