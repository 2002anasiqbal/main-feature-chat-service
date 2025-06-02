"use client";
import { useState } from 'react';

const NotificationSettings = () => {
  // State for expandable sections
  const [expandedSections, setExpandedSections] = useState({
    savedSearches: false,
    favorites: false,
    companies: false
  });

  // State for toggle switches
  const [toggles, setToggles] = useState({
    browserNotifications: true,
    emailNotifications: true
  });

  // Toggle expandable sections
  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  // Toggle switch handler
  const handleToggle = (key) => {
    setToggles(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  // Custom toggle switch component
  const ToggleSwitch = ({ isOn, onToggle }) => (
    <div 
      onClick={onToggle}
      className={`relative w-14 h-7 rounded-full cursor-pointer transition-colors duration-200 ease-in-out ${isOn ? 'bg-teal-600' : 'bg-gray-200'}`}
    >
      <div 
        className={`absolute top-1 w-5 h-5 bg-white rounded-full transition-transform duration-200 ease-in-out ${isOn ? 'translate-x-8' : 'translate-x-1'}`}
      />
    </div>
  );

  // Chevron icon component
  const ChevronIcon = ({ isExpanded }) => (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      width="24" 
      height="24" 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      strokeWidth="2" 
      strokeLinecap="round" 
      strokeLinejoin="round"
      className={`transition-transform text-gray-700 ${isExpanded ? 'rotate-180' : ''}`}
    >
      <polyline points="6 9 12 15 18 9"></polyline>
    </svg>
  );

  return (
    <div className="py-4">
      <h1 className="text-3xl font-bold text-gray-800 mb-4">Customize notifications</h1>
      <p className="text-gray-700 mb-8">
        Do you want an immediate notification on your phone when the price of your dream sofa drops? Or perhaps you want notifications about housing by e-mail? Here you can adjust your notifications exactly as you wish - whether it's favourites, saved searches or companies you follow.
      </p>

      {/* Saved Searches Section */}
      <div className="border border-gray-200 rounded-lg mb-4">
        <button
          className="w-full p-4 flex items-center justify-between text-left"
          onClick={() => toggleSection('savedSearches')}
        >
          <div>
            <h2 className="font-medium text-gray-800">New ads from saved searches</h2>
            <p className="text-gray-600 text-sm">We notify you when there are new hits in your saved searches</p>
          </div>
          <ChevronIcon isExpanded={expandedSections.savedSearches} />
        </button>
        
        {expandedSections.savedSearches && (
          <div className="p-4 border-t border-gray-200">
            {/* Content for saved searches notification settings would go here */}
            <p className="text-gray-600">Configure your saved search notification settings here.</p>
          </div>
        )}
      </div>

      {/* Favorites Section */}
      <div className="border border-gray-200 rounded-lg mb-4">
        <button
          className="w-full p-4 flex items-center justify-between text-left"
          onClick={() => toggleSection('favorites')}
        >
          <div>
            <h2 className="font-medium text-gray-800">Favorites</h2>
            <p className="text-gray-600 text-sm">We advise you about updates on your favourites. Note: not all ad types have notifications enabled</p>
          </div>
          <ChevronIcon isExpanded={expandedSections.favorites} />
        </button>
        
        {expandedSections.favorites && (
          <div className="p-4 border-t border-gray-200">
            {/* Content for favorites notification settings would go here */}
            <p className="text-gray-600">Configure your favorite item notification settings here.</p>
          </div>
        )}
      </div>

      {/* Companies Section */}
      <div className="border border-gray-200 rounded-lg mb-8">
        <button
          className="w-full p-4 flex items-center justify-between text-left"
          onClick={() => toggleSection('companies')}
        >
          <div>
            <h2 className="font-medium text-gray-800">New ads and positions from companies I follow</h2>
            <p className="text-gray-600 text-sm">We advise you about new advertisements and positions from companies you follow</p>
          </div>
          <ChevronIcon isExpanded={expandedSections.companies} />
        </button>
        
        {expandedSections.companies && (
          <div className="p-4 border-t border-gray-200">
            {/* Content for company notification settings would go here */}
            <p className="text-gray-600">Configure your company notification settings here.</p>
          </div>
        )}
      </div>

      {/* Browser Notifications */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-xl font-medium text-gray-800">Notifications in the browser</h2>
          <p className="text-gray-600">Receive notifications directly in your browser, even when FINN is closed.</p>
        </div>
        <ToggleSwitch 
          isOn={toggles.browserNotifications} 
          onToggle={() => handleToggle('browserNotifications')} 
        />
      </div>

      {/* Email Notifications */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-xl font-medium text-gray-800">Receive a copy by email</h2>
          <p className="text-gray-600">We will send you a copy of the message by e-mail.</p>
        </div>
        <ToggleSwitch 
          isOn={toggles.emailNotifications} 
          onToggle={() => handleToggle('emailNotifications')} 
        />
      </div>
    </div>
  );
};

export default NotificationSettings;