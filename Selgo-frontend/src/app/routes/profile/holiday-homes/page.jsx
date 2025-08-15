import ProfileHolidayHomes from "@/components/profile/ProfileHolidayHomes";
import HolidayHomes from "../../travel/holiday-homes/page";
import ProfileBar from "@/components/profile/ProfileBar";

export default function HolidayHomesPage() {
    return (
      <div className="my-10 space-y-10">
        <ProfileBar/>
        <ProfileHolidayHomes />
      </div>
    );
  }