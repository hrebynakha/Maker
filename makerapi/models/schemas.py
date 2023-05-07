from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./sqlite.db"  # Replace with your database URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Container(Base):
    __tablename__ = "containers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    type = Column(String(100))
    capacity = Column(Integer)


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    category = Column(String(100))


class CookingTiming(Base):
    __tablename__ = "cooking_timings"

    id = Column(Integer, primary_key=True, index=True)
    container_id = Column(Integer, ForeignKey("containers.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    timing = Column(Integer)

    container = relationship("Container", backref="cooking_timings")
    ingredient = relationship("Ingredient", backref="cooking_timings")



Base.metadata.create_all(bind=engine)
