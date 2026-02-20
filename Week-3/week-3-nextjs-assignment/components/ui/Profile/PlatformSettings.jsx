'use client';

import React, { useState } from 'react';

export default function PlatformSettings() {
  const [settings, setSettings] = useState({
    follows: true,
    answers: false,
    mentions: true,
    launches: false,
    updates: false,
    newsletter: true,
  });

  const handleToggle = (key) => {
    setSettings((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const ToggleItem = ({ label, stateKey }) => (
    <div className="flex items-center gap-4 group cursor-pointer" onClick={() => handleToggle(stateKey)}>
      
        <div className={`w-10 h-5 flex items-center rounded-full p-1 transition-colors duration-300 ease-in-out ${ settings[stateKey] ? 'bg-primary' : 'bg-gray-200' }`}>
            <div className={`bg-white w-3.5 h-3.5 rounded-full shadow-md transform transition-transform duration-300 ease-in-out ${settings[stateKey] ? 'translate-x-5' : 'translate-x-0' }`} />
      </div>
      <span className="text-sm font-medium text-gray-400 group-hover:text-gray-600 transition-colors">
        {label}
      </span>
    </div>
  );

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 h-full flex flex-col">
      <h2 className="text-lg font-bold text-slate-800 mb-6">Platform Settings</h2>

      
      <div className="mb-8">
        <h3 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-6">
          Account
        </h3>
        <div className="flex flex-col gap-5">
          <ToggleItem label="Email me when someone follows me" stateKey="follows" />
          <ToggleItem label="Email me when someone answers on my post" stateKey="answers" />
          <ToggleItem label="Email me when someone mentions me" stateKey="mentions" />
        </div>
      </div>

      <div>
        <h3 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-6">
          Application
        </h3>
        <div className="flex flex-col gap-5">
          <ToggleItem label="New launches and projects" stateKey="launches" />
          <ToggleItem label="Monthly product updates" stateKey="updates" />
          <ToggleItem label="Subscribe to newsletter" stateKey="newsletter" />
        </div>
      </div>
    </div>
  );
};

