from sqlalchemy import Column, Integer, JSON
from database import Base

class JSONData(Base):
    __tablename__ = "json_data"
    id = Column(Integer, primary_key=True, index=True)
    raw = Column(JSON)
