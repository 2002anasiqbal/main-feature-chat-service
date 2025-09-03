import JobUniverseSection from "@/components/profile/JobUniverseSection";
import ProfileBar from "@/components/profile/ProfileBar";

export default function MyAccountsPage() {
    return (
      <div className="my-20 space-y-10">
        <ProfileBar/>
        <JobUniverseSection/>
      </div>
    );
  }