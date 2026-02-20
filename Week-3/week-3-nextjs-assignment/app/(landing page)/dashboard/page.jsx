import ActiveUsers from "@/components/ui/Dashboard/ActiveUsers";
import DashboardStats from "@/components/ui/Dashboard/DashboardStats";
import Navbar from "@/components/ui/Navbar";
import ProjectsTable from "@/components/ui/ProjectsTable/ProjectsTable";
import RocketsCard from "@/components/ui/Dashboard/RocketsCard";
import SalesOverview from "@/components/ui/Dashboard/SalesOverview";
import WelcomeCard from "@/components/ui/Dashboard/WelcomeCard";

export default function Dashboard(){
    return (
        <div >
            <Navbar page="Dashboard"/>

        {/* stats of website */}
            <DashboardStats />

            {/* welcome card dashboard */}
            <div className="grid grid-cols-[2fr_1.3fr] gap-6 auto-rows-[270px] p-6">
                <WelcomeCard/>
                <RocketsCard/>
            </div>


            {/* graph insights */}
            <div className="flex gap-3 p-6">
                <ActiveUsers/>
                <SalesOverview/>
            </div>

            {/* overviews */}
            <div className="flex gap-3 w-full p-6">
                <div className="flex-2">
                    <ProjectsTable />
                </div>
            </div>

        </div>
    )
}