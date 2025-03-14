import { useState } from 'react'
import './App.css'
import {Routes, Route} from 'react-router-dom'
import Pagina1 from './components/pagina1'
import Pagina2 from './components/pagina2'
import Pagina3 from './components/pagina3'
import Navbar from './components/Navbar'
import { AuthProvider} from './AuthContent'
import AuthContext from './AuthContent'
import { useContext } from 'react'


function App() {
    const [count, setCount] = useState(0)
    return (
    <>
      <Navbar
          content={
              <Routes>
                  <Route path="/" element={<Pagina1 />} />
                  <Route path="/pagina2" element={<Pagina2 />} />
                  <Route path="/pagina3" element={<Pagina3 />} />
              </Routes>
          }
      />
    </>
  )
}

export default App;
