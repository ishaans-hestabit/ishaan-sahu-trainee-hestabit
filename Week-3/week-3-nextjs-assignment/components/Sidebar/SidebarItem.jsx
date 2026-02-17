import Link from "next/link";

export default function SidebarItem({ label, href, icon }) {
    return (

        <Link className=" flex gap-3 p-4  rounded-2xl mx-4 my-2 items-center hover:bg-gray-200" href={href}>
            <div className="bg-primary p-2 rounded-lg">{icon}</div>
            <span className="text-sm">{label}</span>
        </Link>

    )
}