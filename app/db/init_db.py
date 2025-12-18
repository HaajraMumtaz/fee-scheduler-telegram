from .engine import engine
from .base import Base
from . import models  # IMPORTANT: registers models

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")
