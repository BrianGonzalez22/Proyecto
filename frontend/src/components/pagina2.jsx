import {React, useState, useEffect} from 'react'
import AxiosInstance from './Axios'
import MyChartBox from './graficos/BoxChart'
import GarageIcon from '@mui/icons-material/Garage';
import DirectionsCarFilledIcon from '@mui/icons-material/DirectionsCarFilled';
import PieRechart from './graficos/PieRechart';
import ElectricRickshawIcon from '@mui/icons-material/ElectricRickshaw';

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
            <MyChartBox
                icon1 = {<ElectricRickshawIcon/>}
                title1 = {"Capacidad Estacionamiento"}
                chart1 = { <PieRechart/>}

                icon2 = {<DirectionsCarFilledIcon/>}
                title2 = {"Lugares Disponibles"}
                chart2 = { <PieRechart/>}

                icon3 = {<DirectionsCarFilledIcon/>}
                title3 = {"Vehiculos estacionados"}
                chart3 = { <PieRechart/>}
            />
        </div>
    )
}

export default Pagina2