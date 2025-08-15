import FAQ from "@/components/general/FAQ";
import HeroOnlineCar from "@/components/online-car/HeroOnlineCar";
import HowItWorks from "@/components/online-car/HowItWorks";

export default function OnlineCar() {
    return (
        <div className="bg-white">
            <HeroOnlineCar />
            <HowItWorks />
            <div className="pb-10">
                <FAQ />
            </div>
        </div>
    );
}