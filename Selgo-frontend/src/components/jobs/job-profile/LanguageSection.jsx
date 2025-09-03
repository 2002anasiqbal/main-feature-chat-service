//File: components/jobs/job-profile/LanguageSection.jsx
"use client";

import { useState } from "react";
import { ProgressBar } from "./ProgressBar";

export function LanguageSection({ languages = [], onUpdate, onAdd }) {
    const [isAddingNew, setIsAddingNew] = useState(false);
    const [newLanguage, setNewLanguage] = useState({
        name: '',
        proficiency_level: 'intermediate'
    });

    const proficiencyLevels = [
        { value: 'beginner', label: 'Beginner' },
        { value: 'intermediate', label: 'Intermediate' },
        { value: 'advanced', label: 'Advanced' },
        { value: 'fluent', label: 'Fluent' },
        { value: 'native', label: 'Native' }
    ];

    const handleInputChange = (field, value) => {
        setNewLanguage(prev => ({
            ...prev,
            [field]: value
        }));
    };

    const handleSave = async () => {
        try {
            if (!newLanguage.name) {
                alert('Please enter a language name');
                return;
            }

            await onAdd(newLanguage.name, newLanguage.proficiency_level);
            
            setNewLanguage({
                name: '',
                proficiency_level: 'intermediate'
            });
            setIsAddingNew(false);
        } catch (error) {
            console.error('Error adding language:', error);
        }
    };

    const handleCancel = () => {
        setNewLanguage({
            name: '',
            proficiency_level: 'intermediate'
        });
        setIsAddingNew(false);
    };

    const getCompletionPercentage = () => {
        if (languages.length === 0) return 40;
        return Math.min(40 + (languages.length * 20), 100);
    };

    const getProficiencyColor = (level) => {
        const colors = {
            beginner: 'bg-red-100 text-red-800',
            intermediate: 'bg-yellow-100 text-yellow-800',
            advanced: 'bg-blue-100 text-blue-800',
            fluent: 'bg-green-100 text-green-800',
            native: 'bg-purple-100 text-purple-800'
        };
        return colors[level] || 'bg-gray-100 text-gray-800';
    };

    return (
        <div className="border rounded-md mb-4">
            <div className="p-3">
                <h3 className="text-sm font-medium mb-2">Language</h3>
                <ProgressBar percentage={getCompletionPercentage()} />
                
                {/* Existing Languages */}
                {languages.length > 0 && (
                    <div className="mt-3 mb-3">
                        {languages.map((lang, index) => (
                            <div key={index} className="flex justify-between items-center border-l-4 border-green-500 pl-3 mb-2 bg-gray-50 p-2 rounded">
                                <div>
                                    <div className="font-medium text-sm">{lang.language?.name || lang.name}</div>
                                </div>
                                <span className={`text-xs px-2 py-1 rounded ${getProficiencyColor(lang.proficiency_level)}`}>
                                    {lang.proficiency_level}
                                </span>
                            </div>
                        ))}
                    </div>
                )}

                {isAddingNew ? (
                    <div className="mt-3 space-y-3">
                        <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">Language*</label>
                            <input
                                type="text"
                                value={newLanguage.name}
                                onChange={(e) => handleInputChange('name', e.target.value)}
                                className="w-full p-2 border border-gray-300 rounded-md text-sm"
                                placeholder="e.g. Norwegian, English, Spanish"
                            />
                        </div>
                        
                        <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">Proficiency Level</label>
                            <select
                                value={newLanguage.proficiency_level}
                                onChange={(e) => handleInputChange('proficiency_level', e.target.value)}
                                className="w-full p-2 border border-gray-300 rounded-md text-sm"
                            >
                                {proficiencyLevels.map(level => (
                                    <option key={level.value} value={level.value}>
                                        {level.label}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="flex justify-center gap-2">
                            <button 
                                onClick={handleSave}
                                className="text-white bg-teal-600 hover:bg-teal-700 font-medium rounded-md text-sm px-5 py-2"
                            >
                                Save
                            </button>
                            <button 
                                onClick={handleCancel}
                                className="text-gray-600 hover:text-gray-700 border border-gray-300 rounded-md text-sm px-5 py-2"
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                ) : (
                    <div>
                        {languages.length === 0 ? (
                            <>
                                <p className="text-center my-3">Hello, Hello, good day</p>
                                <p className="text-center text-sm text-gray-500 mb-3">Add which languages you know well, or just a little</p>
                            </>
                        ) : (
                            <p className="text-center text-sm text-gray-500 mb-3">Add more languages to strengthen your profile</p>
                        )}
                        
                        <div className="flex justify-center">
                            <button 
                                onClick={() => setIsAddingNew(true)}
                                className="text-white bg-teal-600 hover:bg-teal-700 font-medium rounded-md text-sm px-5 py-2 mx-1"
                            >
                                {languages.length === 0 ? 'Add' : 'Add More'}
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}