import React from 'react';
import { FaFacebook, FaTwitter, FaInstagram } from 'react-icons/fa';

export default function ProfileInformation() {
  const infoItems = [
    { label: 'Full Name:', value: 'Alec M. Thompson' },
    { label: 'Mobile:', value: '(44) 123 1234 123' },
    { label: 'Email:', value: 'alecthompson@mail.com' },
    { label: 'Location:', value: 'United States' },
  ];

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 h-full flex flex-col">
      
      <h2 className="text-lg font-bold text-slate-800 mb-4">
        Profile Information
      </h2>

      
      <p className="text-sm leading-relaxed text-gray-400 font-medium mb-8">
        Hi, I'm Alec Thompson, Decisions: If you can't decide, the answer is no. 
        If two equally difficult paths, choose the one more painful in the short 
        term (pain avoidance is creating an illusion of equality).
      </p>

      
      <div className="flex flex-col gap-5 grow">
        {infoItems.map((item, index) => (
          <div key={index} className="flex items-center gap-3">
            <span className="text-sm font-bold text-slate-700 min-w-20">
              {item.label}
            </span>
            <span className="text-sm font-medium text-gray-400">
              {item.value}
            </span>
          </div>
        ))}

        
        <div className="flex items-center gap-3 mt-2">
          <span className="text-sm font-bold text-slate-700 min-w-20">
            Social Media:
          </span>
          <div className="flex items-center gap-4 text-primary">
            <a href="#" className="hover:scale-110 ">
              <FaFacebook size={16} />
            </a>
            <a href="#" className="hover:scale-110 ">
              <FaTwitter size={16} />
            </a>
            <a href="#" className="hover:scale-110 ">
              <FaInstagram size={16} />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}