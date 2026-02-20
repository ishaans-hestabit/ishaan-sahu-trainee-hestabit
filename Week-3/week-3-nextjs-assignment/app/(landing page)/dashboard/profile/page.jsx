import Conversations from "@/components/ui/Profile/Conversations";
import Navbar from "@/components/ui/Navbar";
import PlatformSettings from "@/components/ui/Profile/PlatformSettings";
import ProfileHeader from "@/components/ui/Profile/ProfileHeader";
import ProfileInformation from "@/components/ui/Profile/ProfileInformation";
import ProjectsSection from "@/components/ui/Profile/ProjectsSection";

export default function Profile() {
  return (
    <div className="p-3 bg-gray-50 min-h-screen">
      
      <div className="relative h-65 w-full bg-primary mt-5 rounded-3xl overflow-visible p-6">
        
        <Navbar page="Profile" />

        <div className="absolute left-0 right-0 -bottom-16 px-6">
           <ProfileHeader />
        </div>
      </div>

      {/*  the header is absolute, we need a div to push the rest of the content down */}
      <div className="mt-24 px-6">
      </div>
    
        <div className="flex gap-4 p-3 items-stretch">
            <div className="flex-1">
                <PlatformSettings/>
            </div>
            <div className="flex-1">
                <ProfileInformation/>
            </div>
            <div className="flex-1">
                <Conversations/>
            </div>
      </div>

      <ProjectsSection/>
    </div>
  );
}