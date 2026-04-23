import { CgProfile } from "react-icons/cg";
import { FiSearch, FiBell, FiSettings } from "react-icons/fi";

export default function Navbar({ page }) {
  return (
    <div className={`flex justify-between items-center px-8 py-5 w-full ${page === "Profile"? 'bg-primary' : ""} rounded-lg`}>
      
      <div>
            <p className={`${page === "Profile"? 'text-white': 'text-gray-400'} text-xs  mb-1`}>
                Pages / <span className={`${page === "Profile"? 'text-white':"text-gray-700"}`}>{page}</span>
            </p>
            <h1 className={`${page === "Profile"? 'text-white': " text-gray-800"} text-lg font-semibold`}>
                {page}
            </h1>
      </div>

      <div className="flex items-center gap-6">
        
            <div className="flex items-center bg-white border border-gray-200 rounded-full px-4 py-2">
              
            <FiSearch className="text-gray-400 text-sm mr-2" />
            <input    type="text"   placeholder="Type here..."   className="bg-transparent outline-none text-sm placeholder-gray-400 w-32"
            />
            </div>

            <button className={`${page === "Profile"? 'text-white':"text-gray-500"} flex items-center gap-2 text-sm  hover:text-gray-700 `}>

            <CgProfile className={` ${page === "Profile"? 'text-white':"text-gray-400"} text-base `} />
            Sign In
            </button>

            <FiSettings className={`${page === "Profile"? 'text-white': "text-gray-400"}  text-lg cursor-pointer hover:text-gray-600 `} />

            <FiBell className={`${page === "Profile"? 'text-white': "text-gray-400"} text-lg cursor-pointer hover:text-gray-600 `} />

      </div>
    </div>
  );
}