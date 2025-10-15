from fastapi import UploadFile


async def upload(file: UploadFile):
    if not file:
        raise Exception('File not found')
    else:
        with open(f'./images/{file.filename}', 'wb') as buffer:
            buffer.write(await file.read())
