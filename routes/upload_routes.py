from flask import Blueprint, request, jsonify, current_app
from utils.file_utils import save_uploaded_files

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload_folder', methods=['POST'])
def upload_folder():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files part'}), 400

    files = request.files.getlist('files[]')
    try:
        save_uploaded_files(files, current_app.config['UPLOAD_FOLDER'])
        return jsonify({'message': 'Upload complete'}), 200
    except Exception as e:
        print(f"Exception occurred during file upload: {e}")
        return jsonify({'error': str(e)}), 500
