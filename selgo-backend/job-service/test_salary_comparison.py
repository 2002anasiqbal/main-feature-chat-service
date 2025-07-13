#!/usr/bin/env python3
"""
Simple test script for Salary Comparison Feature
Tests the functionality using direct database operations
"""

def test_salary_comparison():
    """Test the salary comparison functionality directly"""
    
    print("🔍 Testing Salary Comparison Feature")
    print("=" * 50)
    
    try:
        # Import required modules
        from sqlalchemy import create_engine, text
        
        # Create database connection (adjust if needed)
        DATABASE_URL = "postgresql://postgres:12345@localhost:5432/selgo_job"
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as connection:
            # Test 1: Check if salary_entries table exists
            print("\n1. Checking database setup...")
            result = connection.execute(text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_name = 'salary_entries'
            """))
            
            if result.fetchone():
                print("✅ salary_entries table exists")
            else:
                print("❌ salary_entries table not found - run job service first to create tables")
                return
            
            # Test 2: Insert sample data
            print("\n2. Inserting sample salary data...")
            sample_data = [
                ("Software Engineer", 95000, "San Francisco, CA", 3, "Technology", "201-1000"),
                ("Software Engineer", 110000, "Seattle, WA", 5, "Technology", "1000+"),
                ("Software Engineer", 75000, "Austin, TX", 2, "Technology", "11-50"),
                ("Senior Software Engineer", 140000, "New York, NY", 8, "Financial Services", "1000+"),
                ("Data Scientist", 120000, "San Francisco, CA", 4, "Technology", "501-1000"),
                ("Product Manager", 130000, "Los Angeles, CA", 6, "Technology", "201-1000")
            ]
            
            for job_title, salary, location, experience, industry, company_size in sample_data:
                try:
                    connection.execute(text("""
                        INSERT INTO salary_entries 
                        (profile_id, job_title, annual_salary, location, years_of_experience, 
                         industry, company_size, is_anonymous, created_at)
                        VALUES (1, :job_title, :salary, :location, :experience, 
                                :industry, :company_size, true, NOW())
                        ON CONFLICT DO NOTHING
                    """), {
                        "job_title": job_title,
                        "salary": salary,
                        "location": location,
                        "experience": experience,
                        "industry": industry,
                        "company_size": company_size
                    })
                    print(f"✅ Added: {job_title} - ${salary:,}")
                except Exception as e:
                    print(f"⚠️ Skipped (may be duplicate): {job_title}")
            
            connection.commit()
            
            # Test 3: Basic salary statistics
            print("\n3. Testing basic salary statistics...")
            result = connection.execute(text("""
                SELECT 
                    COUNT(*) as total_entries,
                    AVG(annual_salary) as avg_salary,
                    MIN(annual_salary) as min_salary,
                    MAX(annual_salary) as max_salary
                FROM salary_entries 
                WHERE job_title ILIKE '%Software Engineer%'
                AND is_anonymous = true
            """))
            
            row = result.fetchone()
            if row:
                print(f"✅ Software Engineer Statistics:")
                print(f"   Total Entries: {row[0]}")
                print(f"   Average Salary: ${row[1]:,.2f}")
                print(f"   Salary Range: ${row[2]:,.0f} - ${row[3]:,.0f}")
            
            # Test 4: Industry comparison
            print("\n4. Testing industry comparison...")
            result = connection.execute(text("""
                SELECT 
                    industry,
                    COUNT(*) as count,
                    AVG(annual_salary) as avg_salary
                FROM salary_entries 
                WHERE job_title ILIKE '%Engineer%'
                AND is_anonymous = true
                AND industry IS NOT NULL
                GROUP BY industry
                ORDER BY avg_salary DESC
            """))
            
            print("✅ Industry Comparison (Engineer roles):")
            for row in result:
                print(f"   {row[0]}: ${row[2]:,.0f} avg ({row[1]} entries)")
            
            # Test 5: Experience level analysis
            print("\n5. Testing experience level analysis...")
            result = connection.execute(text("""
                SELECT 
                    CASE 
                        WHEN years_of_experience BETWEEN 0 AND 2 THEN '0-2 years'
                        WHEN years_of_experience BETWEEN 3 AND 5 THEN '3-5 years'
                        WHEN years_of_experience BETWEEN 6 AND 10 THEN '6-10 years'
                        ELSE '10+ years'
                    END as experience_bracket,
                    COUNT(*) as count,
                    AVG(annual_salary) as avg_salary
                FROM salary_entries 
                WHERE job_title ILIKE '%Software Engineer%'
                AND is_anonymous = true
                AND years_of_experience IS NOT NULL
                GROUP BY experience_bracket
                ORDER BY avg_salary
            """))
            
            print("✅ Experience Level Analysis (Software Engineer):")
            for row in result:
                print(f"   {row[0]}: ${row[2]:,.0f} avg ({row[1]} entries)")
            
            # Test 6: Location comparison
            print("\n6. Testing location comparison...")
            result = connection.execute(text("""
                SELECT 
                    location,
                    COUNT(*) as count,
                    AVG(annual_salary) as avg_salary
                FROM salary_entries 
                WHERE job_title ILIKE '%Software Engineer%'
                AND is_anonymous = true
                AND location IS NOT NULL
                GROUP BY location
                ORDER BY avg_salary DESC
            """))
            
            print("✅ Location Comparison (Software Engineer):")
            for row in result:
                print(f"   {row[0]}: ${row[2]:,.0f} avg ({row[1]} entries)")
            
            print("\n" + "=" * 50)
            print("🎉 Database Testing Complete!")
            print("\n📝 Next Steps:")
            print("1. Start your job service: python main.py")
            print("2. Test API endpoints at: http://localhost:8002/docs")
            print("3. Try these API calls:")
            print("   - POST /api/v1/salary/compare")
            print("   - GET /api/v1/salary/insights/Software%20Engineer")
            print("   - GET /api/v1/salary/market-overview")
    
    except ImportError:
        print("❌ Missing dependencies. Install with:")
        print("   pip install sqlalchemy psycopg2-binary")
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        print("\n📝 Setup Instructions:")
        print("1. Ensure PostgreSQL is running")
        print("2. Create database 'selgo_job'")
        print("3. Run the job service once to create tables")
        print("4. Update DATABASE_URL in this script if needed")

if __name__ == "__main__":
    print("🚀 Starting Salary Comparison Feature Tests")
    print("💡 This script tests the database queries directly")
    test_salary_comparison()