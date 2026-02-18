import ProjectRow from "./ProjectRow";
import { PROJECTS } from '../../app/tables/dummy_data2.js';

export default function ProjectsTable() {
  return (
    <div className="bg-white rounded-2xl shadow-sm px-6 py-5">
      
      <h2 className="text-lg font-semibold">Projects</h2>
      <p className="text-sm text-gray-400 mb-5">
        <span className="text-green-500 font-medium">30 done</span> this month
      </p>

      <div className="grid grid-cols-[2fr_1.5fr_1fr_1fr_0.5fr] text-xs text-gray-400 uppercase pb-3 border-b border-gray-400">
        <span className="pl-1">Companies</span>
        <span>Budget</span>
        <span>Status</span>
        <span>Completion</span>
        <span></span>
      </div>

      <div>
        {PROJECTS.map((project, index) => (
          <ProjectRow key={index} {...project} />
        ))}
      </div>

    </div>
  );
}