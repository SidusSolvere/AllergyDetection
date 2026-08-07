from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///predictions.db")
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True)
    result = Column(String)
    severity_percentage = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)