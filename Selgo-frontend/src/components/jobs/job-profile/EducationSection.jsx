// File: components/jobs/job-profile/EducationSection.jsx
"use client";

import { useState } from "react";
import { ProgressBar } from "./ProgressBar";

export function EducationSection({ educations = [], onUpdate, onAdd }) {
    const [isAddingNew, setIsAddingNew] = useState(false);
    const [newEducation, setNewEducation] = useState({
        degree: '',
        field_of_study: '',
        institution: '',
        location: '',
        start_date: '',
        end_date: '',
        is_current: false,
        description: ''
    });

    const handleInputChange = (field, value) => {
        setNewEducation(prev => ({
            ...prev,
            [field]: value
        }));
    };

    const handleSave = async () => {
        try {
            if (!newEducation.degree || !newEducation.institution) {
                alert('Please fill in degree and institution');
                return;
            }

            await onAdd(newEducation);
            
            setNewEducation({
                degree: '',
                field_of_study: '',
                institution: '',
                location: '',
                start_date: '',
                end_date: '',
                is_current: false,
                description: ''
            });
            setIsAddingNew(false);
        } catch (error) {
            console.error('Error adding education:', error);
        }
    };

    const handleCancel = () => {
        setNewEducation({
            degree: '',
            field_of_study: '',
            institution: '',
            location: '',
            start_date: '',
            end_date: '',
            is_current: false,
            description: ''
        });
        setIsAddingNew(false);
    };

    const getCompletionPercentage = () => {
        if (educations.length === 0) return 40;
        return Math.min(40 + (educations.length * 30), 100);
    };

    return (
        <div className="border rounded-md mb-4 mt-4">
            <div className="p-3">
                <h3 className="text-sm font-medium mb-2">Education</h3>
                <ProgressBar percentage={getCompletionPercentage()} />
                
                {/* Existing Education */}
                {educations.length > 0 && (
                    <div className="mt-3 mb-3">
                        {educations.map((edu, index) => (
                            <div key={index} className="border-l-4 border-blue-500 pl-3 mb-3 bg-gray-50 p-2 rounded">
                                <div className="font-medium text-sm">{edu.degree}</div>
                                <div className="text-sm text-gray-600">{edu.institution}</div>
                                {edu.field_of_study && <div className="text-xs text-gray-500">{edu.field_of_study}</div>}
                                {edu.is_current && <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Current</span>}
                            </div>
                        ))}
                    </div>
                )}

                {isAddingNew ? (
                    <div className="mt-3 space-y-3">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            <div>
                                <label className="block text-xs font-medium text-gray-700 mb-1">Degree*</label>
                                <input
                                    type="text"
                                    value={newEducation.degree}
                                    onChange={(e) => handleInputChange('degree', e.target.value)}
                                    className="w-full p-2 border border-gray-300 rounded-md text-sm"
                                    placeholder="e.g. Bachelor of Science"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-gray-700 mb-1">Field of Study</label>
                                <input
                                    type="text"
                                    value={newEducation.field_of_study}
                                    onChange={(e) => handleInputChange('field_of_study', e.target.value)}
                                    className="w-full p-2 border border-gray-300 rounded-md text-sm"
                                    placeholder="e.g. Computer Science"
                                />
                            </div>
                        </div>
                        
                        <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">Institution*</label>
                            <input
                                type="text"
                                value={newEducation.institution}
                                onChange={(e) => handleInputChange('institution', e.target.value)}
                                className="w-full p-2 border border-gray-300 rounded-md text-sm"
                                placeholder="e.g. University of Oslo"
                            />
                        </div>

                        <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">Location</label>
                            <input
                                type="text"
                                value={newEducation.location}
                                onChange={(e) => handleInputChange('location', e.target.value)}
                                className="w-full p-2 border border-gray-300 rounded-md text-sm"
                                placeholder="e.g. Oslo, Norway"
                            />
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            <div>
                                <label className="block text-xs font-medium text-gray-700 mb-1">Start Date</label>
                                <input
                                    type="date"
                                    value={newEducation.start_date}
                                    onChange={(e) => handleInputChange('start_date', e.target.value)}
                                    className="w-full p-2 border border-gray-300 rounded-md text-sm"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-gray-700 mb-1">End Date</label>
                                <input
                                    type="date"
                                    value={newEducation.end_date}
                                    onChange={(e) => handleInputChange('end_date', e.target.value)}
                                    disabled={newEducation.is_current}
                                    className="w-full p-2 border border-gray-300 rounded-md text-sm disabled:bg-gray-100"
                                />
                                <label className="flex items-center mt-1">
                                    <input
                                        type="checkbox"
                                        checked={newEducation.is_current}
                                        onChange={(e) => {
                                            handleInputChange('is_current', e.target.checked);
                                            if (e.target.checked) {
                                                handleInputChange('end_date', '');
                                            }
                                        }}
                                        className="mr-2"
                                    />
                                    <span className="text-xs text-gray-600">I'm currently studying here</span>
                                </label>
                            </div>
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
                        {educations.length === 0 ? (
                            <>
                                <p className="text-center my-3">Have you completed an education?</p>
                                <p className="text-center text-sm text-gray-500 mb-3">Tell what and where you have studied</p>
                            </>
                        ) : (
                            <p className="text-center text-sm text-gray-500 mb-3">Add more education to strengthen your profile</p>
                        )}
                        
                        <div className="flex justify-center">
                            <button 
                                onClick={() => setIsAddingNew(true)}
                                className="text-white bg-teal-600 hover:bg-teal-700 font-medium rounded-md text-sm px-5 py-2 mx-1"
                            >
                                {educations.length === 0 ? 'Add' : 'Add More'}
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}