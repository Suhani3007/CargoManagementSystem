from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

class CargoItem(BaseModel):
    cargo_name: Optional[str] = ""
    description: Optional[str] = ""

class read_cargo(BaseModel):
    page: int
    rec_size: int
    filter: CargoItem
    sort: str




Base = declarative_base()

class Cargo(Base):
    __tablename__ = 'cargo'

    cargo_id = Column(String, primary_key=True)
    cargo_name = Column(String, unique=True, nullable=False)
    description = Column(String)
    quantity = Column(Integer)
    archive = Column(Boolean, default=False)