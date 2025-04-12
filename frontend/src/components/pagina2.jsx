import {React, useState, useEffect} from 'react'
import { MenuItem, Select, FormControl, InputLabel, Typography } from '@mui/material';
import TablaDatos from './tabladatos';
import AxiosInstance from './axios';
const Pagina2 = () => {

      const [datos, setDatos] = useState({
        vehiculos: [],
        usuarios: [],
        registros: []
      });
    
      const [seleccion, setSeleccion] = useState('vehiculos');
      const [columnasDinamicas, setColumnasDinamicas] = useState([]);
      const [fechasDisponibles, setFechasDisponibles] = useState([]);
      const [fechaSeleccionada, setFechaSeleccionada] = useState('');
    
      useEffect(() => {
        AxiosInstance.get('obtener-datos/')
          .then(response => {
            setDatos(response.data);
          })
          .catch(error => {
            console.error('Error al obtener los datos:', error);
          });
      }, []);

            // Obtener las fechas disponibles solo cuando la tabla seleccionada sea 'registros'
        useEffect(() => {
            if (seleccion === 'registros') {
            AxiosInstance.get('obtener-fechas-registros/')
                .then(response => {
                // Formateamos las fechas para que solo contengan el día, mes y año
                const fechasFormateadas = response.data.map(fecha => {
                    const date = new Date(fecha);
                    return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
                });
                setFechasDisponibles(fechasFormateadas);
                })
                .catch(error => {
                console.error('Error al obtener las fechas:', error);
                });
            } else {
            setFechasDisponibles([]); // Si no es registros, limpia las fechas disponibles
            }
        }, [seleccion]);

        // Filtrar los datos según la fecha seleccionada (si se está visualizando 'registros')
        useEffect(() => {
            if (seleccion === 'registros' && fechaSeleccionada) {
            // Establecer el rango de tiempo para el día completo
            const inicioFecha = `${fechaSeleccionada}T00:00:00`; // 00:00:00 de esa fecha
            const finFecha = `${fechaSeleccionada}T23:59:59`; // 23:59:59 de esa fecha

            // Hacer la consulta para obtener los registros filtrados por el rango de fecha y hora
            AxiosInstance.get(`obtener-fechas-filtradas/?fecha_inicio=${inicioFecha}&fecha_fin=${finFecha}`)
                .then(response => {
                setDatos(prevDatos => ({
                    ...prevDatos,
                    registros: response.data
                }));
                })
                .catch(error => {
                console.error('Error al obtener los registros filtrados:', error);
                });
            }
        }, [fechaSeleccionada, seleccion]);
    
      useEffect(() => {
        const currentData = datos[seleccion];
        if (currentData && currentData.length > 0) {
          const columnas = Object.keys(currentData[0]).map(key => ({
            field: key,
            headerName: key.charAt(0).toUpperCase() + key.slice(1),
            width: 150,
          }));
          setColumnasDinamicas(columnas);
        } else {
          setColumnasDinamicas([]);
        }
      }, [seleccion, datos]);
    
      return (
        <div style={{ padding: '2rem' }}>
          <Typography variant="h4">Dashboard de Consultas</Typography>
    
          <FormControl fullWidth style={{ marginTop: '1rem' }}>
            <InputLabel id="select-label">Selecciona una tabla</InputLabel>
            <Select
              labelId="select-label"
              value={seleccion}
              label="Selecciona una tabla"
              onChange={(e) => setSeleccion(e.target.value)}
            >
              <MenuItem value="vehiculos">Vehículos</MenuItem>
              <MenuItem value="usuarios">Usuarios</MenuItem>
              <MenuItem value="registros">Registros</MenuItem>
            </Select>
          </FormControl>
    
          {/* Mostrar el selector de fechas solo si se selecciona 'registros' */}
      {seleccion === 'registros' && (
        <FormControl fullWidth style={{ marginTop: '1rem' }}>
          <InputLabel id="fecha-label">Selecciona una fecha</InputLabel>
          <Select
            labelId="fecha-label"
            value={fechaSeleccionada}
            label="Selecciona una fecha"
            onChange={(e) => setFechaSeleccionada(e.target.value)}
          >
            {fechasDisponibles.map((fecha, index) => (
              <MenuItem key={index} value={fecha}>
                {fecha}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      )}

      {/* Mostrar la tabla de datos filtrados (por fecha si es registros) */}
      <TablaDatos datos={datos[seleccion]} columnas={columnasDinamicas} />
        </div>
      );
    };
    
export default Pagina2