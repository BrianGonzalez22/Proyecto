import { useState, useEffect } from 'react'
import './App.css'
import {Routes, Route, Navigate, useNavigate} from 'react-router-dom'
import Pagina1 from './components/pagina1'
import Pagina2 from './components/pagina2'
import Pagina3 from './components/pagina3'
import Navbar from './components/Navbar'
import Login from './components/Login';
import Register from './components/register'


function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  // Verificar token en el inicio
  useEffect(() => {
    const token = localStorage.getItem('access');
    setIsAuthenticated(!!token);
  }, []);

  // Función para logout
  const handleLogout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    setIsAuthenticated(false);
    navigate('/login');
  };

  return (
    <>
      {isAuthenticated ? (
        <div style={{ display: 'flex' }}>
          <Navbar onLogout={handleLogout} />
          <div style={{ flexGrow: 1, padding: '70px' }}>
            <Routes>
              <Route path="/" element={<Pagina1 />} />
              <Route path="/pagina2" element={<Pagina2 />} />
              <Route path="/pagina3" element={<Pagina3 />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </div>
        </div>
      ) : (
        <Routes>
          <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/*" element={<Navigate to="/login" />} />
        </Routes>
      )}
    </>
  );
}

export default App;