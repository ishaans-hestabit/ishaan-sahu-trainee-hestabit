import { CgProfile } from "react-icons/cg";
import { FiSearch, FiBell, FiSettings } from "react-icons/fi";

export default function Navbar({ page }) {
  return (
    <div className="flex justify-between items-center px-8 py-5 w-full">
      
      <div>
            <p className="text-xs text-gray-400 mb-1">
                Pages / <span className="text-gray-700">{page}</span>
            </p>
            <h1 className="text-lg font-semibold text-gray-800">
                {page}
            </h1>
      </div>

      <div className="flex items-center gap-6">
        
            <div className="flex items-center bg-white border border-gray-200 rounded-full px-4 py-2">
            <FiSearch className="text-gray-400 text-sm mr-2" />
            <input    type="text"   placeholder="Type here..."   className="bg-transparent outline-none text-sm placeholder-gray-400 w-32"
            />
            </div>

            <button className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 ">
            <CgProfile className="text-base text-gray-400" />
            Sign In
            </button>

            <FiSettings className="text-gray-400 text-lg cursor-pointer hover:text-gray-600 " />

            <FiBell className="text-gray-400 text-lg cursor-pointer hover:text-gray-600 " />

      </div>
    </div>
  );
}