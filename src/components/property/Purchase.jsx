import GenericCardCollection from "../GenericCardCollection";
import Card from "../root/Card";
const propertyIcons = [
    { tag: "Plots", icon: "1.svg", route: "/plots" },
    { tag: "Residence Abroad", icon: "2.svg", route: "/residence-abroad" },
    { tag: "Housing for Sale", icon: "3.svg", route: "/housing-sale" },
    { tag: "New Homes", icon: "4.svg", route: "/new-homes" },
    { tag: "Vacation Homes", icon: "5.svg", route: "/vacation-homes" },
    { tag: "Leisure Plots", icon: "6.svg", route: "/leisure-plots" },
];

export default function Purchase() {
    return (
        <div>

            {/* Icon Row (GenericCardCollection) */}
            <div className="relative -top-10">
                <GenericCardCollection
                    rows={[{ items: propertyIcons }]}
                    imageBasePath="/assets/property/"
                    containerStyles={{ container: "mt-6" }}
                    rowStyles={{
                        0: { gridCols: "grid-cols-2 sm:grid-cols-3 md:grid-cols-6", centered: true },
                    }}
                />
            </div>

            {/* Property Listing Section */}
            <div className="w-full relative -top-10 mt-12 pb-10">
                <div className="flex items-center gap-10 justify-center">
                    {/* Property Card */}
                    <div className="w-full max-w-sm">
                        <Card
                            id="1"
                            image="/assets/property/property.jpeg"
                            title="Rooms"
                            price="$150"
                            description="1 bedroom"
                            route="/routes/property/property-details"
                        />
                    </div>
                    {/* Property Info Text - Centered & Responsive */}
                    {/* Property Info Text */}
                    <div className="flex flex-col items-center space-y-8">
                        <h2 className="text-xl text-gray-800 font-semibold">
                            The house with four bedrooms or the apartment with a west-facing balcony?
                        </h2>
                        <p className="text-gray-600 mt-2">
                            We understand it's difficult to choose...💙 That's why we've created a new
                            comparison service called Bolig i sikte. Here you can easily keep track of and
                            compare homes.
                        </p>
                        <button className="mt-4 px-6 py-3 bg-teal-600 text-white rounded-md font-semibold hover:bg-teal-700 transition-all">
                            Compare Homes
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}