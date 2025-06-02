import GenericCardCollection from "@/components/GenericCardCollection";

const propertyIcons = [
    { tag: "Plots", icon: "1.svg", route: "/plots" },
    { tag: "Residence Abroad", icon: "2.svg", route: "/residence-abroad" },
    { tag: "Housing for Sale", icon: "3.svg", route: "/housing-sale" },
    { tag: "New Homes", icon: "4.svg", route: "/new-homes" },
    { tag: "Vacation Homes", icon: "5.svg", route: "/vacation-homes" },
    { tag: "Leisure Plots", icon: "6.svg", route: "/leisure-plots" },
];
export default function NutritionPage() {
    return (
        <div>
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

        </div>
    );
}
