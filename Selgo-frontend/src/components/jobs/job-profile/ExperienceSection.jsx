// File: components/jobs/job-profile/ExperienceSection.jsx
"use client";

import { useState } from "react";
import { ProgressBar } from "./ProgressBar";

export function ExperienceSection({ experiences = [], onUpdate, onAdd }) {
    const [isAddingNew, setIsAddingNew] = useState(false);
    const [newExperience, setNewExperience] = useState({
        job_title: '',
        company_name: '',
        location: '',
        start_date: '',
        end_date: '',
        is_current: false,
        description: ''
    });

    const handleInputChange = (field, value) => {
        setNewExperience(prev => ({
            ...prev,
            [field]: value
        }));
    };

    const handleSave = async () => {
        try {
            // Validate required fields
            if (!newExperience.job_title || !newExperience.company_name) {
                alert('Please fill in job title and company name');
                return;
            }

            await onAdd(newExperience);
            
            // Reset form
            setNewExperience({
                job_title: '',
                company_name: '',
                location: '',
                start_date: '',
                end_date: '',
                is_current: false,
                description: ''
            });
            setIsAddingNew(false);
        } catch (error) {
            console.error('Error adding experience:', error);
        }
    };

    const handleCancel = () => {
        setNewExperience({
            job_title: '',
            company_name: '',
            location: '',
            start_date: '',
            end_date: '',
            is_current: false,
            description: ''
        });
        setIsAddingNew(false);
    };

    const getCompletionPercentage = () => {
        if (experiences.length === 0) return 30;
        return Math.min(30 + (experiences.length * 20), 100);
    };

    return (
        <div className="border rounded-md mb-4">
            <div className="p-3">
                <h3 className="text-sm font-medium mb-2">Add experience</h3>
                <ProgressBar percentage={getCompletionPercentage()} />
                
                {/* Existing Experiences */}
                {experiences.length > 0 && (
                    <div className="mt-3 mb-3">
                        {experiences.map((exp, index) => (
                            <div key={index} className="border-l-4 border-teal-500 pl-3 mb-3 bg-gray-50 p-2 rounded">
                                <div className="font-medium text-sm">{exp.job_title}</div>
                                <div className="text-sm text-gray-600">{exp.company_name}</div>
                                {exp.location && <div className="text-xs text-gray-500">{exp.location}</div>}
                                {exp.is_current && <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Current</span>}
                            </div>
                        ))}
                    </div>
                )}

                {isAddingNew ? (
                    <div className="mt-3 space-y-3">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            <div>
                                <label className="block text-xs font-medium text-gray-700 mb-1">Job Title*</label>
                                <input
                                    type="text"
                                    value={newExperience.job_title}
                                    onChange={(e) => handleInputChange('job_title', e.target.value)}
                                    className="w-full p-2 border border-gray-300 rounded-md text-sm"
                                    placeholder="e.g. Software Engineer"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-gray-700 mb-1">Company*</label>
                                <input
                                    type="text"
                                    value={newExperience.company_name}
                                    onChange={(e) => handleInputChange('company_name', e.target.value)}
                                    className="w-full p-2 border border-gray-300 rounded-md text-sm"
                                    placeholder="e.g. Microsoft"
                                />
                            </div>
                        </div>
                        
                        <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">Location</label>
                            <input
                                type="text"
                                value={newExperience.location}
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
                                    value={newExperience.start_date}
                                    onChange={(e) => handleInputChange('start_date', e.target.value)}
                                    className="w-full p-2 border border-gray-300 rounded-md text-sm"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-gray-700 mb-1">End Date</label>
                                <input
                                    type="date"
                                    value={newExperience.end_date}
                                    onChange={(e) => handleInputChange('end_date', e.target.value)}
                                    disabled={newExperience.is_current}
                                    className="w-full p-2 border border-gray-300 rounded-md text-sm disabled:bg-gray-100"
                                />
                                <label className="flex items-center mt-1">
                                    <input
                                        type="checkbox"
                                        checked={newExperience.is_current}
                                        onChange={(e) => {
                                            handleInputChange('is_current', e.target.checked);
                                            if (e.target.checked) {
                                                handleInputChange('end_date', '');
                                            }
                                        }}
                                        className="mr-2"
                                    />
                                    <span className="text-xs text-gray-600">I currently work here</span>
                                </label>
                            </div>
                        </div>

                        <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">Description</label>
                            <textarea
                                value={newExperience.description}
                                onChange={(e) => handleInputChange('description', e.target.value)}
                                className="w-full p-2 border border-gray-300 rounded-md text-sm"
                                rows="3"
                                placeholder="Describe your role and achievements..."
                            />
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
                        {experiences.length === 0 ? (
                            <>
                                <p className="text-center my-3">You are almost there!</p>
                                <p className="text-center text-sm text-gray-500 mb-3">When did you start? Add a date to be able to use the Job profile as a CV</p>
                            </>
                        ) : (
                            <p className="text-center text-sm text-gray-500 mb-3">Add more experience to strengthen your profile</p>
                        )}
                        
                        <div className="flex justify-center">
                            <button 
                                onClick={() => setIsAddingNew(true)}
                                className="text-white bg-teal-600 hover:bg-teal-700 font-medium rounded-md text-sm px-5 py-2 mx-1"
                            >
                                {experiences.length === 0 ? 'Fill out' : 'Add More'}
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
