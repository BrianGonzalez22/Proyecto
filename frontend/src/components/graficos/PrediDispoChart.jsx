import React, { useEffect, useState } from "react";
import AxiosInstance from "../Axios";  // Importamos Axios
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";  // Importamos componentes de Recharts

const GraficoOcupacion = () => {
  const [data, setData] = useState([]);

  // Cargar los datos utilizando Axios
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await AxiosInstance.get("predecir-dispo/"); // Aquí la URL de tu API para obtener las predicciones
        setData(response.data);  // Almacenar los datos en el estado
      } catch (error) {
        console.error("Error al obtener los datos:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          {/* Ejes X e Y */}
          <XAxis dataKey="fecha" tick={{ fontSize: 12 }} tickFormatter={(value) => new Date(value).toLocaleString()} />
          <YAxis tick={{ fontSize: 12 }} />
          
          {/* Añadimos una cuadrícula */}
          <CartesianGrid strokeDasharray="3 3" />
          
          {/* Tooltip para mostrar información detallada */}
          <Tooltip formatter={(value) => `${value.toFixed(2)} lugares`} />

          {/* Leyenda */}
          <Legend />

          {/* Línea del gráfico de ocupación esperada */}
          <Line
            type="monotone"
            dataKey="ocupacion_esperada"
            stroke="#8884d8" // Color de la línea
            activeDot={{ r: 8 }} // Puntos activos en la línea
            strokeWidth={2}
            dot={false} // Si no quieres mostrar los puntos individuales en la línea
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default GraficoOcupacion;
