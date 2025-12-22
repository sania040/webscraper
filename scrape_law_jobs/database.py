from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./jobs.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    organization = Column(String)
    location = Column(String)
    description = Column(Text)
    url = Column(String, unique=True) # Unique to prevent duplicates
    is_1l = Column(Boolean, default=False)

def init_db():
    Base.metadata.create_all(bind=engine)