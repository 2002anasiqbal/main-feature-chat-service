
"use client";

import React, { useState, useEffect } from 'react';
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
import jobService from '@/services/jobService';
import useAuthStore from '@/store/store';
import { useRouter } from 'next/navigation';

export default function JobProfile() {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [recommendations, setRecommendations] = useState([]);
    const [notifications, setNotifications] = useState([]);
    const [showSalaryComparison, setShowSalaryComparison] = useState(false);
    const [salaryComparisonData, setSalaryComparisonData] = useState(null);
    const [loadingSalaryComparison, setLoadingSalaryComparison] = useState(false);
    const { user } = useAuthStore();
    const router = useRouter();

    // Simple notification system
    const showNotification = (message, type = 'success') => {
        const id = Date.now();
        const notification = { id, message, type };
        setNotifications(prev => [...prev, notification]);
        
        setTimeout(() => {
            setNotifications(prev => prev.filter(n => n.id !== id));
        }, 3000);
    };

    const removeNotification = (id) => {
        setNotifications(prev => prev.filter(n => n.id !== id));
    };

    useEffect(() => {
        if (!user && !localStorage.getItem('accessToken')) {
            router.push('/routes/auth/signin?redirect=/routes/jobs/job-profile');
            return;
        }
        
        loadProfileData();
        loadRecommendations();
    }, [user, router]);

    const loadProfileData = async () => {
        try {
            setLoading(true);
            const dashboard = await jobService.getProfileDashboard();
            setProfile(dashboard.profile);
            
            // Check if profile has sufficient data for salary comparison
            if (dashboard.profile?.work_experiences?.length > 0) {
                setShowSalaryComparison(true);
            }
            
        } catch (error) {
            console.error('Error loading profile:', error);
            showNotification('Failed to load profile data', 'error');
        } finally {
            setLoading(false);
        }
    };

    const loadRecommendations = async () => {
        try {
            const recs = await jobService.getJobRecommendationsWithReasons(5);
            setRecommendations(recs);
        } catch (error) {
            console.error('Error loading recommendations:', error);
        }
    };

    const updateProfileField = async (field, value) => {
        try {
            const updateData = { [field]: value };
            const updatedProfile = await jobService.updateProfile(updateData);
            setProfile(updatedProfile);
            showNotification('Profile updated successfully', 'success');
            
            // Reload profile to get updated completion percentage
            loadProfileData();
        } catch (error) {
            console.error('Error updating profile:', error);
            showNotification('Failed to update profile', 'error');
        }
    };

    const deleteProfile = async () => {
        if (!window.confirm('Are you sure you want to delete your profile? This action cannot be undone.')) {
            return;
        }

        try {
            await jobService.deleteProfile();
            showNotification('Profile deleted successfully', 'success');
            setProfile(null);
        } catch (error) {
            console.error('Error deleting profile:', error);
            showNotification('Failed to delete profile', 'error');
        }
    };

    const generateCV = async () => {
        try {
            const cv = await jobService.generateCVFromProfile();
            showNotification('CV generated successfully', 'success');
            await jobService.downloadCV(cv.id);
        } catch (error) {
            console.error('Error generating CV:', error);
            showNotification('Failed to generate CV', 'error');
        }
    };

    const handleSalaryComparison = async () => {
        try {
            setLoadingSalaryComparison(true);
            const comparisonData = await jobService.getProfileSalaryComparison();
            
            if (comparisonData.error) {
                showNotification(comparisonData.message, 'error');
                return;
            }
            
            setSalaryComparisonData(comparisonData);
            // Navigate to salary comparison page with data
            router.push('/routes/jobs/salary-comparison');
        } catch (error) {
            console.error('Error getting salary comparison:', error);
            showNotification('Failed to get salary comparison. Please ensure you have work experience added.', 'error');
        } finally {
            setLoadingSalaryComparison(false);
        }
    };

    const addWorkExperience = async () => {
        try {
            // This would open a modal or navigate to add experience form
            const experienceData = {
                job_title: '',
                company_name: '',
                location: '',
                start_date: new Date(),
                is_current: true,
                description: ''
            };
            
            // For now, we'll prompt for basic info
            const jobTitle = prompt('Enter job title:');
            const companyName = prompt('Enter company name:');
            
            if (jobTitle && companyName) {
                await jobService.addWorkExperience({
                    ...experienceData,
                    job_title: jobTitle,
                    company_name: companyName
                });
                
                showNotification('Work experience added successfully', 'success');
                loadProfileData();
            }
        } catch (error) {
            console.error('Error adding work experience:', error);
            showNotification('Failed to add work experience', 'error');
        }
    };

    const addEducation = async () => {
        try {
            const degree = prompt('Enter degree:');
            const institution = prompt('Enter institution:');
            
            if (degree && institution) {
                await jobService.addEducation({
                    degree,
                    institution,
                    start_date: new Date(),
                    is_current: false
                });
                
                showNotification('Education added successfully', 'success');
                loadProfileData();
            }
        } catch (error) {
            console.error('Error adding education:', error);
            showNotification('Failed to add education', 'error');
        }
    };

    const addSkill = async () => {
        try {
            const skillName = prompt('Enter skill name:');
            const proficiencyLevel = prompt('Enter proficiency level (beginner/intermediate/advanced/expert):') || 'intermediate';
            
            if (skillName) {
                await jobService.addSkill(skillName, proficiencyLevel);
                showNotification('Skill added successfully', 'success');
                loadProfileData();
            }
        } catch (error) {
            console.error('Error adding skill:', error);
            showNotification('Failed to add skill', 'error');
        }
    };

    const addLanguage = async () => {
        try {
            const languageName = prompt('Enter language name:');
            const proficiencyLevel = prompt('Enter proficiency level (beginner/intermediate/advanced/fluent/native):') || 'intermediate';
            
            if (languageName) {
                await jobService.addLanguage(languageName, proficiencyLevel);
                showNotification('Language added successfully', 'success');
                loadProfileData();
            }
        } catch (error) {
            console.error('Error adding language:', error);
            showNotification('Failed to add language', 'error');
        }
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center py-10">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-500"></div>
            </div>
        );
    }

    if (!profile) {
        return (
            <div className="text-center py-10">
                <p className="text-red-600 mb-4">Failed to load profile data</p>
                <button 
                    onClick={loadProfileData}
                    className="bg-teal-600 text-white px-4 py-2 rounded-md hover:bg-teal-700"
                >
                    Retry
                </button>
            </div>
        );
    }

    return (
        <div className="py-4 text-gray-700">
            {/* Notification System */}
            <div className="fixed top-4 right-4 z-50 space-y-2">
                {notifications.map(notification => (
                    <div
                        key={notification.id}
                        className={`px-4 py-2 rounded-md shadow-lg transition-all duration-300 ${
                            notification.type === 'success' 
                                ? 'bg-green-500 text-white' 
                                : 'bg-red-500 text-white'
                        }`}
                    >
                        <div className="flex items-center justify-between">
                            <span>{notification.message}</span>
                            <button
                                onClick={() => removeNotification(notification.id)}
                                className="ml-2 text-white hover:text-gray-200"
                            >
                                ×
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            <ProfileHeader
                title="Job profile"
                description="With Job Profile you get recommendations tailored to your preferences and it is easier to send an application when a job marked with Simple application appears. The job profile is only visible to you, not employers or others."
            />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2">
                    {/* Contact Info Section */}
                    <ProfileSection title="Contact Info">
                        <ProfileInfoItem
                            value={user?.email || 'Email not set'}
                            onEdit={() => console.log('Edit contact info')}
                            onAdd={() => console.log('Add contact info')}
                        />
                        {profile.phone && (
                            <ProfileInfoItem
                                label="Phone"
                                value={profile.phone}
                                onEdit={() => {
                                    const newPhone = prompt('Enter phone number:', profile.phone);
                                    if (newPhone) updateProfileField('phone', newPhone);
                                }}
                                onAdd={() => {
                                    const phone = prompt('Enter phone number:');
                                    if (phone) updateProfileField('phone', phone);
                                }}
                                className="mt-4"
                            />
                        )}
                    </ProfileSection>

                    {/* Salary Comparison Section */}
                    {showSalaryComparison && (
                        <ProfileSection title="Salary Comparison">
                            <p className="text-sm text-gray-700 mb-4">
                                Compare your current salary with market data based on your experience and location.
                            </p>
                            <button
                                onClick={handleSalaryComparison}
                                disabled={loadingSalaryComparison}
                                className="bg-teal-600 text-white px-4 py-2 rounded-md hover:bg-teal-700 disabled:opacity-50"
                            >
                                {loadingSalaryComparison ? 'Loading...' : 'Compare Your Salary'}
                            </button>
                        </ProfileSection>
                    )}

                    {/* Wages Section */}
                    <ProfileSection
                        title="Wages"
                        titleButton={true}
                        onTitleButtonClick={() => {
                            const minSalary = prompt('Enter minimum desired salary:');
                            const maxSalary = prompt('Enter maximum desired salary:');
                            if (minSalary || maxSalary) {
                                updateProfileField('desired_salary_min', minSalary ? parseFloat(minSalary) : null);
                                updateProfileField('desired_salary_max', maxSalary ? parseFloat(maxSalary) : null);
                            }
                        }}
                    >
                        <p className="text-sm text-gray-700 mb-4">
                            The salary information you have added to your current position is used to compare your salary with others who have a similar position
                        </p>
                        {profile.desired_salary_min || profile.desired_salary_max ? (
                            <div className="border rounded-md p-3">
                                <div className="text-sm font-medium">Desired Salary</div>
                                <div className="text-sm">
                                    {profile.desired_salary_min && `$${profile.desired_salary_min.toLocaleString()}`}
                                    {profile.desired_salary_min && profile.desired_salary_max && ' - '}
                                    {profile.desired_salary_max && `$${profile.desired_salary_max.toLocaleString()}`}
                                </div>
                            </div>
                        ) : (
                            <div className="text-gray-500 text-sm">No salary information added</div>
                        )}
                    </ProfileSection>

                    {/* Wishes for next job Section */}
                    <ProfileSection title="Wishes for the next job">
                        <p className="text-sm text-gray-700 mb-4">
                            The information you provide here is used to provide you with recommended jobs on our platform.
                        </p>

                        <ProfileInfoItem
                            label="Location"
                            value={profile.location || 'Location not set'}
                            onEdit={() => {
                                const newLocation = prompt('Enter location:', profile.location || '');
                                if (newLocation) updateProfileField('location', newLocation);
                            }}
                            onAdd={() => {
                                const location = prompt('Enter location:');
                                if (location) updateProfileField('location', location);
                            }}
                        />

                        <ProfileInfoItem
                            label="Desired Position"
                            value={profile.desired_job_title || 'Position not set'}
                            onEdit={() => {
                                const newTitle = prompt('Enter desired job title:', profile.desired_job_title || '');
                                if (newTitle) updateProfileField('desired_job_title', newTitle);
                            }}
                            onAdd={() => {
                                const title = prompt('Enter desired job title:');
                                if (title) updateProfileField('desired_job_title', title);
                            }}
                            className="mt-4"
                        />
                    </ProfileSection>

                    {/* Resume Section */}
                    <ProfileSection title="Resume">
                        <p className="text-sm text-gray-700 mb-4">
                            You can use the CV directly in applications marked with "Simple application" or download the CV as a PDF and use it on all applications
                        </p>

                        <AboutMeSection 
                            summary={profile.professional_summary}
                            onUpdate={(summary) => updateProfileField('professional_summary', summary)}
                        />

                        <ExperienceSection 
                            experiences={profile.work_experiences || []}
                            onUpdate={loadProfileData}
                            onAdd={addWorkExperience}
                        />

                        <EducationSection 
                            educations={profile.educations || []}
                            onUpdate={loadProfileData}
                            onAdd={addEducation}
                        />

                        <LanguageSection 
                            languages={profile.languages || []}
                            onUpdate={loadProfileData}
                            onAdd={addLanguage}
                        />
                    </ProfileSection>
                </div>

                <div className="lg:col-span-1">
                    <ProfileStrengthPanel strength={profile.profile_completion || 0} />
                    <RecommendationsPanel 
                        email={user?.email || ''} 
                        recommendations={recommendations}
                    />
                    <ResumePanel onGenerateCV={generateCV} />
                </div>
            </div>
            
            {/* Delete Profile Button */}
            <div className="mt-8 pt-6 border-t">
                <button 
                    onClick={deleteProfile} 
                    className="bg-red-600 text-white h-10 px-4 rounded-lg hover:bg-red-700 transition"
                >
                    Delete your profile
                </button>
            </div>
        </div>
    );
}