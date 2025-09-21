"use client";
import { useRouter } from "next/navigation";
import SquareCard from "./root/Square";
import Image from "next/image";

export default function GenericCardCollection({
  rows = [],
  containerStyles = {},
  rowStyles = {},
  imageBasePath,
  size = "w-25 h-25",
  showDetails,
}) {
  const router = useRouter();
  const handleClick = (route) => router.push(route);

  return (
    <div className={`flex flex-col items-center mt-6 ${containerStyles.container || ""}`}>
      {rows.map((row, rowIndex) => {
        const currentRowStyles = rowStyles[rowIndex] || {};
        // always use 'mb-6' by default, but if there's a custom marginBottom,
        // apply it at md+ only:
        const marginClasses = `mb-6${
          currentRowStyles.marginBottom ? ` md:${currentRowStyles.marginBottom}` : ""
        }`;

        return (
          <div
            key={rowIndex}
            className={`
              w-full
              py-0
              mb-2
              sm:py-6
              sm:${marginClasses}
              overflow-x-visible       /* no scroll by default */
              sm:overflow-x-auto       /* scroll only from sm+ up */
            `}
          >           <div className="mx-auto w-full sm:w-fit">
              <div
                className={`
                  grid grid-cols-2 gap-2 justify-center mx-auto
              
                  sm:flex sm:items-start sm:gap-6 sm:px-4 sm:min-w-max  /* slider on sm+ */
                `}
              >
                {row.items.map((item, index) => (
                  <SquareCard
                    key={index}
                    tag={item.tag}
                    // rectangular on <sm, square & fixed size on sm+:
                    size="w-full h-auto sm:w-25 sm:h-25"
                    onClick={() => handleClick(item.route)}
                    showDetails={showDetails}
                    {...item.additionalProps}
                    IconComponent={item.IconComponent} // New prop for React icons
                    iconProps={item.iconProps} // Props for the icon
                    Icon={!item.IconComponent ? () => (
                      <Image
                        src={`${imageBasePath}${item.icon}`}
                        alt={item.tag}
                        width={item.iconWidth || 20}
                        height={item.iconHeight || 20}
                        className={item.iconClass || "mx-auto"}
                      />
                    ) : undefined}
                  />
                ))}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
