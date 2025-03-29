import React, { useEffect, useState } from 'react';
import AxiosInstance from '../Axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Cell, CartesianGrid, ResponsiveContainer } from 'recharts';

const HeatmapChart = () => {
  const [data, setData] = useState([]);

  // Obtener los datos de la API
  useEffect(() => {
    AxiosInstance.get('predecir-prophet/')
      .then((response) => {
        const filteredData = response.data.map(item => {
          // Crear un nuevo objeto para cada fila, pero solo tomar la hora
          const date = new Date(item.hora);
          const hora = date.getHours().toString().padStart(2, '0'); // Extrae solo la hora (formato HH)
          const minutos = date.getMinutes().toString().padStart(2, '0'); // Extrae los minutos (formato MM)
          return {
            ...item,
            hora: `${hora}:${minutos}`, // Crear formato "HH:MM"
          };
        });
        setData(filteredData);
      })
      .catch((error) => {
        console.error('Error al obtener datos:', error);
      });
  }, []);

  // Función para asignar colores basada en la predicción
  const getColor = (value) => {
    if (value < 5) return "#b9fbc0";
    if (value < 10) return "#98f5e1";
    if (value > 17) return "#57cc99";
    if (value < 16) return "#38a3a5";
    return "#22577a";
  };

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="hora" />
        <YAxis label={{ value: 'Entradas', angle: -90, position: 'insideLeft' }} />
        <Tooltip />
        <Bar dataKey="prediccion">
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={getColor(entry.prediccion)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};

export default HeatmapChart;
