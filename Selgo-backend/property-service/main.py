# property-service/main.py (Fixed for your structure)
"""
Main entry point for the Property Service
Run with: python main.py
"""

import os
import sys
import uvicorn
from pathlib import Path

def main():
    """Main function to start the Property Service"""
    
    print("🚀 Starting Selgo Property Service...")
    print("=" * 50)
    
    # Get configuration from environment variables or use defaults
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8004"))
    environment = os.getenv("ENVIRONMENT", "development")
    reload = environment == "development"
    
    # Database configuration info
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "selgo_property")
    db_user = os.getenv("DB_USER", "postgres")
    
    print(f"🌐 Server Configuration:")
    print(f"   - Host: {host}")
    print(f"   - Port: {port}")
    print(f"   - Environment: {environment}")
    print(f"   - Auto-reload: {reload}")
    print()
    
    print(f"🗄️ Database Configuration:")
    print(f"   - Host: {db_host}:{db_port}")
    print(f"   - Database: {db_name}")
    print(f"   - User: {db_user}")
    print()
    
    print(f"📋 Available Endpoints:")
    print(f"   - API Docs: http://{host}:{port}/docs")
    print(f"   - Health Check: http://{host}:{port}/health")
    print(f"   - Features List: http://{host}:{port}/api/properties/features")
    print()
    
    print(f"🔧 Features Implemented:")
    print(f"   - Points 1-5: Basic property management")
    print(f"   - Points 6-10: Advanced features (map, comparison, loans, rentals)")
    print()
    
    try:
        # Import and run the FastAPI application
        print("⚡ Starting FastAPI server...")
        print("   Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Run the application - use the correct path
        uvicorn.run(
            "src.app:app",  # Correct import path
            host=host,
            port=port,
            reload=reload,
            log_level="info" if environment == "development" else "warning"
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\n🔍 Troubleshooting:")
        print("   1. Check if PostgreSQL is running")
        print("   2. Verify database credentials")
        print("   3. Ensure port 8004 is available")
        print("   4. Check if all dependencies are installed")
        sys.exit(1)

if __name__ == "__main__":
    main()