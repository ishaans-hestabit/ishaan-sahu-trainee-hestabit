export default function ProjectRow({
    name,icon,budget,status,completion,
  }) {
  return (
    <div className="grid grid-cols-[2fr_1.5fr_1fr_1fr_0.5fr] items-center py-3.5 border-b border-gray-200 last:border-none">
      
      <div className="flex items-center gap-3">
        <img src={icon} alt={name} className="w-6 h-6" />
        <span className="text-sm font-medium text-gray-700">
          {name}
        </span>
      </div>

      <span className="text-sm text-gray-600">{budget}</span>

      <span className="text-sm text-gray-600">{status}</span>

      <div className="flex items-center gap-3">
        <span className="text-sm text-primary font-medium w-10">
          {completion}%
        </span>

        <div className="flex-1 bg-gray-200 h-1.5 rounded-full">
          <div
            className="bg-primary h-1.5 rounded-full"
            style={{ width: `${completion}%` }}
          ></div>
        </div>
      </div>

      <span className="text-gray-400 text-lg cursor-pointer text-center">⋮</span>

    </div>
  );
}