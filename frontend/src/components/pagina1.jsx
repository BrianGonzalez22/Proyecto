import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';

// Datos de ejemplo
const parkingData = [
  { hour: '00:00', vehicles: 20 },
  { hour: '01:00', vehicles: 15 },
  { hour: '02:00', vehicles: 10 },
  { hour: '03:00', vehicles: 5 },
  { hour: '04:00', vehicles: 8 },
  { hour: '05:00', vehicles: 12 },
  { hour: '06:00', vehicles: 25 },
  { hour: '07:00', vehicles: 50 },
  { hour: '08:00', vehicles: 80 },
  { hour: '09:00', vehicles: 100 },
  { hour: '10:00', vehicles: 120 },
  { hour: '11:00', vehicles: 150 },
  { hour: '12:00', vehicles: 180 },
];

const revenueData = [
  { day: 'Lunes', revenue: 500 },
  { day: 'Martes', revenue: 700 },
  { day: 'Miércoles', revenue: 600 },
  { day: 'Jueves', revenue: 900 },
  { day: 'Viernes', revenue: 1200 },
  { day: 'Sábado', revenue: 1500 },
  { day: 'Domingo', revenue: 1000 },
];

const parkedVehicles = [
  { plate: 'ABC-123', entryTime: '08:00', duration: '2 horas' },
  { plate: 'XYZ-789', entryTime: '09:30', duration: '1 hora' },
  { plate: 'DEF-456', entryTime: '10:15', duration: '3 horas' },
  { plate: 'GHI-987', entryTime: '11:00', duration: '30 minutos' },
];

const ParkingDashboard = () => {
  const [metrics, setMetrics] = useState({
    totalParked: 150,
    availableSpaces: 50,
    totalRevenue: 5000,
  });

  // Simular actualización en tiempo real
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics((prev) => ({
        ...prev,
        totalParked: prev.totalParked + Math.floor(Math.random() * 5),
        availableSpaces: prev.availableSpaces - Math.floor(Math.random() * 5),
        totalRevenue: prev.totalRevenue + Math.floor(Math.random() * 100),
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      {/* Encabezado */}
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Dashboard de Control de Estacionamiento</h1>
        <button className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
          Actualizar Datos
        </button>
      </header>

      {/* Métricas principales */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-700">Vehículos Estacionados</h3>
          <p className="text-2xl font-bold text-gray-900">{metrics.totalParked}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-700">Espacios Disponibles</h3>
          <p className="text-2xl font-bold text-gray-900">{metrics.availableSpaces}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          
        </div>
      </div>

      {/* Gráficos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Ocupación del Estacionamiento</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={parkingData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="hour" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="vehicles" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Ingresos Diarios</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={revenueData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="revenue" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Tabla de vehículos estacionados */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Vehículos Estacionados</h2>
        <table className="w-full text-left">
          <thead>
            <tr>
              <th className="py-2">Placa</th>
              <th className="py-2">Hora de Entrada</th>
              <th className="py-2">Tiempo Estacionado</th>
            </tr>
          </thead>
          <tbody>
            {parkedVehicles.map((vehicle, index) => (
              <tr key={index} className="border-t">
                <td className="py-2">{vehicle.plate}</td>
                <td className="py-2">{vehicle.entryTime}</td>
                <td className="py-2">{vehicle.duration}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pie de página */}
      <footer className="mt-8 text-center text-gray-600">
        <p>© 2023 Control de Estacionamiento. Todos los derechos reservados.</p>
      </footer>
    </div>
  );
};

export default ParkingDashboard;