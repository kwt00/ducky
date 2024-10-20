from flask import Blueprint, render_template, request, jsonify, current_app
from utils.rag_processor import process_rag, answer_question

rag_bp = Blueprint('rag', __name__)


@rag_bp.route('/start_indexing', methods=['POST'])
def start_indexing():
    try:
        folder_path = current_app.config['UPLOAD_FOLDER']
        process_rag(folder_path, current_app.config['FAISS_INDEX_FOLDER'])
        return jsonify({'message': 'Indexing complete'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@rag_bp.route('/rag')
def rag():
    try:
        folder_path = current_app.config['UPLOAD_FOLDER']
        process_rag(folder_path, current_app.config['FAISS_INDEX_FOLDER'])
        return render_template('assistant.html')
    except Exception as e:
        return f"An error occurred: {e}", 500

@rag_bp.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    try:
        answer = answer_question(question)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
