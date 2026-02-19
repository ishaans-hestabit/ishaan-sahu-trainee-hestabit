'use client';

import React from 'react';
import { FaBell, FaHtml5, FaShoppingCart, FaCreditCard, FaDropbox } from 'react-icons/fa';
import { SiAdobecreativecloud } from 'react-icons/si';

const orders = [
  {
    id: 1,
    title: '$2400, Design changes',
    date: '22 DEC 7:20 PM',
    icon: <FaBell className="text-teal-400" />,
    color: 'border-teal-400',
  },
  {
    id: 2,
    title: 'New order #4219423',
    date: '21 DEC 11:21 PM',
    icon: <FaHtml5 className="text-red-500" />,
    color: 'border-red-500',
  },
  {
    id: 3,
    title: 'Server Payments for April',
    date: '21 DEC 9:28 PM',
    icon: <FaShoppingCart className="text-blue-400" />,
    color: 'border-blue-400',
  },
  {
    id: 4,
    title: 'New card added for order #3210145',
    date: '20 DEC 3:52 PM',
    icon: <FaCreditCard className="text-orange-400" />,
    color: 'border-orange-400',
  },
  {
    id: 5,
    title: 'Unlock packages for Development',
    date: '19 DEC 11:35 PM',
    icon: <FaDropbox className="text-purple-500" />,
    color: 'border-purple-500',
  },
  {
    id: 6,
    title: 'New order #9851258',
    date: '18 DEC 4:41 PM',
    icon: <SiAdobecreativecloud className="text-pink-600" />,
    color: 'border-pink-600',
    isLast: true,
  },
];

export default function OrdersOverview (){
  return (
    <div className="bg-white p-6 rounded-2xl border border-gray-100 h-full basis-1/3 pb-11 shadow-sm" >
      
      <div className="mb-8">
        <h2 className="text-lg font-bold text-slate-800">Orders overview</h2>
        <p className="text-sm font-medium text-gray-400">
          <span className="text-green-500 font-bold">+30%</span> this month
        </p>
      </div>

      <div className="flex flex-col">
        {orders.map((order, index) => (
          <div key={order.id} className="relative flex gap-4 pb-6">
            
            {!order.isLast && (
              <div className="absolute left-[11px] top-6 w-[2px] h-full bg-gray-100" />
            )}

            
            <div className="relative z-10 flex items-center justify-center min-w-[24px] h-[24px] mt-1">
              {order.icon}
            </div>

            
            <div className="flex flex-col">
              <h4 className="text-sm font-bold text-slate-700">
                {order.title}
              </h4>
              <p className="text-xs font-bold text-gray-400 mt-1">
                {order.date}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
