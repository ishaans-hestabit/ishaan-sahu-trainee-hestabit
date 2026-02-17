import { FaRegCircleQuestion } from "react-icons/fa6";
export default function SideBarHelp(){
    return (
        <div className="flex flex-col  w-54.5 h-47 bg-primary m-4 p-3 rounded-2xl gap-3">
            
            <div className="flex items-center justify-center w-10 h-10 bg-white rounded-lg ">
                <FaRegCircleQuestion 
                    className="text-primary text-xl" 
                    style={{ color: 'var(--color-primary)' }} 
                />
            </div>
            
            <div className="">
                <h1 className="text-white font-bold">Need Help?</h1>
                <p className="text-white">Please check our docs</p>
            </div>
            <button className="px-6 py-3 rounded-2xl bg-white font-light text-sm">DOCUMENTATION</button>
        </div>
    );
}