"use client"
// import Header from "@/components/layout/Header";
// import Footer from "@/components/layout/Footer";
import SquareMain from "@/components/theSquare/SquareMain";
import PopularAds from "@/components/home/PopularAds";
import Page from "@/components/GenerateCard";

export default function TheSquare() {
  return (
    <div className="bg-white">
      {/* <Header /> */}
      <SquareMain />
      {/* <div className="> */}
        <PopularAds />
        <Page />
      {/* </div> */}
      {/* <Footer /> */}
    </div>
  );
}