from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel


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

class ProcessStep(BaseModel):
    def __init__(self, name, requirements=None, actions=None):
        self.name = name
        self.requirements = requirements or []
        self.actions = actions or []


class CookingProcess(BaseModel):
    def __init__(self, name):
        self.name = name
        self.process_steps = []

    def add_step(self, name, requirements=None, actions=None):
        step = ProcessStep(name, requirements, actions)
        self.process_steps.append(step)

    def execute_process(self, available_items):
        for step in self.process_steps:
            if self.check_requirements(step, available_items):
                print(f"Executing step: {step.name}")
                for action in step.actions:
                    # Execute the action here...
                    print(f"Performing action: {action}")
                print("Step completed.\n")
                available_items.append(step.name)
            else:
                print(f"Cannot execute step: {step.name}. Requirements not met.\n")

    def check_requirements(self, step, available_items):
        for requirement in step.requirements:
            if requirement not in available_items:
                return False
        return True
