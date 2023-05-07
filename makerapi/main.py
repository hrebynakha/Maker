import sys
import os

# Add the project directory to the Python module search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import serial
from fastapi import FastAPI
from makerapi.models.schemas import CookingProcess, ProcessStep
from makerapi.models.database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware

import uvicorn




app = FastAPI()
arduino = serial.Serial('COM3', 9600)  # Replace 'COM3' with the appropriate port


origins = [
    "http://localhost:3000",
    # Add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/temperature")
def get_temperature():
    arduino.write(b'T')  # Send a command to Arduino to request temperature reading
    data = arduino.readline().decode().strip()  # Read the data from Arduino
    temperature = parse_temperature(data)  # Parse the temperature value from the received data
    return {"temperature": temperature}

@app.get("/humidity")
def get_humidity():
    arduino.write(b'H')  # Send a command to Arduino to request humidity reading
    data = arduino.readline().decode().strip()  # Read the data from Arduino
    humidity = parse_humidity(data)  # Parse the humidity value from the received data
    return {"humidity": humidity}

@app.get("/water-level")
def get_water_level():
    arduino.write(b'W')  # Send a command to Arduino to request water level reading
    data = arduino.readline().decode().strip()  # Read the data from Arduino
    water_level = parse_water_level(data)  # Parse the water level value from the received data
    return {"water_level": water_level}

def parse_temperature(data):
    # Assuming the data format is "Temperature: XX°C\tHumidity: XX%\tWater Level: XX"
    temperature_start = data.index("Temperature: ") + len("Temperature: ")
    temperature_end = data.index("°C")
    temperature = data[temperature_start:temperature_end]
    return temperature

def parse_humidity(data):
    # Assuming the data format is "Temperature: XX°C\tHumidity: XX%\tWater Level: XX"
    humidity_start = data.index("Humidity: ") + len("Humidity: ")
    humidity_end = data.index("%")
    humidity = data[humidity_start:humidity_end]
    return humidity

def parse_water_level(data):
    # Assuming the data format is "Temperature: XX°C\tHumidity: XX%\tWater Level: XX"
    water_level_start = data.index("Water Level: ") + len("Water Level: ")
    water_level = data[water_level_start:]
    return water_level


@app.get("/processes/{process_id}")
def get_process(process_id: int):
    db = SessionLocal()
    process = db.query(CookingProcess).get(process_id)
    db.close()
    
    if process:
        return process
    else:
        return {"message": "Process not found"}

@app.post("/processes")
def create_process(process: CookingProcess):
    db = SessionLocal()
    db.add(process)
    db.commit()
    db.refresh(process)
    db.close()
    
    return {"message": "Process created"}

@app.put("/processes/{process_id}")
def update_process(process_id: int, process: CookingProcess):
    db = SessionLocal()
    existing_process = db.query(CookingProcess).get(process_id)
    
    if existing_process:
        existing_process.name = process.name
        db.commit()
        db.close()
        return {"message": "Process updated"}
    else:
        db.close()
        return {"message": "Process not found"}

@app.delete("/processes/{process_id}")
def delete_process(process_id: int):
    db = SessionLocal()
    existing_process = db.query(CookingProcess).get(process_id)
    
    if existing_process:
        db.delete(existing_process)
        db.commit()
        db.close()
        return {"message": "Process deleted"}
    else:
        db.close()
        return {"message": "Process not found"}

@app.post("/processes/{process_id}/steps")
def add_process_step(process_id: int, step: ProcessStep):
    db = SessionLocal()
    existing_process = db.query(CookingProcess).get(process_id)
    
    if existing_process:
        existing_process.process_steps.append(step)
        db.commit()
        db.close()
        return {"message": "Step added to process"}
    else:
        db.close()
        return {"message": "Process not found"}

@app.put("/processes/{process_id}/steps/{step_id}")
def update_process_step(process_id: int, step_id: int, step: ProcessStep):
    db = SessionLocal()
    existing_process = db.query(CookingProcess).get(process_id)
    
    if existing_process and step_id < len(existing_process.process_steps):
        existing_step = existing_process.process_steps[step_id]
        existing_step.name = step.name
        existing_step.requirements = step.requirements
        existing_step.actions = step.actions
        db.commit()
        db.close()
        return {"message": "Step updated"}
    else:
        db.close()
        return {"message": "Process or step not found"}

@app.delete("/processes/{process_id}/steps/{step_id}")
def delete_process_step(process_id: int, step_id: int):
    db = SessionLocal()
    existing_process = db.query(CookingProcess).get(process_id)
    
    if existing_process and step_id < len(existing_process.process_steps):
        existing_step = existing_process.process_steps[step_id]
        db.delete(existing_step)
        db.commit()
        db.close()
        return {"message": "Step deleted"}
    else:
        db.close()
        return {"message": "Process or step not found"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run the FastAPI server
