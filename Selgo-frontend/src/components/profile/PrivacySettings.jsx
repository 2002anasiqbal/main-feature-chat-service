"use client";
import { useState } from "react";

export default function PrivacySettings() {
  // State for toggle switches
  const [toggles, setToggles] = useState({
    newsletter: true,
    personalized: true,
    importantInfo: true,
    shareActivity: true,
    marketing: true,
    ageGroup: true,
    interests: true,
    gender: true,
    area: true
  });

  // Toggle handler
  const handleToggle = (key) => {
    setToggles(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  // State for dropdowns
  const [expandedSections, setExpandedSections] = useState({
    externalAds: false,
    terminateAccount: false
  });

  // Toggle dropdown handler
  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  // Custom toggle switch component
  const ToggleSwitch = ({ id, isOn, onToggle }) => (
    <div 
      className={`relative w-14 h-7 rounded-full cursor-pointer transition-colors duration-200 ease-in-out ${isOn ? 'bg-teal-600' : 'bg-gray-200'}`}
      onClick={onToggle}
    >
      <div 
        className={`absolute top-1 w-5 h-5 bg-white rounded-full transition-transform duration-200 ease-in-out ${isOn ? 'translate-x-8' : 'translate-x-1'}`}
      />
    </div>
  );

  // Custom chevron icon instead of using Lucide React
  const ChevronIcon = ({ isExpanded }) => (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      width="20" 
      height="20" 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      strokeWidth="2" 
      strokeLinecap="round" 
      strokeLinejoin="round"
      className={`transition-transform ${isExpanded ? 'rotate-180' : ''}`}
    >
      <polyline points="6 9 12 15 18 9"></polyline>
    </svg>
  );

  return (
    <div className="py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-4">Privacy settings</h1>
      <p className="text-gray-800 mb-12">
        New rules for privacy give you better control over the traces you leave online, and what FINN and others can use your data for. Good, right? We promise to be open about what we do, and always focus on what helps you.
      </p>

      {/* Newsletter Section */}
      <div className="mb-10">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-xl font-bold text-gray-800">Get a newsletter from FINN</h2>
          <ToggleSwitch 
            id="newsletter" 
            isOn={toggles.newsletter} 
            onToggle={() => handleToggle('newsletter')} 
          />
        </div>
        <p className="text-gray-800">
          FINN sends you newsletters with, for example, travel tips, job trends, fun competitions and smart advice for you as a buyer and seller. To do this, we use the contact information associated with your user on FINN.
        </p>
      </div>

      {/* Personalized FINN */}
      <div className="mb-10">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-xl font-bold text-gray-800">Personalized FINN</h2>
          <ToggleSwitch 
            id="personalized" 
            isOn={toggles.personalized} 
            onToggle={() => handleToggle('personalized')} 
          />
        </div>
        <p className="text-gray-800">
          We show you FINN ads we think you will be interested in and adapt FINN to your use. To do this, we store information about how you use our services. The data is not shared with others.
        </p>
      </div>

      {/* Important Information */}
      <div className="mb-10">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-xl font-bold text-gray-800">Receive important information from FINN</h2>
          <ToggleSwitch 
            id="importantInfo" 
            isOn={toggles.importantInfo} 
            onToggle={() => handleToggle('importantInfo')} 
          />
        </div>
        <p className="text-gray-800">
          We show you FINN ads we think you will be interested in and adapt FINN to your use. To do this, we store information about how you use our services. The data is not shared with others.
        </p>
      </div>

      {/* Account Settings */}
      <h1 className="text-3xl font-bold text-gray-800 mb-4">Settings for your account for Schibsted Marketplaces</h1>
      <p className="text-gray-800 mb-12">
        New rules for privacy give you better control over the traces you leave online, and what FINN and others can use your data for. Good, right? We promise to be open about what we do, and always focus on what helps you.
      </p>

      {/* Share Activity */}
      <div className="mb-10">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-xl font-bold text-gray-800">Share activity for analysis and product development</h2>
          <ToggleSwitch 
            id="shareActivity" 
            isOn={toggles.shareActivity} 
            onToggle={() => handleToggle('shareActivity')} 
          />
        </div>
      </div>

      {/* Marketing */}
      <div className="mb-10">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-xl font-bold text-gray-800">Marketing of the services on other platforms</h2>
          <ToggleSwitch 
            id="marketing" 
            isOn={toggles.marketing} 
            onToggle={() => handleToggle('marketing')} 
          />
        </div>
        <p className="text-gray-800 mb-6">
          Your account information, geographical area, assumed interests and activity in our services allow us to sort news and other content to show you more of the matters that are likely to interest you.
        </p>
        
        <h3 className="text-lg font-semibold text-gray-800 mb-2">Customized advertising</h3>
        <p className="text-gray-800 mb-4">
          Your account information may be used to tailor the advertising you see. We combine it with activity data if you agreed to personalized advertising in the consent settings (popup on the services' website).
        </p>
      </div>

      {/* Ad Settings */}
      <div className="space-y-6 mb-10">
        {/* Age Group */}
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-800">See ads based on age group</h3>
          <ToggleSwitch 
            id="ageGroup" 
            isOn={toggles.ageGroup} 
            onToggle={() => handleToggle('ageGroup')} 
          />
        </div>
        
        {/* Interests */}
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-800">See ads based on interests</h3>
          <ToggleSwitch 
            id="interests" 
            isOn={toggles.interests} 
            onToggle={() => handleToggle('interests')} 
          />
        </div>
        
        {/* Gender */}
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-800">See ads based on gender</h3>
          <ToggleSwitch 
            id="gender" 
            isOn={toggles.gender} 
            onToggle={() => handleToggle('gender')} 
          />
        </div>
        
        {/* Area */}
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-800">See ads based on area</h3>
          <ToggleSwitch 
            id="area" 
            isOn={toggles.area} 
            onToggle={() => handleToggle('area')} 
          />
        </div>
      </div>

      {/* Expandable Sections */}
      <div className="space-y-4">
        {/* External Ads */}
        <div className="border border-gray-200 rounded-lg">
          <button 
            className="w-full flex items-center justify-between p-4 text-left text-gray-800" 
            onClick={() => toggleSection('externalAds')}
          >
            <span className="font-semibold">Settings from ads from external network</span>
            <ChevronIcon isExpanded={expandedSections.externalAds} />
          </button>
          
          {expandedSections.externalAds && (
            <div className="p-4 pt-0 border-t border-gray-200">
              <p className="text-gray-800">
                Settings for external ad networks would appear here. This would include options for managing 
                third-party cookies, ad tracking, and other external advertising preferences.
              </p>
              {/* Placeholder for actual settings */}
              <div className="mt-4 space-y-2">
                <div className="flex items-center">
                  <input type="checkbox" id="thirdParty" className="mr-2" />
                  <label htmlFor="thirdParty" className="text-gray-800">Allow third-party cookies</label>
                </div>
                <div className="flex items-center">
                  <input type="checkbox" id="adTracking" className="mr-2" />
                  <label htmlFor="adTracking" className="text-gray-800">Allow ad tracking</label>
                </div>
              </div>
            </div>
          )}
        </div>
        
        {/* Terminate Account */}
        <div className="border border-gray-200 rounded-lg">
          <button 
            className="w-full flex items-center justify-between p-4 text-left text-gray-800" 
            onClick={() => toggleSection('terminateAccount')}
          >
            <span className="font-semibold">Terminate account</span>
            <ChevronIcon isExpanded={expandedSections.terminateAccount} />
          </button>
          
          {expandedSections.terminateAccount && (
            <div className="p-4 pt-0 border-t border-gray-200">
              <p className="text-gray-800 mb-4">
                Warning: Terminating your account will permanently delete all your data and cannot be undone.
                You will lose access to all services and saved information.
              </p>
              <button className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors">
                Permanently Delete Account
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}