from flask import Blueprint, render_template, request, jsonify, current_app
from utils.rag_processor import process_rag, answer_question
from utils.file_utils import get_uploaded_py_files_content
from utils.rag_processor import answer_question
from openai import OpenAI
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
        # Step 1: Get code contents
        upload_folder = current_app.config['UPLOAD_FOLDER']
        code_contents = get_uploaded_py_files_content(upload_folder)

        # Step 2: Get RAG content
        rag_content = answer_question(question)

        # Step 3: Combine contents
        combined_content = f"{code_contents}\n\nRAG Response:\n{rag_content}"

        # Step 4: Call the SambaNova AI model
        client = OpenAI(
            base_url="https://api.sambanova.ai/v1",
            api_key="0ac5c7fc-6cce-43d4-b866-354185cde242"
        )

        completion = client.chat.completions.create(
            model="Meta-Llama-3.1-8B-Instruct",
            messages = [
                {"role": "system", "content": "You are a debugger. Give advice and reference the error explicitly (error code and line) in your response if there is one, if not, dont."},
                {"role": "user", "content": combined_content}
            ],
            stream= False
        )
        
        
        assistant_response1 = completion.choices[0].message.content
        
        completion = client.chat.completions.create(
            model="Meta-Llama-3.1-8B-Instruct",
            messages = [
                {"role": "system", "content": "You are a critiquer, harshly evaluate the debugging advice below, be succinct but comprehensive."},
                {"role": "user", "content": assistant_response1}
            ],
            stream= False
        )
        critiquer_response = completion.choices[0].message.content
        # Get the assistant's response
        completion = client.chat.completions.create(
            model="Meta-Llama-3.1-8B-Instruct",
            max_completion_tokens=500,
            messages = [
                {"role": "system", "content": "You are a debugger, take into account the criticism below and revise your previous advice. Keep it short and concise"},
                {"role": "user", "content": critiquer_response}
            ],
            stream= False
        )
        
        assistant_response2 = completion.choices[0].message.content

        # Return the assistant's response in JSON format
        return jsonify({'answer': assistant_response2}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


    except Exception as e:
        return jsonify({'error': str(e)}), 500
