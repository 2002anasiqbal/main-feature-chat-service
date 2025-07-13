// selgo-frontend/src/app/routes/motor-cycle/create-ad/page.jsx
// FIXED: Use correct category name with "6000" suffix

"use client";
import { useSearchParams } from "next/navigation";
import MotorcycleForm from "@/components/MC/form/MotorcycleForm";

export default function CreateMotorcycleAd() {
  const searchParams = useSearchParams();
  const rawCategory = searchParams.get('category') || 'Motorcycles 6000';
  
  // Fix category mapping - ensure it matches database categories
  const categoryMap = {
    'Motorcycles': 'Motorcycles 6000',
    'Thresher': 'Thresher 6000',
    'Suzuki': 'Suzuki 6000',
    'Auto bikes': 'Auto bikes 6000',
    'Tractor': 'Tractor 6000',
    'Bikes': 'Bikes 6000'
  };
  
  // Map the category to the correct database name
  const category = categoryMap[rawCategory] || rawCategory;
  
  console.log("🔍 Category Debug:");
  console.log("  Raw category from URL:", rawCategory);
  console.log("  Mapped category:", category);

  return (
    <div className="min-h-screen bg-white">
      <div className="container mx-auto px-4 py-8">
        <MotorcycleForm category={category} />
      </div>
    </div>
  );
}