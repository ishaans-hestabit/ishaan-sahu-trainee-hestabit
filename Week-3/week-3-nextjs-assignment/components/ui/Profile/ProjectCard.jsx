import Image from "next/image";

export default function ProjectCard ({ id, title, description, image }) { 
    return  (
  <div className="flex flex-col group cursor-pointer">
    
    <div className="relative w-full h-48 rounded-2xl overflow-hidden mb-4">
      <Image src={image} alt={title} fill className="object-cover scale-y-120" />
    </div>

   
    <span className="text-xs font-medium text-gray-400 mb-1">Project #{id}</span>

    <h3 className="text-lg font-bold text-slate-800 mb-2">{title}</h3>

    <p className="text-sm text-gray-400 font-medium mb-6 ">
      {description}
    </p>

    <div className="flex items-center justify-between mt-auto">
      <button className="px-8 py-2 rounded-xl border border-primary text-[10px] font-bold text-primary hover:bg-teal-50 uppercase">
        VIEW ALL
      </button>
      
    </div>
  </div>
)};