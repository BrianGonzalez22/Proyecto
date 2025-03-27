import React, { PureComponent } from 'react';
import { Radar, RadarChart, PolarGrid, Legend, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';

const data = [
  {
    subject: 'Lunes',
    A: 120,
    B: 110,
    fullMark: 150,
  },
  {
    subject: 'Martes',
    A: 98,
    B: 130,
    fullMark: 150,
  },
  {
    subject: 'Miercoles',
    A: 86,
    B: 130,
    fullMark: 150,
  },
  {
    subject: 'Jueves',
    A: 99,
    B: 100,
    fullMark: 150,
  },
  {
    subject: 'Viernes',
    A: 85,
    B: 90,
    fullMark: 150,
  },
  {
    subject: 'Sabado',
    A: 65,
    B: 85,
    fullMark: 150,
  },
];

export default class Example extends PureComponent {
  static demoUrl = 'https://codesandbox.io/p/sandbox/radar-chart-specified-domain-l68xry';

  render() {
    return (
        <div style={{ width: '100%', height: '400px' }}>
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={30} domain={[0, 150]} />
          <Radar name="Alumnos" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
          <Radar name="Doc/Adm" dataKey="B" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
          <Radar name="Motos" dataKey="B" stroke="#e36868" fill="#e36868" fillOpacity={0.6} />
          <Legend />
        </RadarChart>
      </ResponsiveContainer>
      </div>
    );
  }
}
