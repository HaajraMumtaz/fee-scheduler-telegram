# app/db/base.py
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# app/db/connection.py
from sqlalchemy import create_engine
engine = create_engine("sqlite:///your_db_file.db", echo=True)
from app.db.base import Base
from app.db.engine import engine

# ⚠️ WARNING: this deletes all tables and data!
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("✅ Database tables recreated")
