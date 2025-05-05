import ProfileBar from "@/components/profile/ProfileBar";
import ProfileForm from "@/components/profile/ProfileForm";

export default function ProfileFormPage() {
    return (
      <div className="my-20 space-y-10">
        <ProfileBar />
        <ProfileForm />
      </div>
    );
  }