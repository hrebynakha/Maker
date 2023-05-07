import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const Dashboard = () => {
  const [temperature, setTemperature] = useState('');
  const [humidity, setHumidity] = useState('');
  const [waterLevel, setWaterLevel] = useState('');
  const [temperatureData, setTemperatureData] = useState([]);
  const [humidityData, setHumidityData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const temperatureResponse = await axios.get('http://localhost:8000/temperature');
        const { data } = temperatureResponse;
        if (data && data.temperature) {
          const { temperature } = data;
          setTemperature(temperature);
          updateTemperatureChart(temperature);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }

      try {
        const humidityResponse = await axios.get('http://localhost:8000/humidity');
        const { data } = humidityResponse;
        if (data && data.humidity) {
          const { humidity } = data;
          setHumidity(humidity);
          updateHumidityChart(humidity);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }

      try {
        const waterLevelResponse = await axios.get('http://localhost:8000/water-level');
        const { data } = waterLevelResponse;
        if (data && data.water_level) {
          const { waterLevel } = data;
          setWaterLevel(waterLevel);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    const interval = setInterval(fetchData, 5000); // Fetch data every 5 seconds

    return () => {
      clearInterval(interval); // Clear the interval when the component is unmounted
    };
  }, []);

  const updateTemperatureChart = (newTemperature) => {
    setTemperatureData((prevData) => {
      const newData = [...prevData, { time: new Date().toLocaleTimeString(), temperature: newTemperature }];
      if (newData.length > 10) {
        newData.shift();
      }
      return newData;
    });
  };

  const updateHumidityChart = (newHumidity) => {
    setHumidityData((prevData) => {
      const newData = [...prevData, { time: new Date().toLocaleTimeString(), humidity: newHumidity }];
      if (newData.length > 10) {
        newData.shift();
      }
      return newData;
    });
  };

  const waterLevelColor = waterLevel === 0 ? 'red' : 'green';

  return (
    <div>
      <h2>Dashboard</h2>
      <div>
        <h3>Temperature</h3>
        <p>Current Temperature: {temperature}</p>
        <LineChart width={400} height={300} data={temperatureData}>
          <XAxis dataKey="time" />
          <YAxis />
          <CartesianGrid strokeDasharray="3 3" />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="temperature" stroke="#2196f3" dot={false} />
        </LineChart>
      </div>
      <div>
        <h3>Humidity</h3>
        <p>Current Humidity: {humidity}</p>
        <LineChart width={400} height={300} data={humidityData}>
          <XAxis dataKey="time" />
          <YAxis />
          <CartesianGrid strokeDasharray="3 3" />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="humidity" stroke="#2196f3" dot={false} />
        </LineChart>
      </div>
      <div>
        <h3>Water Level</h3>
        <p style={{ color: waterLevelColor }}>
          Water Level: {waterLevel === 0 ? 'Low' : 'High'}
        </p>
      </div>
    </div>
  );
};

export default Dashboard;
