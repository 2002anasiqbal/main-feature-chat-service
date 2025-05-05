import Image from "next/image";
const UsedProductInfo = () => {
    return (
      <section className="text-gray-800 max-w-5xl mx-auto px-4 py-10">
        <div className="flex flex-col md:flex-row items-center gap-8">
          {/* Image */}
          <div className="w-full md:w-1/2">
            <Image
              src="/assets/eu-electronics/2.svg" // Replace with your actual path
              width={100}
              height={80}
              alt="Used product"
              className="rounded-xl w-full object-cover"
            />
          </div>
  
          {/* Text Content */}
          <div className="w-full md:w-1/2">
            <h2 className="text-xl font-semibold mb-4">A safe and easy way to buy used</h2>
            <ol className="list-decimal list-inside text-gray-700 space-y-2 text-sm">
              <li>The product undergoes a thorough quality check by professionals</li>
              <li>Parts that do not work perfectly (such as the screen or battery) are replaced</li>
              <li>Professionally cleaned and data from previous owner deleted</li>
              <li>You receive the product in the post and can enjoy a 2-year warranty!</li>
            </ol>
          </div>
        </div>
  
        {/* Message Section */}
        <div className="text-center mt-10">
          <p className="font-semibold mb-4 text-lg">If you have any questions message us</p>
          <button className="bg-teal-600 hover:bg-teal-700 text-white text-sm font-semibold py-2 px-6 rounded-lg shadow-md transition-all">
            Send message
          </button>
        </div>
      </section>
    );
  };
  
  export default UsedProductInfo;  