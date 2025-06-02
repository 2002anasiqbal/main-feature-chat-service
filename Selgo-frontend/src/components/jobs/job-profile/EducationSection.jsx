import { ProgressBar } from "./ProgressBar";

export function EducationSection() {
    return (
      <div className="border rounded-md mb-4 mt-4">
        <div className="p-3">
          <h3 className="text-sm font-medium mb-2">Education</h3>
          <ProgressBar percentage={40} />
          <p className="text-center my-3">Have you completed an education?</p>
          <p className="text-center text-sm text-gray-500 mb-3">Tell what and where you have studied</p>
          <div className="flex justify-center">
            <button className="text-white bg-teal-600 hover:bg-teal-700 font-medium rounded-md text-sm px-5 py-2 mx-1">
              Edit
            </button>
            <button className="text-teal-600 hover:text-teal-700 mx-1">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
            </button>
          </div>
        </div>
      </div>
    );
  }  