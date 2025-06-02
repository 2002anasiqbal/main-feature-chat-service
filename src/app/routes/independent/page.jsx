import ButtonCard from "@/components/general/ButtonCard";
import CalendarComponent from "@/components/general/CalendarComponent";
import ContactUs from "@/components/general/ContactUs";
import FAQ from "@/components/general/FAQ";
import MapAdCard from "@/components/general/MapAdCard";
import ProductMoreDeatils from "@/components/general/ProductMoreDetails";
import RecentlyVisitedSlider from "@/components/general/RecentlyVisitedSlider";
import TwoButtonComponent from "@/components/general/TwoButtonCompoent";
import OnlineCarCard from "@/components/online-car/OnlineCarCard";
import FindingsList from "@/components/profile/FindingLists";
import FixedFinished from "@/components/profile/FixedFinished";
import JobUniverseSection from "@/components/profile/JobUniverseSection";
import MyAds from "@/components/profile/MyAds";
import NotificationSettings from "@/components/profile/NotificationSettings";
import PaymentsSection from "@/components/profile/PaymentSection";
import PrivacySettings from "@/components/profile/PrivacySettings";
import ProfileBar from "@/components/profile/ProfileBar";
import ProfileCards from "@/components/profile/ProfileCards";
import ProfileForm from "@/components/profile/ProfileForm";
import SecuritySettings from "@/components/profile/SecuritySettings";
import ContactCard from "@/components/property/ContactCard";
import PropertySlider from "@/components/property/PropertySlider";
import HolidayHomes from "../travel/holiday-homes/page";
import ProfileHolidayHomes from "@/components/profile/ProfileHolidayHomes";
import SavedSearches from "@/components/profile/SavedSearches";
import BusinessProfileComponent from "@/components/profile/BusinessProfileComponent";
import AdvertisementReviews from "@/components/profile/AdvertisementReviews";
import JobSearchForm from "@/components/profile/JobSearchForm";
import CompaniesIFollow from "@/components/profile/CompaniesIFollow";
import JobPreferences from "@/components/profile/JobPrefrences";
import Alris from "@/components/profile/alris";

const mockFindings = [
  { title: "My Findings", ads: 2 },
  { title: "Favorite Items", ads: 5 },
  { title: "Recently Viewed", ads: 3 },
];

const securityData = {
  title: "Security",
  description:
    "Did you know that you can secure your account even more? On this page you will find various security measures that can be used for a safe and secure experience at FINN.",
  buttonText: "Bank id +",
  items: [
    {
      title: "Two-step authentication",
      description: "Authentication app. You will receive a code from your security app.",
      status: "Not activated",
      buttonText: "Activate",
    },
    {
      title: "SMS code",
      description: "We will send a code to your phone number.",
      status: "Not activated",
      buttonText: "Activate",
    },
    {
      title: "Devices you are logged in to",
      description: "Windows 10\nChrome",
      status: "Active",
      buttonText: "Active Now",
    },
  ],
};

const mockSearches = [
  { title: "Apartments in Oslo" },
  { title: "Electric Cars" },
  { title: "Remote Jobs" },
];

const followedCompanies = [
  "Alert Health AS",
  "Dedicated Nurse",
  "Tech Solutions Inc.",
  "Finance Pro Group",
];

export default function Independent() {
  return (
    <div className="bg-white py-20">
      <ProductMoreDeatils />
      <div className="my-20">
        <ContactUs />
      </div>
      <div className="flex justify-center my-10">
        <MapAdCard />
      </div>
      <div className="flex justify-center my-10">
        <CalendarComponent />
      </div>
      <div className="flex justify-center my-10">
        <FAQ />
      </div>
      <div className="flex justify-center my-10">
        <OnlineCarCard />
      </div>
      <div className="flex justify-center my-10">
        <TwoButtonComponent />
      </div>
      <div className="flex justify-center my-10">
        <PropertySlider />
      </div>
      <div className="flex justify-center my-10">
        <ContactCard />
      </div>
      <div className="flex justify-center my-10">
        <ButtonCard />
      </div>
      <div className="flex justify-center my-10">
        <RecentlyVisitedSlider />
      </div>
      <div className="flex justify-center my-10">
        <ProfileBar />
      </div>
      <div className="flex justify-center my-10">
        <ProfileCards />
      </div>

      <div className="flex justify-center my-10">
        <ProfileForm />
      </div>
      <div className="flex justify-center my-10">
        <MyAds />
      </div>
      <div className="">
        <FindingsList findings={mockFindings} />
      </div>
      <div className="">
        <FixedFinished />
      </div>
      <div className="">
        <SecuritySettings {...securityData} />
      </div>
      <div className="">
        <PaymentsSection />
      </div>
      <div className="">
        <JobUniverseSection />
      </div>
      <div className="">
        <PrivacySettings />
      </div>
      <div className="">
        <NotificationSettings />
      </div>
      <div className="">
        <ProfileHolidayHomes />
      </div>
      <div className="">
        <SavedSearches searches={mockSearches} />;
      </div>
      <div className="">
        <BusinessProfileComponent />;
      </div>
      <div className="">
        <AdvertisementReviews />;
      </div>
      <div className="">
        <JobSearchForm />;
      </div>
      <div className="">
        <CompaniesIFollow companies={followedCompanies} />
      </div>
      <div className="">
        <JobPreferences />
      </div>
      <div className="">
        <Alris />
      </div>

    </div>
  );
}