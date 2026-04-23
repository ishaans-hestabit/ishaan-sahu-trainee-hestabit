import Image from "next/image";
import Link from "next/link";

export default function AuthNavbar({ page }) {
  const isSignUp = page === "signup";

  const navLinks = [
    { name: "DASHBOARD", href: "/dashboard"  },
    { name: "PROFILE", href: "/dashboard/profile" },
    { name: "SIGN UP", href: "/signup" },
    { name: "SIGN IN", href: "/signin" },
  ];

  return (
    <nav className="absolute top-8 left-1/2 -translate-x-1/2 w-[90%] max-w-275 z-50">

      <div className={`flex items-center justify-between px-8 py-4 ${isSignUp ? "bg-transparent border-transparent" : "bg-white/80 backdrop-blur-md rounded-2xl border border-white/20 shadow-sm"}`}>

        <Link href="/" className="flex items-center gap-2">
           <div className={`w-6 h-6 rounded flex items-center justify-center ${isSignUp ? "brightness-0 invert" : ""}`}>
              <Image src="/logo-creative-tim-black.svg" width={20} height={20} alt="logo" />
           </div>
           <span className={`text-xs font-bold uppercase tracking-tight ${isSignUp ? "text-white" : "text-slate-800"}`}>
             Purity UI Dashboard
           </span>
        </Link>

        <div className="hidden lg:flex items-center gap-8">
          {navLinks.map((link) => (
            <Link key={link.name} href={link.href} className={`flex items-center gap-2 text-[10px] font-bold  ${isSignUp ? "text-white hover:text-white/80" : "text-slate-700 hover:text-primary"}`}>
                    {link.name}
            </Link>
          ))}
        </div>

        <Link  href="" className={`px-6 py-2.5 text-[10px] font-bold rounded-full uppercase ${isSignUp ? "bg-white text-slate-800 hover:bg-white/90" : "bg-slate-800 text-white hover:bg-slate-700 shadow-md shadow-slate-200"}`}>
          Free Download
        </Link>
      </div>
    </nav>
  );
}