import Image from "next/image";
import { HiCube, HiUserGroup, HiWrench, HiPencil } from "react-icons/hi2";

export default function ProfileHeader() {
  return (
    <div className="w-full bg-white/80 backdrop-blur-md border border-white/20 rounded-[20px] px-4 py-3 flex flex-col md:flex-row items-center justify-between shadow-sm">
      
      
      <div className="flex items-center gap-4">
            <div className="relative">
            
            <div className="w-20 h-20 rounded-2xl overflow-hidden relative shadow-md">
                <Image  src="/author_images/Image6.svg"  alt="Esthera Jackson"  fill className="object-cover"/>
            </div>
          
            <button className="absolute -bottom-1 -right-1 bg-white p-1.5 rounded-lg shadow-md border border-gray-100 hover:scale-105 transition-all">
                <HiPencil className="text-primary w-4 h-4" />
            </button>
        </div>

        
        <div className="flex flex-col">
            <h2 className="text-lg font-bold text-slate-700 leading-tight">
                Esthera Jackson
            </h2>
            <p className="text-sm font-semibold text-gray-400">
                esthera@simmmple.com
            </p>
        </div>
      </div>

      
      <div className="flex items-center gap-1 mt-6 md:mt-0 p-1 rounded-2xl bg-gray-50/50">
        
        
        <button className="flex items-center gap-2 px-6 py-2.5 bg-white shadow-sm rounded-xl text-[10px] font-bold text-slate-700 transition-all border border-transparent hover:border-gray-100">
          <HiCube className="w-3.5 h-3.5" />
          OVERVIEW
        </button>
        
        <button className="flex items-center gap-2 px-6 py-2.5 rounded-xl text-[10px] font-bold text-slate-500 hover:bg-white/60 transition-all">
          <HiUserGroup className="w-3.5 h-3.5" />
          TEAMS
        </button>
        
        <button className="flex items-center gap-2 px-6 py-2.5 rounded-xl text-[10px] font-bold text-slate-500 hover:bg-white/60 transition-all">
          <HiWrench className="w-3.5 h-3.5" />
          PROJECTS
        </button>
        
      </div>
    </div>
  );
}