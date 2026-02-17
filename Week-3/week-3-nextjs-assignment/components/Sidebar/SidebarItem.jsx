"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function SidebarItem({ label, href, icon }) {
  const pathname = usePathname();
  const isActive = pathname === href;

  return (
    <Link href={href}
    
        className={`flex gap-3 p-4 rounded-2xl mx-4 my-2 items-center transition ${isActive ? "bg-white border border-gray-200 shadow-sm" : "hover:bg-gray-200"}
        `} >
        <div className={`p-2 rounded-lg bg-primary `}>
                {icon}
        </div>

        <span className="text-sm text-black">{label}</span>
    </Link>
  );
}