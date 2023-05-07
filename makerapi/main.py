import sys
import os

# Add the project directory to the Python module search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import serial
from fastapi import FastAPI
from makerapi.models import schemas
import uvicorn


app = FastAPI()
arduino = serial.Serial('COM3', 9600)  # Replace 'COM3' with the appropriate port

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run the FastAPI server
