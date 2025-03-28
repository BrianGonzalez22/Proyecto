import {React, useState, useEffect} from 'react'
import AxiosInstance from './Axios'
import MyChartBox from './graficos/BoxChart'
import GarageIcon from '@mui/icons-material/Garage';
import DirectionsCarFilledIcon from '@mui/icons-material/DirectionsCarFilled';
import PieChartComponent from './graficos/PieRechart';
import ElectricRickshawIcon from '@mui/icons-material/ElectricRickshaw';
import EstacionamientoChart from './graficos/graficoOcupacion';
import EstanciaPromedioChart from './graficos/graficoHoras';
import MyChartBox2 from './graficos/BoxChart2';
import HeatmapChart from './graficos/HeatMapChart';

const Pagina1 = () => {

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
                title1 = {"Ocupacion"}
                chart1 = { <PieChartComponent/>}

                icon2 = {<GarageIcon/>}
                title2 = {"Disponibilidad"}
                chart2 = { <EstacionamientoChart/>}

                icon3 = {<DirectionsCarFilledIcon/>}
                title3 = {"Estancia Promedio en minutos"}
                chart3 = { <EstanciaPromedioChart/>}
            />

            <MyChartBox2
                icon1 = {<ElectricRickshawIcon/>}
                title1 = {"Ocupacion"}
                chart1 = { <HeatmapChart/>}

                icon2 = {<GarageIcon/>}
                title2 = {"Disponibilidad"}
                chart2 = { <ElectricRickshawIcon/>}

            />
        </div>
    )
}

export default Pagina1