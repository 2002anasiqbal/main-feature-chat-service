# selgo-backend/motorcycle-service/main.py
"""
Main entry point for running the motorcycle service directly without Docker
Usage: python main.py
"""

import uvicorn
import os
from dotenv import load_dotenv  # Add this import
from src.app import app
from src.database.database import create_tables

def main():
    """
    Main function to start the motorcycle service
    """
    # Load environment variables from .env file
    load_dotenv()
    
    print("🏍️  Starting Selgo Motorcycle Service...")
    
    # Handle database setup based on environment
    environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "development":
        print("📊 Creating database tables (development mode)...")
        try:
            create_tables()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Error creating database tables: {e}")
            print("⚠️  Make sure PostgreSQL is running and database exists")
            print("💡 For production, use 'alembic upgrade head' instead")
            return
    else:
        print("🏭 Production environment detected")
        print("💡 Make sure to run 'alembic upgrade head' before starting the service")
        print("⚠️  Skipping direct table creation in production mode")
    
    # Configuration (using your .env variables)
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8003"))
    reload = os.getenv("ENVIRONMENT", "development") == "development"
    
    print(f"🌐 Server will start on: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔄 Auto-reload: {'Enabled' if reload else 'Disabled'}")
    print(f"🌍 Environment: {environment}")
    print("🚀 Starting server...\n")
    
    # Start the server
    uvicorn.run(
        "src.app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    main()