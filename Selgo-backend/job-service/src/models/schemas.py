# File: job-service/src/models/schemas.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class JobTypeEnum(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"

class ExperienceLevelEnum(str, Enum):
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"

class JobStatusEnum(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    DRAFT = "draft"
    PAUSED = "paused"

class ProficiencyLevelEnum(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    FLUENT = "fluent"
    NATIVE = "native"

class CVTemplateEnum(str, Enum):
    MODERN = "modern"
    CLASSIC = "classic"
    CREATIVE = "creative"
    MINIMAL = "minimal"

# Base Schemas
class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None
    founded_year: Optional[int] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Job Schemas
class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=10)
    short_description: Optional[str] = None
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    benefits: Optional[str] = None
    job_type: JobTypeEnum
    experience_level: ExperienceLevelEnum
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: str = "USD"
    is_salary_negotiable: bool = False
    location: Optional[str] = None
    is_remote: bool = False
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    application_deadline: Optional[datetime] = None
    application_email: Optional[str] = None
    application_url: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    featured: bool = False
    tags: Optional[List[str]] = None

class JobCreate(JobBase):
    company_id: int
    category_id: Optional[int] = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    benefits: Optional[str] = None
    job_type: Optional[JobTypeEnum] = None
    experience_level: Optional[ExperienceLevelEnum] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    is_salary_negotiable: Optional[bool] = None
    location: Optional[str] = None
    is_remote: Optional[bool] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    application_deadline: Optional[datetime] = None
    application_email: Optional[str] = None
    application_url: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    status: Optional[JobStatusEnum] = None
    featured: Optional[bool] = None
    tags: Optional[List[str]] = None

class JobResponse(JobBase):
    id: int
    slug: str
    status: JobStatusEnum
    view_count: int = 0
    application_count: int = 0
    company_id: int
    category_id: Optional[int] = None
    posted_by: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    
    # Nested objects
    company: Optional[CompanyResponse] = None
    
    model_config = ConfigDict(from_attributes=True)

# Job Search and Filter Schemas
class JobSearchRequest(BaseModel):
    q: Optional[str] = None  # Search query
    location: Optional[str] = None
    job_type: Optional[List[JobTypeEnum]] = None
    experience_level: Optional[List[ExperienceLevelEnum]] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    is_remote: Optional[bool] = None
    company_id: Optional[int] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    posted_within_days: Optional[int] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
    sort_by: Optional[str] = "created_at"  # created_at, salary_max, view_count
    sort_order: Optional[str] = "desc"  # asc, desc

class JobSearchResponse(BaseModel):
    jobs: List[JobResponse]
    total: int
    page: int
    limit: int
    total_pages: int

# Profile Schemas
class JobProfileBase(BaseModel):
    phone: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    professional_summary: Optional[str] = None
    desired_job_title: Optional[str] = None
    desired_salary_min: Optional[float] = None
    desired_salary_max: Optional[float] = None
    salary_currency: str = "USD"
    willing_to_relocate: bool = False
    available_from: Optional[datetime] = None
    profile_visibility: str = "private"
    allow_contact: bool = True
    receive_job_alerts: bool = True

class JobProfileCreate(JobProfileBase):
    pass

class JobProfileUpdate(JobProfileBase):
    pass

class JobProfileResponse(JobProfileBase):
    id: int
    user_id: int
    profile_completion: int = 0
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Work Experience Schemas
class WorkExperienceBase(BaseModel):
    job_title: str = Field(..., min_length=1, max_length=255)
    company_name: str = Field(..., min_length=1, max_length=255)
    company_website: Optional[str] = None
    location: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    is_current: bool = False
    description: Optional[str] = None
    achievements: Optional[str] = None
    display_order: int = 0

class WorkExperienceCreate(WorkExperienceBase):
    pass

class WorkExperienceUpdate(WorkExperienceBase):
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    start_date: Optional[datetime] = None

class WorkExperienceResponse(WorkExperienceBase):
    id: int
    profile_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Education Schemas
class EducationBase(BaseModel):
    degree: str = Field(..., min_length=1, max_length=255)
    field_of_study: Optional[str] = None
    institution: str = Field(..., min_length=1, max_length=255)
    location: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    is_current: bool = False
    gpa: Optional[float] = None
    description: Optional[str] = None
    display_order: int = 0

class EducationCreate(EducationBase):
    pass

class EducationUpdate(EducationBase):
    degree: Optional[str] = None
    institution: Optional[str] = None
    start_date: Optional[datetime] = None

class EducationResponse(EducationBase):
    id: int
    profile_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Skill Schemas
class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserSkillBase(BaseModel):
    skill_id: int
    proficiency_level: ProficiencyLevelEnum
    years_of_experience: Optional[int] = None

class UserSkillCreate(UserSkillBase):
    pass

class UserSkillResponse(UserSkillBase):
    id: int
    profile_id: int
    skill: Optional[SkillResponse] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Language Schemas
class LanguageBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    code: Optional[str] = None

class LanguageCreate(LanguageBase):
    pass

class LanguageResponse(LanguageBase):
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserLanguageBase(BaseModel):
    language_id: int
    proficiency_level: ProficiencyLevelEnum

class UserLanguageCreate(UserLanguageBase):
    pass

class UserLanguageResponse(UserLanguageBase):
    id: int
    profile_id: int
    language: Optional[LanguageResponse] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# CV Schemas
class CVBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    template: CVTemplateEnum = CVTemplateEnum.MODERN
    cv_data: Optional[Dict[str, Any]] = None
    is_public: bool = False
    allow_downloads: bool = True

class CVCreate(CVBase):
    pass

class CVUpdate(BaseModel):
    title: Optional[str] = None
    template: Optional[CVTemplateEnum] = None
    cv_data: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None
    allow_downloads: Optional[bool] = None

class CVResponse(CVBase):
    id: int
    user_id: int
    status: str
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    view_count: int = 0
    download_count: int = 0
    created_at: datetime
    updated_at: datetime
    last_generated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# CV Builder Steps Schemas
class ContactInfoStep(BaseModel):
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None

class WorkExperienceStep(BaseModel):
    experiences: List[WorkExperienceBase] = []

class EducationStep(BaseModel):
    educations: List[EducationBase] = []

class LanguageStep(BaseModel):
    languages: List[UserLanguageBase] = []

class SummaryStep(BaseModel):
    professional_summary: str

class CVBuilderData(BaseModel):
    contact_info: Optional[ContactInfoStep] = None
    work_experience: Optional[WorkExperienceStep] = None
    education: Optional[EducationStep] = None
    languages: Optional[LanguageStep] = None
    summary: Optional[SummaryStep] = None

# Article Schemas
class ArticleCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    display_order: int = 0

class ArticleCategoryCreate(ArticleCategoryBase):
    pass

class ArticleCategoryResponse(ArticleCategoryBase):
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    excerpt: Optional[str] = None
    content: str = Field(..., min_length=10)
    featured_image: Optional[str] = None
    image_alt: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    reading_time: Optional[int] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    featured_image: Optional[str] = None
    image_alt: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    status: Optional[str] = None

class ArticleResponse(ArticleBase):
    id: int
    status: str
    published_at: Optional[datetime] = None
    author_id: int
    view_count: int = 0
    created_at: datetime
    updated_at: datetime
    category: Optional[ArticleCategoryResponse] = None
    
    model_config = ConfigDict(from_attributes=True)

# Salary Comparison Schemas
class SalaryEntryBase(BaseModel):
    job_title: str = Field(..., min_length=1, max_length=255)
    annual_salary: float = Field(..., gt=0)
    currency: str = "USD"
    bonus: Optional[float] = None
    stock_options: Optional[float] = None
    other_compensation: Optional[float] = None
    company_name: Optional[str] = None
    location: Optional[str] = None
    years_of_experience: Optional[int] = None
    company_size: Optional[str] = None
    industry: Optional[str] = None
    is_current: bool = True
    is_anonymous: bool = True

class SalaryEntryCreate(SalaryEntryBase):
    pass

class SalaryEntryResponse(SalaryEntryBase):
    id: int
    profile_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class SalaryComparisonRequest(BaseModel):
    job_title: str
    location: Optional[str] = None
    years_of_experience: Optional[int] = None
    industry: Optional[str] = None

class SalaryComparisonResponse(BaseModel):
    job_title: str
    location: Optional[str] = None
    average_salary: float
    median_salary: float
    min_salary: float
    max_salary: float
    total_entries: int
    percentile_25: float
    percentile_75: float
    currency: str = "USD"

# Recommendation Schemas
class JobRecommendationResponse(BaseModel):
    id: int
    job_id: int
    score: float
    reason: Optional[str] = None
    job: Optional[JobResponse] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Popular Search Schemas
class PopularSearchResponse(BaseModel):
    id: int
    search_term: str
    search_type: str
    search_count: int
    is_featured: bool
    display_order: int
    
    model_config = ConfigDict(from_attributes=True)

class PopularSearchesGrouped(BaseModel):
    positions: List[str] = []
    locations: List[str] = []
    articles: List[str] = []

# File Upload Schemas
class FileUploadResponse(BaseModel):
    filename: str
    file_path: str
    file_size: int
    file_type: str
    upload_url: Optional[str] = None

# Generic Response Schemas
class MessageResponse(BaseModel):
    message: str
    
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    
# Job Alert Schemas
class JobAlertCreate(BaseModel):
    alert_name: str = Field(..., min_length=1, max_length=255)
    search_criteria: Dict[str, Any] = Field(..., description="Search parameters for the alert")
    notification_method: str = Field(default="email", description="email, push, both")
    frequency: str = Field(default="daily", description="daily, weekly, monthly")

class JobAlertUpdate(BaseModel):
    alert_name: Optional[str] = None
    search_criteria: Optional[Dict[str, Any]] = None
    notification_method: Optional[str] = None
    frequency: Optional[str] = None
    is_active: Optional[bool] = None

class JobAlertResponse(BaseModel):
    id: int
    user_id: int
    alert_name: str
    search_criteria: Dict[str, Any]
    is_active: bool
    notification_method: str
    frequency: str
    total_jobs_sent: int
    last_sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Job Recommendation Schemas
class JobRecommendationResponse(BaseModel):
    job_id: int
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    score: float
    reason: str
    created_at: datetime

# User Job Preferences Schemas
class UserJobPreferencesCreate(BaseModel):
    preferred_job_titles: Optional[List[str]] = None
    preferred_locations: Optional[List[str]] = None
    preferred_job_types: Optional[List[str]] = None
    preferred_experience_levels: Optional[List[str]] = None
    min_salary: Optional[float] = None
    max_salary: Optional[float] = None
    salary_currency: str = "USD"
    remote_preference: str = "no_preference"
    preferred_company_sizes: Optional[List[str]] = None
    preferred_industries: Optional[List[str]] = None
    email_notifications: bool = True
    push_notifications: bool = True
    notification_frequency: str = "daily"

class UserJobPreferencesResponse(UserJobPreferencesCreate):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Enhanced Job Response with Analytics
class JobResponseWithAnalytics(JobResponse):
    analytics: Optional[Dict[str, Any]] = None
    is_saved: Optional[bool] = None
    is_applied: Optional[bool] = None
    recommendation_score: Optional[float] = None
    recommendation_reason: Optional[str] = None

# Job Application Schemas
class JobApplicationCreate(BaseModel):
    cover_letter: Optional[str] = None
    cv_file_path: Optional[str] = None
    additional_info: Optional[str] = None

class JobApplicationUpdate(BaseModel):
    status: Optional[str] = None
    cover_letter: Optional[str] = None
    additional_info: Optional[str] = None

class JobApplicationResponse(BaseModel):
    id: int
    job_id: int
    user_id: int
    cover_letter: Optional[str] = None
    cv_file_path: Optional[str] = None
    additional_info: Optional[str] = None
    status: str
    applied_at: datetime
    reviewed_at: Optional[datetime] = None
    job: Optional[JobResponse] = None
    
    model_config = ConfigDict(from_attributes=True)

# Job Category Schemas  
class JobCategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[int] = None

class JobCategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: bool
    job_count: Optional[int] = None
    created_at: datetime
    children: Optional[List['JobCategoryResponse']] = None
    
    model_config = ConfigDict(from_attributes=True)

# Company Schemas (Enhanced)
class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None
    founded_year: Optional[int] = None

class CompanyResponseWithJobs(CompanyResponse):
    jobs: Optional[List[JobResponse]] = None
    job_count: int = 0
    avg_salary: Optional[float] = None

# Job Analytics Schemas
class JobAnalyticsResponse(BaseModel):
    job_id: int
    period: Dict[str, Any]
    summary: Dict[str, Any]
    daily_data: List[Dict[str, Any]]
    geographic_data: List[Dict[str, Any]]
    traffic_sources: List[Dict[str, Any]]

class EmployerAnalyticsResponse(BaseModel):
    employer_id: int
    total_jobs: int
    period: Dict[str, Any]
    summary: Dict[str, Any]
    top_performing_jobs: List[Dict[str, Any]]
    job_performance: List[Dict[str, Any]]

# Search and Filter Schemas (Enhanced)
class JobSearchFilters(BaseModel):
    q: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[List[str]] = None
    experience_level: Optional[List[str]] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    is_remote: Optional[bool] = None
    company_id: Optional[int] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    posted_within_days: Optional[int] = None
    company_size: Optional[List[str]] = None
    industry: Optional[List[str]] = None

class JobSearchResponseEnhanced(BaseModel):
    jobs: List[JobResponseWithAnalytics]
    total: int
    page: int
    limit: int
    total_pages: int
    filters_applied: JobSearchFilters
    facets: Optional[Dict[str, List[Dict[str, Any]]]] = None  # For filter counts

# Saved Job Schemas
class SavedJobResponse(BaseModel):
    id: int
    job_id: int
    user_id: int
    saved_at: datetime
    job: Optional[JobResponse] = None
    
    model_config = ConfigDict(from_attributes=True)

# Job View History Schemas
class JobViewResponse(BaseModel):
    id: int
    job_id: int
    user_id: Optional[int] = None
    viewed_at: datetime
    job: Optional[JobResponse] = None
    
    model_config = ConfigDict(from_attributes=True)

# Job Statistics Schemas
class JobStatisticsResponse(BaseModel):
    total_jobs: int
    active_jobs: int
    jobs_this_month: int
    total_applications: int
    avg_applications_per_job: float
    top_categories: List[Dict[str, Any]]
    top_companies: List[Dict[str, Any]]
    salary_insights: Dict[str, Any]

# Bulk Operations Schemas
class BulkJobAction(BaseModel):
    job_ids: List[int]
    action: str  # activate, deactivate, delete, feature, unfeature
    
class BulkJobResponse(BaseModel):
    successful: List[int]
    failed: List[Dict[str, Any]]
    total_processed: int

# Advanced Filter Options
class FilterOptionsResponse(BaseModel):
    job_types: List[Dict[str, str]]
    experience_levels: List[Dict[str, str]]
    industries: List[Dict[str, Any]]
    company_sizes: List[Dict[str, str]]
    locations: List[Dict[str, Any]]
    salary_ranges: List[Dict[str, Any]]
    categories: List[JobCategoryResponse]
    
# Job Feed Schemas (for homepage/recommendations)
class JobFeedRequest(BaseModel):
    user_location: Optional[str] = None
    user_skills: Optional[List[str]] = None
    feed_type: str = "mixed"  # recent, recommended, trending, mixed
    limit: int = Field(default=20, ge=1, le=100)

class JobFeedResponse(BaseModel):
    jobs: List[JobResponseWithAnalytics]
    feed_type: str
    personalized: bool
    refresh_token: str  # For pagination/refresh

# Company Follow Schemas
class CompanyFollowResponse(BaseModel):
    id: int
    company_id: int
    user_id: int
    followed_at: datetime
    company: Optional[CompanyResponse] = None
    
    model_config = ConfigDict(from_attributes=True)

# Job Alert Summary
class JobAlertSummaryResponse(BaseModel):
    total_alerts: int
    active_alerts: int
    total_jobs_sent: int
    alerts_sent_today: int
    most_active_alert: Optional[str] = None
    
# User Job Activity Summary
class UserJobActivityResponse(BaseModel):
    user_id: int
    jobs_viewed_today: int
    jobs_saved_total: int
    applications_submitted: int
    last_job_viewed: Optional[datetime] = None
    activity_score: int
    recommended_actions: List[str]