from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from models.file import File
from core.storage import save_file

MAX_FILE_SIZE = 2 * 1024 * 1024 #2MB
ALLOWED_TYPES = {"image/png", "image/jpeg"}

def upload_user_avatar(db: Session, user_id: int, file: UploadFile):

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid File type")

    contents = file.file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    # reset pointer
    file.file.seek(0)

    filename, path = save_file(file)
    db_file = File(
        filename = filename,
        content_type = file.content_type,
        path = path,
        size = len(contents),
        owner_id = user_id
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file