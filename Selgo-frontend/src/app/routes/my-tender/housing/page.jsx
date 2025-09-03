import HousingAssociationHelp from "@/components/mt-tender/housing/HousingAssociationHelp";
import HousingAssociationTips from "@/components/mt-tender/housing/HousingAssociationTips";
import HousingCategoryMain from "@/components/mt-tender/housing/HousingCategoryMain";
import HousingEvaluationsSection from "@/components/mt-tender/housing/HousingEvaluationsSection";
import MittanbudComparison from "@/components/mt-tender/housing/MittanbudComparison";
import SatisfiedUsers from "@/components/mt-tender/housing/SatisfiedUsers";
import XLProjectSupervisors from "@/components/mt-tender/housing/XLProjectSupervisors";
import MyTenderMain from "@/components/mt-tender/MyTinderMain";

export default function HousingPage() {
  return (
    <div className="bg-white">
      <HousingCategoryMain/>
      <MittanbudComparison/>
      <XLProjectSupervisors/>
      <HousingAssociationHelp/>
      <SatisfiedUsers/>
      <HousingEvaluationsSection/>
      <HousingAssociationTips/>
    </div>
  );
}