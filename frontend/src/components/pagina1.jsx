import React, { useState, useEffect } from 'react'
import AxiosInstance from './axios'  // Importamos la instancia personalizada de axios

const Pagina1 = () => {
  // Estados para guardar los datos de entradas y salidas
  const [entradas, setEntradas] = useState(0)
  const [salidas, setSalidas] = useState(0)

  // useEffect para hacer la solicitud inicial cuando el componente se monta
  useEffect(() => {
    // Función para obtener los datos de la API
    const fetchData = () => {
      AxiosInstance.get('registros/contar_registros/')
        .then((response) => {
          setEntradas(response.data.total_entradas)
          setSalidas(response.data.total_salidas)
        })
        .catch((error) => {
          console.error('Error al obtener los datos:', error)
        })
    }

    // Llamamos a la función inmediatamente al cargar el componente
    fetchData()

    // Configuramos un intervalo para actualizar cada 5 segundos (5000 ms)
    const intervalId = setInterval(fetchData, 30000)

    // Limpiar el intervalo cuando el componente se desmonte
    return () => clearInterval(intervalId)
  }, [])  // Solo se ejecuta una vez cuando se monta el componente

  return (
    <div>
      <h2>📊 Contabilización de Registros</h2>
      <p>Entradas: {entradas}</p>
      <p>Salidas: {salidas}</p>
    </div>
  )
}

export default Pagina1
