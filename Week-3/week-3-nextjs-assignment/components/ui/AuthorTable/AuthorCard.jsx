export default function AuthorCard({
    img,name,email,position,heirarchy,status,date_of_employment,
  }) {
  const isOnline = status === "online";

  return (
    <div className="grid grid-cols-[2fr_1.5fr_1fr_1fr_0.5fr] justify-between items-center py-2 border-b border-gray-200 last:border-none">
      
      <div className="flex gap-3">
        <img src={img} alt={name} className="w-10 h-10 rounded-xl object-cover"/>

            <div>
            <h2 className="text-sm font-semibold text-gray-800">{name}</h2>
            <h3 className="text-xs text-gray-400">{email}</h3>
            </div>
      </div>

      <div className="">
        <h1 className="text-sm font-semibold text-gray-700">{position}</h1>
        <h2 className="text-xs text-gray-400">{heirarchy}</h2>
      </div>

      <div className="">
        <span className={`text-xs px-3 py-1 rounded-full font-medium ${isOnline ? "bg-green-100 text-green-600": "bg-gray-100 text-gray-400"}`}>
          {isOnline ? "Online" : "Offline"}
        </span>
      </div>

      <div className="text-sm text-gray-600">
        {date_of_employment}
      </div>

      <div className="text-sm text-gray-400 cursor-pointer hover:text-gray-600">
        Edit
      </div>
    </div>
  );
}