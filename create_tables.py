from core.database import engine, Base
from models.user import User
from models.file import File

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)