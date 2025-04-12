import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';  // Importa useNavigate

const Login = ({ setIsAuthenticated }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
  
    const handleLogin = async (e) => {
      e.preventDefault();
      try {
        const response = await axios.post('http://localhost:8000/login/', {
          username,
          password
        });
  
        
        localStorage.setItem('access', response.data.access);
        localStorage.setItem('refresh', response.data.refresh);
  
        setIsAuthenticated(true); // Actualiza el estado
        alert('Login exitoso');
        navigate('/'); // Redirige al dashboard
      } catch (error) {
        alert('Error en el login. Verifique sus credenciales.');
      }
    };
  
    return (
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Usuario"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Iniciar Sesión</button>
      </form>
    );
  };
  
  export default Login;
