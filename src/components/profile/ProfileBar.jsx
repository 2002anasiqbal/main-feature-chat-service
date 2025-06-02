"use client";
import Link from "next/link";

const ProfileBar = ({
  profileImage = "/assets/profile/1.svg",
  name = "John Doe",
  email = "johndoe@example.com",
}) => {
  return (
    <div className="flex items-center justify-between py-4 bg-white w-full">
      {/* Profile Info */}
      <div className="flex items-center gap-4">
        <img
          src={profileImage}
          alt="Profile"
          className="w-20 h-20 rounded-full object-cover"
        />
        <div>
          <h3 className="text-lg text-gray-900 font-semibold">{name}</h3>
          <p className="text-gray-500 text-sm">{email}</p>
        </div>
      </div>

      {/* Edit Button */}
      <Link href="/routes/profile/form">
        <button className="px-4 py-2 bg-teal-500 text-white text-sm rounded-md hover:bg-teal-600 transition">
          Edit Profile
        </button>
      </Link>
    </div>
  );
};

export default ProfileBar;