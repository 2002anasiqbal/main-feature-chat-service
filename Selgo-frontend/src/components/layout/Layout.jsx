"use client";
import { usePathname } from "next/navigation";
import Header from "./Header";
import Footer from "./Footer";
import { FavoritesProvider } from "@/components/favorites/FavoritesManager";

const Layout = ({ children }) => {
  const pathname = usePathname();

  // pages where header/footer should be hidden
  const excludedRoutes = [
    "/routes/auth/signup",
    "/routes/auth/signin",
    "/routes/my-tender",
    "/routes/my-tender/login",
    "/routes/my-tender/plummer",
    "/routes/my-tender/category",
    "/routes/my-tender/registration", 
    "/routes/my-tender/housing",
    "/routes/messages",
  ];

  const shouldShowHeaderFooter = !excludedRoutes.includes(pathname);
  const isMessagesRoute = pathname === "/routes/messages";

  return (
    <FavoritesProvider>
      <div className="flex flex-col min-h-screen bg-white">
        {shouldShowHeaderFooter && <Header />}

        <main
          className={`
            flex-grow
            w-full
            ${isMessagesRoute ? "max-w-full h-full" : "max-w-4xl"}
            mx-auto
            ${shouldShowHeaderFooter ? "sm:pt-16 pt-16" : ""}
            ${isMessagesRoute ? "px-0" : "px-5 md:px-8 lg:px-0"}
          `}
        >
          {children}
        </main>

        {shouldShowHeaderFooter && <Footer />}
      </div>
    </FavoritesProvider>
  );
};

export default Layout;