"use client";
import { useState, useEffect } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import useAuthStore from "@/store/store";
import { FaUserCircle } from "react-icons/fa";
// import { HiLanguage } from "react-icons/io5";
// import { CiMenuFries } from "react-icons/gi";

import { CiCirclePlus, CiBellOn, CiUser, CiChat1, CiMenuFries} from "react-icons/ci";
import { HiLanguage } from "react-icons/hi2";

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isLangMenuOpen, setIsLangMenuOpen] = useState(false);

  // Using global store to manage auth
  const { user, isAuthenticated, logout } = useAuthStore();
  const router = useRouter();

  // For demo, static counts. Replace with real data if needed.
  const [notifications, setNotifications] = useState(2);
  const [messages, setMessages] = useState(3);

  // Close burger menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (isMenuOpen && !event.target.closest("#menu")) {
        setIsMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isMenuOpen]);

  // Close language menu when clicking outside (handles both mobile and desktop)
  useEffect(() => {
    const handleClickOutsideLang = (event) => {
      if (isLangMenuOpen) {
        if (
          !event.target.closest("#lang-menu") &&
          !event.target.closest("#lang-menu-desktop") &&
          !event.target.closest("#lang-button") &&
          !event.target.closest("#lang-button-desktop")
        ) {
          setIsLangMenuOpen(false);
        }
      }
    };
    document.addEventListener("mousedown", handleClickOutsideLang);
    return () => {
      document.removeEventListener("mousedown", handleClickOutsideLang);
    };
  }, [isLangMenuOpen]);

  // Define your nav items
  const menuItems = [
    { name: "Travel", icon: "airplane-take-off-01.svg", href: "/routes/travel" },
    { name: "Jobs", icon: "job-search.svg", href: "/routes/jobs" },
    { name: "Property", icon: "home-09.svg", href: "/routes/property" },
<<<<<<< HEAD
    { name: "Motorcycles", icon: "motorbike-02.svg", href: "/routes/motor-cycle" },
    { name: "Boat", icon: "boat.svg", href: "/routes/boat" },
    { name: "Furniture", icon: "furniture.svg", href: "/routes/the-square" },
    { name: "Fridge", icon: "fridge.svg", href: "/routes/nu-electronics" },
=======
    { name: "Cars", icon: "car-02.svg", href: "/routes/cars" },
    { name: "Motorcycles", icon: "motorbike-02.svg", href: "/routes/motor-cycle" },
    { name: "Boat", icon: "boat.svg", href: "/routes/boat" },
    { name: "Square", icon: "shape-square.svg", href: "/routes/square" },
>>>>>>> ef864b3 (Replace Features branch with selgo-feature contents)
    { name: "Agreements", icon: "agreement-02.svg", href: "/routes/my-tender" },
    { name: "Smart Devices", icon: "bot.svg", href: "/routes/nu-electronics" },
  ];

  // Handle Logout
  const handleLogout = async () => {
    await logout();
    router.push("/"); // Redirect wherever you'd like after logout
  };

  // Handle Profile Navigation
  const handleProfileClick = () => {
    router.push("/routes/profile");
  };

  // Handle Language Change (stub for now)
  const handleLanguageChange = (lang) => {
    console.log("Language changed to:", lang);
    // Implement your language change logic here (e.g., setting a cookie or context)
    setIsLangMenuOpen(false);
  };

  // Icon hover class that will be used for all icon containers
  const iconHoverClass = "transition-all duration-200 hover:drop-shadow-[0_0_8px_rgba(20,184,166,0.65)] transform hover:scale-110";

  return (
    <header className="bg-white shadow-md fixed top-0 left-0 w-full z-50 flex flex-col md:flex-row md:h-16">
      {/* Top row for small screens - Logo and Burger */}
      <div className="flex items-center justify-between w-full h-16 md:hidden px-5">
        {/* Logo on left for small screens */}
        <div className="flex items-center">
          <Link href={"/"}>
            <Image src="/assets/header/selgo.svg" alt="Selgo Logo" width={80} height={32} priority />
          </Link>
        </div>

        {/* Burger on right for small screens */}
        <div className="relative">
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className={`relative ${iconHoverClass}`}
          >
            <CiMenuFries size={24} className="text-teal-700" />
          </button>

          {isMenuOpen && (
            <div
              id="menu"
              className="absolute top-full right-0 w-64 bg-white shadow-lg z-[9999] p-4 rounded-lg md:hidden"
            >
              <ul className="flex flex-col space-y-4 text-gray-900">
                {menuItems.map((item, index) => (
                  <Link href={item.href} key={index}>
                    <li className="flex items-center gap-3 text-lg font-medium hover:text-teal-500 cursor-pointer">
                      <div className={iconHoverClass}>
                        <Image
                          src={`/assets/header/dropdown/${item.icon}`}
                          alt={item.name}
                          width={24}
                          height={24}
                        />
                      </div>
                      {item.name}
                    </li>
                  </Link>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {/* Bottom row for small screens - Post Ad, Language, Messages, Notifications, User */}
      <div className="fixed bottom-0 left-0 right-0 z-50 bg-white shadow-inner flex items-center justify-between px-5 w-full h-12 md:hidden">
               {/* Post Ad */}
          <Link href="/routes/create-ad">
            <div className={iconHoverClass}>
              <CiCirclePlus size={24} className="text-teal-700 cursor-pointer" />
            </div>
          </Link>


        {/* Language Dropdown (Mobile) */}
        <div className="relative">
          <button
            id="lang-button"
            onClick={() => setIsLangMenuOpen(!isLangMenuOpen)}
            className={`p-1 cursor-pointer rounded-full hover:shadow-teal-100 transition-colors duration-200 group ${iconHoverClass}`}
          >
            <HiLanguage size={24} className="text-teal-700 group-hover:text-teal-700" />
          </button>
          {isLangMenuOpen && (
            <div
              id="lang-menu"
              className="absolute -top-20 border-1 border-teal-400 left-0 w-32 bg-white shadow-lg z-40 p-2 rounded-lg"
            >
              <ul className="flex flex-col space-y-2 text-gray-900">
                <li
                  className="cursor-pointer hover:text-teal-500"
                  onClick={() => handleLanguageChange("en")}
                >
                  English (En)
                </li>
                <li
                  className="cursor-pointer hover:text-teal-500"
                  onClick={() => handleLanguageChange("no")}
                >
                  Norsk (No)
                </li>
              </ul>
            </div>
          )}
        </div>

        {/* Messages */}
        <Link href="/routes/messages">
          <div className={`relative cursor-pointer ${iconHoverClass}`}>
            <CiChat1 size={24} className="text-teal-700" />
            {messages > 0 && (
              <span className="absolute -top-1 -right-2 bg-red-500 text-white text-xs rounded-full px-1">
                {messages}
              </span>
            )}
          </div>
        </Link>

        {/* Notifications */}
        <Link href="/routes/notifications">
          <div className={`relative cursor-pointer ${iconHoverClass}`}>
            <CiBellOn size={24} className="text-teal-700" />
            {notifications > 0 && (
              <span className="absolute -top-1 -right-2 bg-red-500 text-white text-xs rounded-full px-1">
                {notifications}
              </span>
            )}
          </div>
        </Link>

        {/* User Profile (Mobile) - Fixed nesting issue */}
        <div className="relative flex items-center gap-1 cursor-pointer">
          {isAuthenticated() ? (
            <>
              <div onClick={handleProfileClick} className={`flex items-center ${iconHoverClass}`}>
                {user?.avatar ? (
                  <Image
                    src={user.avatar}
                    alt="User"
                    width={32}
                    height={32}
                    className="rounded-full cursor-pointer"
                  />
                ) : (
                  <FaUserCircle size={28} className="text-teal-700" />
                )}
              </div>
              <button
                onClick={handleLogout}
                className="text-sm text-teal-700 hover:underline"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <div onClick={handleProfileClick} className={`flex items-center ${iconHoverClass}`}>
                <FaUserCircle size={24} className="text-teal-700 cursor-pointer" />
              </div>
              <Link href="/routes/auth/signin">
                <span className="text-sm text-teal-700 hover:underline">Log in</span>
              </Link>
            </>
          )}
        </div>
      </div>


      {/* Desktop Layout - Hidden on small screens */}
      <div className="w-full flex justify-center">
        <div className="hidden md:flex items-center justify-between w-full px-8 flex-wrap max-w-4xl lg:px-0">
          {/* Left - Burger Icon + Logo */}
          <div className="flex items-center space-x-6 shrink-0">
            {/* Burger Icon */}
            <button onClick={() => setIsMenuOpen(!isMenuOpen)} className={`relative ${iconHoverClass}`}>
              <CiMenuFries size={24} className="text-teal-700 shrink-0" />
            </button>

            {/* Logo */}
            <Link href={"/"}>
              <div className="flex justify-center items-center shrink-0">
                <Image
                  src="/assets/header/selgo.svg"
                  alt="Selgo Logo"
                  width={90}
                  height={40}
                  priority
                  className="shrink-0"
                />
              </div>
            </Link>
          </div>

          {/* Right - Actions */}
          <div className="flex items-center space-x-5 shrink-0">
            {/* Post Ad */}
            <Link href="/routes/ads">
              <div className={iconHoverClass}>
                <CiCirclePlus size={24} className="text-teal-700 cursor-pointer shrink-0" />
              </div>
            </Link>

            {/* Messages */}
            <Link href="/routes/messages">
              <div className={`relative cursor-pointer ${iconHoverClass}`}>
                <CiChat1 size={24} className="text-teal-700 shrink-0" />
                {messages > 0 && (
                  <span className="absolute -top-1 -right-2 bg-red-500 text-white text-xs rounded-full px-1">
                    {messages}
                  </span>
                )}
              </div>
            </Link>

            {/* Notifications */}
            <Link href="/routes/notifications">
              <div className={`relative cursor-pointer ${iconHoverClass}`}>
                <CiBellOn size={24} className="text-teal-700 shrink-0" />
                {notifications > 0 && (
                  <span className="absolute -top-1 -right-2 bg-red-500 text-white text-xs rounded-full px-1">
                    {notifications}
                  </span>
                )}
              </div>
            </Link>

            {/* Language Dropdown */}
            <div className="relative shrink-0">
              <button
                id="lang-button-desktop"
                onClick={() => setIsLangMenuOpen(!isLangMenuOpen)}
                className={`p-1 cursor-pointer rounded-full hover:shadow-teal-100 transition-colors duration-200 group ${iconHoverClass}`}
              >
                <HiLanguage size={24} className="text-teal-700 group-hover:text-teal-700 shrink-0" />
              </button>
              {isLangMenuOpen && (
                <div
                  id="lang-menu-desktop"
                  className="absolute top-full left-0 w-32 border border-teal-500 bg-white shadow-lg z-40 p-2 rounded-lg"
                >
                  <ul className="flex flex-col space-y-2 text-gray-900">
                    <li className="cursor-pointer hover:text-teal-500" onClick={() => handleLanguageChange("en")}>
                      English (En)
                    </li>
                    <li className="cursor-pointer hover:text-teal-500" onClick={() => handleLanguageChange("no")}>
                      Norsk (No)
                    </li>
                  </ul>
                </div>
              )}
            </div>

            {/* User Profile */}
            <div className="relative flex items-center gap-1 cursor-pointer shrink-0">
              {isAuthenticated() ? (
                <>
                  <div onClick={handleProfileClick} className={`flex items-center ${iconHoverClass}`}>
                    {user?.avatar ? (
                      <Image
                        src={user.avatar}
                        alt="User"
                        width={32}
                        height={32}
                        className="rounded-full cursor-pointer shrink-0"
                      />
                    ) : (
                      <FaUserCircle size={28} className="text-teal-700 shrink-0" />
                    )}
                  </div>
                  <button onClick={handleLogout} className="text-sm text-teal-700 hover:underline">
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <div onClick={handleProfileClick} className={`flex items-center ${iconHoverClass}`}>
                    <FaUserCircle size={24} className="text-teal-700 cursor-pointer shrink-0" />
                  </div>
                  <Link href="/routes/auth/signin">
                    <span className="text-sm text-teal-700 hover:underline">Log in</span>
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Desktop Dropdown Menu for Burger (if open) */}
      {isMenuOpen && (
        <div
          id="menu"
          className="hidden md:block absolute top-full left-60 border-1 rounded-lg border-teal-300 p-4 w-1/2 md:w-1/4 lg:w-1/5 bg-white shadow-lg z-40 rounded-b-lg"
        >
          <ul className="flex flex-col space-y-4 text-gray-900">
            {menuItems.map((item, index) => (
              <Link href={item.href} key={index}>
                <li className="flex items-center gap-3 text-lg font-medium hover:text-teal-500 cursor-pointer">
                  <div className={iconHoverClass}>
                    <Image
                      src={`/assets/header/dropdown/${item.icon}`}
                      alt={item.name}
                      width={24}
                      height={24}
                    />
                  </div>
                  {item.name}
                </li>
              </Link>
            ))}
          </ul>
        </div>
      )}
    </header>
  );
};

export default Header;