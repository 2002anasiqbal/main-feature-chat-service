"use client";

import React from 'react';
import { ProfileHeader } from './ProfileHeader';
import { ProfileSection } from './ProfileSection';
import { ProfileInfoItem } from './ProfileInfoItem';
import { ProgressBar } from './ProgressBar';
import { AboutMeSection } from './AboutMeSection';
import { ExperienceSection } from './ExperienceSection';
import { RecommendationsPanel } from './RecommendationsPanel';
import { ProfileStrengthPanel } from './ProfileStrengthPanel';
import { ResumePanel } from './ResumePanel';
import { EducationSection } from './EducationSection';
import { LanguageSection } from './LanguageSection';

export default function JobProfile() {
    // This data could come from an API or context
    const profileData = {
        email: 'Lara@gmail.com',
        location: 'Trondhiem',
        production: 'Production of bakery and pasta',
        profileStrength: 40,
        emailForRecommendations: 'xyz@gmail.com'
    };

    return (
        <div className="py-4 text-gray-700">
            <ProfileHeader
                title="Job profile"
                description="With Jobbprofil you get recommendations tailored to your preferences and it is easier to send an application when a job marked with Simple application appears. The job profile is only visible to you, not employers or others."
            />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2">
                    {/* Contact Info Section */}
                    <ProfileSection title="Contact Info">
                        <ProfileInfoItem
                            value={profileData.email}
                            onEdit={() => console.log('Edit contact info')}
                            onAdd={() => console.log('Add contact info')}
                        />
                    </ProfileSection>

                    {/* Wages Section */}
                    <ProfileSection
                        title="Wages"
                        titleButton={true}
                        onTitleButtonClick={() => console.log('Add wages')}
                    >
                        <p className="text-sm text-gray-700 mb-4">
                            The salary information you have added to your current position is used to compare your salary with others who have a similar position
                        </p>
                    </ProfileSection>

                    {/* Wishes for next job Section */}
                    <ProfileSection title="Wishes for the next job">
                        <p className="text-sm text-gray-700 mb-4">
                            The information you provide here is used to provide you with recommended jobs on FINN.
                        </p>

                        {/* Location */}
                        <ProfileInfoItem
                            label="Location"
                            value={profileData.location}
                            onEdit={() => console.log('Edit location')}
                            onAdd={() => console.log('Add location')}
                        />

                        {/* Production */}
                        <ProfileInfoItem
                            label="Production"
                            value={profileData.production}
                            onEdit={() => console.log('Edit production')}
                            onAdd={() => console.log('Add production')}
                            className="mt-4"
                        />
                    </ProfileSection>

                    {/* Resume Section */}
                    <ProfileSection title="Resume">
                        <p className="text-sm text-gray-700 mb-4">
                            You can use the CV directly in applications on FINN marked with "Simple application" or download the CV as a PDF and use it on all applications
                        </p>

                        {/* About me */}
                        <AboutMeSection />

                        {/* Add experience */}
                        <ExperienceSection />

                        <EducationSection />

                        <LanguageSection />
                    </ProfileSection>
                </div>

                <div className="lg:col-span-1">
                    {/* Right sidebar panels */}
                    <ProfileStrengthPanel strength={profileData.profileStrength} />
                    <RecommendationsPanel email={profileData.emailForRecommendations} />
                    <ResumePanel />
                </div>
            </div>
            <button onClick={console.log("delete clicked")} className="bg-red-600 text-white h-10 px-4 rounded-lg">
                Delete your profile
            </button>
        </div>
    );
}