from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import os
from dotenv import load_dotenv

# This line is what actually reads the .env file
load_dotenv() 

db_url = os.getenv("DATABASE_URL")


engine = create_engine(
    db_url,
    pool_size=5,        # Keeps a small pool of connections ready
    max_overflow=10,    # Allows extra connections during spikes
    pool_pre_ping=True  # Health-checks the connection before using it
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)