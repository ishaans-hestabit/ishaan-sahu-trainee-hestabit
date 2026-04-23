"use client"
import './globals.css'

import AuthNavbar from "@/components/ui/AuthNavBar";

export default function Home() {
  return (
    <div className="min-h-screen bg-white flex flex-col">
      
      <AuthNavbar/>

      
      <main className="grow flex flex-col items-center justify-center px-6 text-center">
        <div className="space-y-4 mb-12">
          <h1 className="text-5xl md:text-8xl font-primary uppercase text-primary">
            The Dashboard.
          </h1>
          
        </div>

        
        <button onClick={() => window.location.href = '/dashboard'}
          className="px-12 py-5 bg-primary rounded-3xl text-white text-sm font-bold uppercase  hover:bg-teal-500">
          Enter Workspace
        </button>

      </main>
    </div>
  );
}
