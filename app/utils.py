import os
import uuid
from flask import current_app

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_file(file, folder_key):
    if not file or file.filename == '':
        return None
    if not allowed_file(file.filename):
        return None
    
    folder = current_app.config[folder_key]
    os.makedirs(folder, exist_ok=True)

    ext = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(folder, unique_filename)
    file.save(filepath)
    return unique_filename