'use client';

import React from 'react';
import { AreaChart,Area,XAxis,YAxis,CartesianGrid,Tooltip,ResponsiveContainer} from 'recharts';

const data = [
  { name: 'Jan', sales: 180, revenue: 500 },
  { name: 'Feb', sales: 220, revenue: 200 },
  { name: 'Mar', sales: 210, revenue: 160 },
  { name: 'Apr', sales: 340, revenue: 260 },
  { name: 'May', sales: 350, revenue: 210 },
  { name: 'Jun', sales: 460, revenue: 230 },
  { name: 'Jul', sales: 350, revenue: 200 },
  { name: 'Aug', sales: 300, revenue: 160 },
  { name: 'Sep', sales: 350, revenue: 110 },
  { name: 'Oct', sales: 220, revenue: 140 },
  { name: 'Nov', sales: 400, revenue: 170 },
  { name: 'Dec', sales: 430, revenue: 130 },
];

export default function SalesOverview() {
  return (
    <div className=" w-full bg-white p-6 rounded-2xl border border-gray-100 h-[400px]">
      
      <div className="mb-6">
        <h2 className="text-lg font-bold text-slate-800">Sales overview</h2>
        <p className="text-sm font-medium text-gray-400">
          <span className="text-green-500 font-bold">(+5) more</span> in 2021
        </p>
      </div>

      <div className="h-[250px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
            <defs>
              
              <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#4FD1C5" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#4FD1C5" stopOpacity={0} />
              </linearGradient>
              
              <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#2D3748" stopOpacity={0.2} />
                <stop offset="95%" stopColor="#2D3748" stopOpacity={0} />
              </linearGradient>
            </defs>
            
            <CartesianGrid  strokeDasharray="3 3"  vertical={false}  stroke="#E2E8F0"/>
            
            <XAxis  dataKey="name"  axisLine={false}  tickLine={false}  tick={{ fill: '#A0AEC0', fontSize: 12 }}  dy={10}/>
            
            <YAxis axisLine={false} tickLine={false} tick={{ fill: '#A0AEC0', fontSize: 12 }} ticks={[0, 100, 200, 300, 400, 500]}/>
            
            <Tooltip />

            <Area type="monotone" dataKey="sales" stroke="#4FD1C5" strokeWidth={3} fillOpacity={1} fill="url(#colorSales)"/>

            
            <Area type="monotone" dataKey="revenue" stroke="#2D3748" strokeWidth={3} fillOpacity={1} fill="url(#colorRevenue)"/>
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};