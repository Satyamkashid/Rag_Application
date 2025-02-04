# routes.py

from flask import Blueprint, request, jsonify
from controllers.upload_controller import upload_file
from controllers.process_controller import process_file
from controllers.llumo_controller import llumo_eval

# Define blueprints for routes
upload_routes = Blueprint('upload_routes', __name__)
process_routes = Blueprint('process_routes', __name__)
llumo_routes = Blueprint('llumo_routes', __name__)

# Upload route
@upload_routes.route('/upload', methods=['POST'])
def handle_upload():
    return upload_file()

# Process route
@process_routes.route('/process', methods=['POST'])
def handle_process():
    return process_file()

# LLUMO evaluation route
@llumo_routes.route('/llumo-eval', methods=['POST'])
def handle_llumo_eval():
    return llumo_eval()