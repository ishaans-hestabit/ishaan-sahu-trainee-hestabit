import { Plus } from "lucide-react";
import ProjectCard from "./ProjectCard";


export default function ProjectsSection() {
  const projects = [
    {
      id: 1,
      title: "Modern",
      description: "As Uber works through a huge amount of internal management turmoil.",
      image: "/projects/modern.jpg",
      avatars: ["/author_images/Image1.svg", "/author_images/Image2.svg", "/author_images/Image3.svg", "/author_images/Image4.svg"]
    },
    {
      id: 2,
      title: "Scandinavian",
      description: "Music is something that every person has his or her own specific opinion about.",
      image: "/projects/scandi.jpg",
      avatars: ["/author_images/Image2.svg", "/author_images/Image3.svg", "/author_images/Image1.svg", "/author_images/Image4.svg"]
    },
    {
      id: 3,
      title: "Minimalist",
      description: "Different people have different taste, and various types of music.",
      image: "/projects/minimal.jpg",
      avatars: ["/author_images/Image4.svg", "/author_images/Image1.svg", "/author_images/Image2.svg", "/author_images/Image3.svg"]
    }
  ];

  return (
    <div className="bg-white p-6 rounded-3xl border border-gray-100">
      
      <div className="mb-8">
        <h2 className="text-lg font-bold text-slate-800">Projects</h2>
        <p className="text-sm font-medium text-gray-400">Architects design houses</p>
      </div>

      
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        {projects.map((project) => (
          <ProjectCard key={project.id} {...project} />
        ))}

        
        <div className="flex flex-col items-center justify-center border-2 border-dashed border-gray-200 rounded-3xl p-8 hover:border-teal-400  cursor-pointer group min-h-80">

          <div className="p-3 rounded-full bg-gray-50 group-hover:bg-teal-50 mb-4">
             <Plus className="w-6 h-6 text-gray-400 group-hover:text-primary" />
          </div>

          <span className="text-lg font-bold text-gray-400 group-hover:text-slate-800">
            Create a New Project
          </span>
        </div>
      </div>
    </div>
  );
}