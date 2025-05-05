"use client"
import ProductDetail from "@/components/general/ProductDetail";
import LocationMap from "@/components/general/LocationMap";
export default function ProductPage() {
  return (
    <div className="bg-white pb-44">
    <ProductDetail
      title="Brand new Norcool CU 350 ECO - new price NOK 16,000"
      price="149.99"
      currency="$"
      salePrice="NOK 500"
      productImages={[
        "https://picsum.photos/600/400?random=1",
        "https://picsum.photos/600/400?random=2",
        "https://picsum.photos/600/400?random=3",
      ]}
      description="New in the box. Cooling range from 2 to 18 degrees makes it suitable for cooling both food and wine."
      keyInfo="Form of ownership: Owner (Owned) • Plot area: 6,273 m²"
      sellerInfo={{
        name: "Paintings.no",
        website: "https://companywebsite.com",
        moreAds: "https://companywebsite.com/more-ads",
        followCompany: "https://companywebsite.com/follow",
      }}
      onMessageClick={() => console.log("Send Message clicked")}
      onFixDoneClick={() => console.log("Ask for Fix Done clicked")}
    />
     <div>
      <LocationMap latitude={59.9139} longitude={10.7522} locationName="Oslo, Norway" />
    </div>
    </div>
  );
}