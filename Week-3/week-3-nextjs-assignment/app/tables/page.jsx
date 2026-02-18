import AuthorTable from "@/components/ui/AuthorTable";
import Navbar from "@/components/ui/Navbar";
import ProjectsTable from "@/components/ui/ProjectsTable";

export default function Tables(){
    return (
        <div>
            <Navbar page="Tables"></Navbar>

            <div className="p-4">
                <AuthorTable></AuthorTable>
            </div>

            <div className="p-4">
                <ProjectsTable></ProjectsTable>
            </div>
        </div>
    )
}