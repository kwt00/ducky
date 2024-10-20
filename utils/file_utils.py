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


def save_file_content(relative_path, content, upload_folder):
    # Sanitize the file path
    relative_path = sanitize_filepath(relative_path)
    # Extract the base filename
    base_filename = os.path.basename(relative_path)
    # Skip saving hidden files
    if base_filename.startswith('.'):
        print(f"Skipping hidden file: {relative_path}")
        return
    filepath = os.path.join(upload_folder, relative_path)
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    # Write the content to the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
