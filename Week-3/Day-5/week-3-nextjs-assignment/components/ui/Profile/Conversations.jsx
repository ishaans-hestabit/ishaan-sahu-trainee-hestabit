import Image from "next/image";

const conversations = [
  {
    id: 1,
    name: "Esthera Jackson",
    message: "Hi! I need more informations...",
    image: "/author_images/Image6.svg", 
  },
  {
    id: 2,
    name: "Esthera Jackson",
    message: "Awesome work, can you change...",
    image: "/author_images/Image1.svg",
  },
  {
    id: 3,
    name: "Esthera Jackson",
    message: "Have a great afternoon...",
    image: "/author_images/Image2.svg",
  },
  {
    id: 4,
    name: "Esthera Jackson",
    message: "About files I can...",
    image: "/author_images/Image3.svg",
  },
];

export default function Conversations() {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 h-full">
      <h2 className="text-lg font-bold text-slate-800 mb-6">Conversations</h2>
      
      <div className="flex flex-col gap-6">
        
        {conversations.map((conv) => (
          <div key={conv.id} className="flex items-center justify-between group">
                <div className="flex items-center gap-4">
                
                <div className="relative w-12 h-12 rounded-xl overflow-hidden ">
                    <Image src={conv.image} alt={conv.name} fill className="object-cover"/>
                </div>

              
              <div className="flex flex-col">
                    <span className="text-sm font-bold text-slate-700">
                        {conv.name}
                    </span>
                <span className="text-xs font-medium text-gray-400">
                  {conv.message}
                </span>
              </div>
            </div>

            
            <button className="text-[10px] font-bold text-primary hover:text-teal-500 transition-colors uppercase tracking-wider">
              REPLY
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}