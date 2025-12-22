from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal, Job, init_db
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

app = FastAPI(title="1L Law Jobs API", description="API to fetch 1L summer law jobs in Georgia")

# Initialize DB on startup
init_db()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Updated Pydantic Model for Response (V2 Compatible)
class JobSchema(BaseModel):
    title: str
    organization: str
    location: str
    description: Optional[str] = None
    url: Optional[str] = None
    is_1l: bool

    # This replaces the old 'class Config'
    model_config = ConfigDict(from_attributes=True)

@app.get("/jobs", response_model=List[JobSchema])
def read_jobs(
    skip: int = 0, 
    limit: int = 10, 
    city: Optional[str] = None, 
    is_1l: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Job)
    
    if city:
        query = query.filter(Job.location.contains(city))
    if is_1l is not None:
        query = query.filter(Job.is_1l == is_1l)
        
    jobs = query.offset(skip).limit(limit).all()
    return jobs

@app.get("/")
def root():
    return {"message": "Go to /docs to see the API documentation"}