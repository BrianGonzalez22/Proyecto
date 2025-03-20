import { useState } from 'react'
import './App.css'
import {Routes, Route, Navigate} from 'react-router-dom'
import Pagina1 from './components/pagina1'
import Pagina2 from './components/pagina2'
import Pagina3 from './components/pagina3'
import Navbar from './components/Navbar'
import Login from './components/Login';
import Register from './components/register'


function App() {
  // Verificamos si existe un token (simulando autenticación)
  const isAuthenticated = !!localStorage.getItem('access');

  return (
    <>
      {isAuthenticated ? (
        <Navbar
          content={
            <Routes>
              <Route path="/" element={<Pagina1 />} />
              <Route path="/pagina2" element={<Pagina2 />} />
              <Route path="/pagina3" element={<Pagina3 />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          }
        />
      ) : (
        // Si no está autenticado, redirige al login
        <Routes>
          <Route path="/*" element={<Navigate to="/login" />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      )}
    </>
  );
}

export default App;