// File: components/jobs/job-profile/AboutMeSection.jsx
"use client";

import { useState } from "react";
import { ProgressBar } from "./ProgressBar";

export function AboutMeSection({ summary, onUpdate }) {
    const [isEditing, setIsEditing] = useState(false);
    const [editValue, setEditValue] = useState(summary || '');

    const handleSave = () => {
        onUpdate(editValue);
        setIsEditing(false);
    };

    const handleCancel = () => {
        setEditValue(summary || '');
        setIsEditing(false);
    };

    const getCompletionPercentage = () => {
        return summary && summary.trim().length > 0 ? 80 : 40;
    };

    return (
        <div className="border rounded-md mb-4">
            <div className="p-3">
                <h3 className="text-sm font-medium mb-2">About me</h3>
                <ProgressBar percentage={getCompletionPercentage()} />
                
                {isEditing ? (
                    <div className="mt-3">
                        <textarea
                            value={editValue}
                            onChange={(e) => setEditValue(e.target.value)}
                            className="w-full p-2 border border-gray-300 rounded-md resize-none"
                            rows="4"
                            placeholder="Write a short summary of who you are and what you can do..."
                        />
                        <div className="flex justify-center gap-2 mt-3">
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
                        {summary ? (
                            <div className="mt-3">
                                <p className="text-sm text-gray-700 mb-3">{summary}</p>
                            </div>
                        ) : (
                            <div>
                                <p className="text-center my-3">Make a good first impression</p>
                                <p className="text-center text-sm text-gray-500 mb-3">Write a short summary of who you are and what you can do</p>
                            </div>
                        )}
                        
                        <div className="flex justify-center">
                            <button 
                                onClick={() => setIsEditing(true)}
                                className="text-white bg-teal-600 hover:bg-teal-700 font-medium rounded-md text-sm px-5 py-2 mx-1"
                            >
                                {summary ? 'Edit' : 'Add'}
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}