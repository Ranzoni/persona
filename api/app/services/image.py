from fastapi import UploadFile


__UPLOAD_DIR = 'images'

def get_upload_dir() -> str:
    return __UPLOAD_DIR

async def upload(file: UploadFile):
    if not file:
        raise Exception('File not found')
    else:
        with open(f'./images/{file.filename}', 'wb') as buffer:
            buffer.write(await file.read())
