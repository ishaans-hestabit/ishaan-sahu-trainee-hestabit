
'use client'; 
import React from 'react';
import { BarChart,Bar,XAxis,YAxis,CartesianGrid,ResponsiveContainer,} from 'recharts';
import { FaWallet, FaRocket, FaShoppingCart, FaWrench } from 'react-icons/fa';

// Mock data for the chart to make it "real"
const chartData = [
  { name: 'Page A', value: 330 },
  { name: 'Page B', value: 250 },
  { name: 'Page C', value: 110 },
  { name: 'Page D', value: 300 },
  { name: 'Page E', value: 490 },
  { name: 'Page F', value: 390 },
  { name: 'Page G', value: 480 },
  { name: 'Page H', value: 280 },
  { name: 'Page I', value: 190 },
];

// Mock data for the bottom stats section
const statsData = [
  {
    icon: <FaWallet className="text-white" size={14} />,
    label: 'Users',
    value: '32,984',
    progress: 60, // Percentage for the bar beneath
  },
  {
    icon: <FaRocket className="text-white" size={14} />,
    label: 'Clicks',
    value: '2,42m',
    progress: 80,
  },
  {
    icon: <FaShoppingCart className="text-white" size={14} />,
    label: 'Sales',
    value: '2,400$',
    progress: 35,
  },
  {
    icon: <FaWrench className="text-white" size={14} />,
    label: 'Items',
    value: '320',
    progress: 50,
  },
];

export default function ActiveUsers() {
  return (
    <div className="flex flex-col bg-white p-6 rounded-2xl w-full h-100">
      
      <div className="w-full rounded-xl overflow-hidden relative h-55 p-4"
        
        style={{ backgroundColor: '#2D375F' }}>

        <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{  top: 30,  right: 20,  left: -20,  bottom: 10, }}>

                <CartesianGrid strokeDasharray="3 3" vertical={false} horizontal={false} />
                <XAxis dataKey="name" hide={true} />
                <YAxis  axisLine={false}   tick={{ fill: '#ffffff', fontSize: 12, fontWeight: 500 }}   ticks={[0, 100, 200, 300, 400, 500]} />
                <Bar  dataKey="value"  fill="#ffffff"  barSize={6} radius={[10, 10, 10, 10]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-6 mb-8">
        <h2 className="text-xl font-bold text-gray-800">Active Users</h2>
        <p className="text-sm text-gray-500 font-medium">
          <span className="text-green-400 font-bold">(+23)</span> than last week
        </p>
      </div>


      <div className="grid grid-cols-4 gap-6">

        {statsData.map((stat, index) => (
          <div key={index} className="flex flex-col">
            
            <div className="flex items-center gap-3 mb-2">
                <div className="p-2 bg-primary rounded-xl shadow-sm">
                    {stat.icon}
                </div>
                <span className="text-sm text-gray-400 font-medium">
                    {stat.label}
                </span>
            </div>

            <h3 className="text-xl font-bold text-gray-800 mb-3">
              {stat.value}
            </h3>

            <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div className="h-full bg-primary rounded-full" style={{ width: `${stat.progress}%` }}></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

