from flask import Blueprint, request, jsonify
import os

upload_bp = Blueprint('upload', __name__)

# Define the directory where uploaded files will be saved
UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Helper function to check if a file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    # Check if the POST request has a file part
    if 'file' not in request.files:
        return jsonify(message='No file part'), 400

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return jsonify(message='No selected file'), 400

    # Check if the file has an allowed extension
    if not allowed_file(file.filename):
        return jsonify(message='Invalid file extension'), 400

    # Create the "data" directory if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Save the file to the "data" directory
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))

    return jsonify(message='File uploaded successfully'), 200