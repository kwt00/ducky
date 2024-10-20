import os
from werkzeug.utils import secure_filename

def sanitize_filepath(filepath):
    # Sanitize the file path to prevent path traversal attacks
    filepath = filepath.lstrip('/\\')
    filepath = os.path.normpath(filepath)
    if '..' in filepath or filepath.startswith(('/', '\\')):
        raise ValueError('Invalid filepath')
    parts = filepath.split(os.sep)
    sanitized_parts = [secure_filename(part) for part in parts]
    return os.path.join(*sanitized_parts)

def save_uploaded_files(files, upload_folder):
    for file in files:
        filename = file.filename
        if filename == '':
            continue
        sanitized_path = sanitize_filepath(filename)
        filepath = os.path.join(upload_folder, sanitized_path)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)


def get_uploaded_py_files_content(upload_folder):
    code_contents = ""
    for root, dirs, files in os.walk(upload_folder):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    code_contents += f'\n# File: {file_path}\n'
                    code_contents += f.read()
    return code_contents