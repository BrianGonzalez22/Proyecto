import React, { useEffect, useState } from 'react';
import AxiosInstance from '../Axios'; // Suponiendo que tu instancia axios está configurada
import { BarChart, Bar, XAxis, YAxis, Tooltip, Cell, CartesianGrid, ResponsiveContainer } from 'recharts';

const HeatmapChart = () => {
  const [data, setData] = useState([]);

  // Obtener los datos de la API
  useEffect(() => {
    AxiosInstance.get('grafico/')
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error('Error al obtener datos:', error);
      });
  }, []);

  // Función para asignar colores
  const getColor = (value) => {
    if (value < 30) return "#b9fbc0";
    if (value < 60) return "#98f5e1";
    if (value < 90) return "#57cc99";
    if (value < 120) return "#38a3a5";
    return "#22577a";
  };

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="intervalo" />
        <YAxis label={{ value: 'Minutos', angle: -90, position: 'insideLeft' }} />
        <Tooltip />
        <Bar dataKey="tiempo_estancia_promedio">
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={getColor(entry.tiempo_estancia_promedio)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};

export default HeatmapChart;
