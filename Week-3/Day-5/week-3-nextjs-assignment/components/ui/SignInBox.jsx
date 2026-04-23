"use client"
export default function SignInBox() {
  return (
    <div className="max-w-87.5 w-full flex flex-col">

      <h1 className="text-primary text-4xl font-bold mb-2">Welcome Back</h1>

      <p className="text-gray-400 text-sm font-bold mb-10">
        Enter your email and password to sign in
      </p>

      <form className="flex flex-col gap-6" onSubmit={(e) => e.preventDefault()}>

        <div className="flex flex-col gap-2">
          <label className="text-sm font-bold text-slate-700 ml-1">Email</label>

          <input type="email" placeholder="Your email address" className="p-4 border border-gray-200 rounded-2xl text-sm outline-none focus:border-teal-400" />
        </div>

        <div className="flex flex-col gap-2">
          <label className="text-sm font-bold text-slate-700 ml-1">Password</label>
          <input type="password" placeholder="Your password" className="p-4 border border-gray-200 rounded-2xl text-sm outline-none focus:border-teal-400" />
        </div>

        <button className="w-full bg-primary text-white py-4 rounded-2xl text-[10px] font-bold uppercase tracking-widest shadow-lg shadow-teal-100 hover:shadow-teal-200">
          SIGN IN
        </button>
      </form>

      <p className="text-center mt-8 text-xs font-medium text-gray-400">
        Don't have an account? <span className="text-primary font-bold cursor-pointer hover:underline">Sign Up</span>
      </p>
    </div>
  );
}