import os
import shutil
from fastapi import UploadFile


__UPLOAD_DIR = 'images'

def get_upload_dir() -> str:
    return __UPLOAD_DIR

def save_image(file: UploadFile):
    if not file:
        raise Exception('File not found')
    else:
        file_path = os.path.join(get_upload_dir(), file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

def remove_image(file_name: str):
    if not file_name:
        return
    
    file_path = os.path.join(get_upload_dir(), file_name)
    
    if os.path.exists(file_path):
        os.remove(file_path)
