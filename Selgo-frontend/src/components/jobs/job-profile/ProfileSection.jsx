export function ProfileSection({ title, children, titleButton = false, onTitleButtonClick }) {
    return (
      <div className="mb-6">
        <div className="flex items-center mb-2">
          <h2 className="text-lg font-medium text-gray-800">{title}</h2>
          {titleButton && (
            <button 
              onClick={onTitleButtonClick}
              className="ml-2 text-teal-500 hover:text-teal-600"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
            </button>
          )}
        </div>
        {children}
      </div>
    );
  }
  