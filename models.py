from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class People(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True)
    birth_year = Column(String, nullable=True)
    eye_color = Column(String, nullable=True)
    films = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    hair_color = Column(String, nullable=True)
    height = Column(String, nullable=True)
    homeworld = Column(String, nullable=True)
    mass = Column(String, nullable=True)
    name = Column(String, nullable=True, unique=True)
    skin_color = Column(String, nullable=True)
    species = Column(String, nullable=True)
    starships = Column(String, nullable=True)
    vehicles = Column(String, nullable=True)
