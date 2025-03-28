import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import AxiosInstance from '../Axios'; // Asegúrate de importar la instancia de Axios

const EstanciaPromedioChart = () => {
  // Estado para almacenar los datos del gráfico
  const [data, setData] = useState([]);

  // Hacer la solicitud al endpoint cuando el componente se monte
  useEffect(() => {
    // Suponiendo que el endpoint es "/api/promedio_ocupacion"
    AxiosInstance.get('grafico/')  // Usamos la instancia de Axios
      .then((response) => {
        // Transformar los datos para tener el formato adecuado para el gráfico
        const transformedData = response.data.map((item) => ({
          hora: item.intervalo,  // Esto es el intervalo de tiempo (por ejemplo, "06:00 - 07:00")
          tiempoEstancia: Math.round(item.tiempo_estancia_promedio), // El promedio de ocupación
        }));

        // Actualizar el estado con los nuevos datos
        setData(transformedData);
      })
      .catch((error) => {
        console.error('Error al obtener los datos:', error);
      });
  }, []); // El array vacío significa que esto se ejecutará solo una vez, al montarse el componente

  return (
    <div>
      {/* Verificamos si los datos están disponibles antes de renderizar el gráfico */}
      {data.length > 0 ? (
        <LineChart width={370} height={400} data={data}>
          {/* Cuadrícula de fondo */}
          <CartesianGrid strokeDasharray="3 3" />
          
          {/* Eje X y Eje Y */}
          <XAxis dataKey="hora" />
          <YAxis label={{ value: 'Minutos', angle: -90, position: 'insideLeft' }} />
          
          {/* Tooltip para información al pasar el mouse */}
          <Tooltip />
          
          {/* Leyenda */}
          <Legend />
          
          {/* Línea principal con estilo */}
          <Line type="monotone" dataKey="tiempoEstancia" stroke="#00C49F" strokeWidth={2} />
        </LineChart>
      ) : (
        <p>Cargando datos...</p>  // Mostrar un mensaje de carga mientras los datos no estén disponibles
      )}
    </div>
  );
};

export default EstanciaPromedioChart;
