import { FaCheckCircle, FaTruck, FaCalendarAlt, FaThumbsUp } from 'react-icons/fa';

const WarrantyBanner = () => {
  return (
    <div className="text-center py-6">
      <h2 className="text-lg font-medium mb-4 text-gray-800">
        Save up to <span className="font-bold">50%</span> of the new price on used with warranty
      </h2>

      <div className="bg-teal-700 text-white rounded-lg flex flex-wrap justify-between gap-6 px-6 py-3 max-w-4xl mx-auto">
        <div className="flex items-center gap-2">
          <FaCheckCircle className="text-white" />
          <span className="text-sm">2 years warranty</span>
        </div>
        <div className="flex items-center gap-2">
          <FaTruck className="text-white" />
          <span className="text-sm">Fast delivery</span>
        </div>
        <div className="flex items-center gap-2">
          <FaCalendarAlt className="text-white" />
          <span className="text-sm">30 days open purchase</span>
        </div>
        <div className="flex items-center gap-2">
          <FaThumbsUp className="text-white" />
          <span className="text-sm">Checked by professionals</span>
        </div>
      </div>
    </div>
  );
};

export default WarrantyBanner;