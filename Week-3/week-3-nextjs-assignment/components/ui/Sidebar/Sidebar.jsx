import Link from "next/link";
import SidebarItem from "./SidebarItem";
import { FaHome } from "react-icons/fa";
import { FaTableList } from "react-icons/fa6";
import { CgProfile } from "react-icons/cg";
import { FaMoneyBillAlt } from "react-icons/fa";
import { VscSignIn } from "react-icons/vsc";
import { SiGnuprivacyguard } from "react-icons/si";
import SideBarHelp from "./SideBarHelp";


export default function Sidebar(){

    // we are doing this so that we dont need ot update ui by hand everytime instead we can just add it here and they are gonna handle it like a automatically
    const MAIN_NAV = [
        { label: 'Dashboard', href: '/' ,icon:<FaHome color="white" />},
        { label: 'Tables', href: '/tables' ,icon : <FaTableList  color="white"/>},
        { label: 'Billing', href: '/billing' ,icon : <FaMoneyBillAlt color="white"/>
}
        ];
// seperated these so that wer can have seperation on concren between two types of functionality in sidebar
    const ACCOUNT_NAV = [
    { label: 'Profile', href: '/profile', icon : <CgProfile color="white"/>},
    { label: 'Sign In', href: '/signin', icon: <VscSignIn color="white"/>},
    { label: 'Sign Up', href: '/signup', icon:  <SiGnuprivacyguard color="white"/>}
    ];
    return(
        <div className="flex flex-col h-screen w-64 sticky top-0 bg-gray-100 ">

            <div className="mb-10">

            <div className="flex gap-3 p-6 font-bold text-black"> 
                <img className="" src="../logo-creative-tim-black.svg" alt="" />
                <h1 className="text-sm">PURITY UI DASHBOARD</h1>
            </div>

            <ul>
                {
                    MAIN_NAV.map((item)=>(
                        <li key={item.label}>
                        <SidebarItem label={item.label} href={item.href} icon={item.icon}></SidebarItem>
                        </li>
                    ))
                }
            </ul>

            <h2 className="p-4 pl-7 font-bold text-sm">ACCOUNT PAGES</h2>

            <ul>
                {
                    ACCOUNT_NAV.map((item)=>(
                        <li key={item.label}>
                        <SidebarItem label={item.label} href={item.href} icon={item.icon}></SidebarItem>
                        </li>
                    ))
                }
            </ul>
            </div>

            <SideBarHelp></SideBarHelp>
        </div>
    )
}