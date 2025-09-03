export default function SatisfiedUsers() {
    const videos = [1, 2, 3]; // Replace with video thumbnail URLs or embed later
  
    return (
      <div className="bg-white py-16 px-6">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-xl sm:text-2xl font-semibold text-gray-900">
            Meet satisfied users of Mittanbud
          </h2>
          <p className="mt-2 text-gray-700 text-sm sm:text-base">
            With Mittanbud you get the job done! Don&apos;t just take our word for it, check out the videos below and see other people&apos;s experiences with Mittanbud.
          </p>
  
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mt-10">
            {videos.map((_, i) => (
              <div key={i} className="text-center">
                <div className="aspect-video bg-gray-300 rounded" />
                <p className="mt-2 text-sm font-semibold text-gray-700">Customer of Mittanbud</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }
  