export default function StatsCard({
    title,value,change,icon
    }) {

        const isNegative = change.trim().startsWith('-');
  return (

    <div className="bg-card-bg rounded-2xl px-5 py-4 shadow-sm flex items-center justify-between">
      
      <div>
        <p className="text-xs text-gray-400 mb-1">
          {title}
        </p>

        <div className="flex items-center gap-2">
          <span className="text-lg font-semibold text-gray-800">
            {value}
          </span>

          <span
            className={`text-xs font-medium 
                ${ isNegative ? "text-red-500" : "text-green-500"}`}>
            {change}
          </span>
        </div>
      </div>

      <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-primary ">
        {icon}
      </div>
    </div>
  );
}
