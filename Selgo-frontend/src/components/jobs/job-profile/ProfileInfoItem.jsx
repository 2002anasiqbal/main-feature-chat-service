export function ProfileInfoItem({ label, value, onEdit, onAdd, className = "" }) {
    return (
      <div className={`border rounded-md ${className}`}>
        <div className="flex justify-between items-center p-3">
          <div>
            {label && <div className="text-sm font-medium mb-1">{label}</div>}
            <div className="text-sm">{value}</div>
          </div>
          <div className="flex">
            <button 
              onClick={onEdit} 
              className="text-white bg-teal-600 hover:bg-teal-700 font-medium rounded-md text-sm px-5 py-2 mx-1"
            >
              Edit
            </button>
            <button 
              onClick={onAdd} 
              className="text-teal-600 hover:text-teal-700 mx-1"
            >
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
  