"use client"
import { FaFacebook, FaApple, FaGoogle } from "react-icons/fa";

export default function SignUpBox() {
  return (
    <div className="bg-white w-full max-w-112.5 rounded-3xl lg:px-12 lg:py-8 mt-20">
      <h2 className="text-lg font-bold text-slate-800 text-center mb-8">Register with</h2>
      
      <div className="flex justify-center gap-4 mb-10">
        {[FaFacebook, FaApple, FaGoogle].map((Icon, i) => (
          <button key={i} className="p-4 border border-gray-100 rounded-2xl hover:bg-gray-50">
            <Icon className="text-slate-800 text-xl" />
          </button>
        ))}
      </div>

      <div className="flex items-center gap-4 mb-10">
            <div className="h-px bg-gray-100 grow" />
            <span className="text-[10px] font-bold text-gray-300 uppercase">or</span>
            <div className="h-px bg-gray-100 grow" />
      </div>

      <form className="flex flex-col gap-5" onSubmit={(e) => e.preventDefault()}>

        <div className="flex flex-col gap-2">
          <label className="text-[12px] font-bold text-slate-700 ml-1">Name</label>
          <input type="text" placeholder="Your full name" className="p-4 border border-gray-200 rounded-2xl text-sm outline-none focus:border-primary" />
        </div>

        <div className="flex flex-col gap-2">
          <label className="text-[12px] font-bold text-slate-700 ml-1">Email</label>
          <input type="email" placeholder="Your email address" className="p-4 border border-gray-200 rounded-2xl text-sm outline-none focus:border-primary " />
        </div>

        <div className="flex flex-col gap-2">
          <label className="text-[12px] font-bold text-slate-700 ml-1">Password</label>
          <input type="password" placeholder="Your password" className="p-4 border border-gray-200 rounded-2xl text-sm outline-none focus:border-primary " />
        </div>


        <button className="w-full bg-primary text-white py-4 rounded-2xl text-[10px] font-bold">
          SIGN UP
        </button>
      </form>

      <p className="text-center mt-8 text-xs font-medium text-gray-400">
        Already have an account? <span className="text-primary font-bold cursor-pointer hover:underline">Sign In</span>
      </p>
    </div>
  );
}