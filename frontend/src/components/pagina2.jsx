import {React, useState, useEffect} from 'react'
import AxiosInstance from './Axios'



const Pagina2 = () => {

    const [registrosData, setMyregistrosData] = useState([])

    console.log("datos", registrosData)
    const GetData = () => {
        AxiosInstance.get(`registros/`)
        .then((res) => {
            setMyregistrosData(res.data)
        } )
    } 

    useEffect(() => {
        GetData()
    },[])
    return(
        <div>
            
        </div>
    )
}

export default Pagina2