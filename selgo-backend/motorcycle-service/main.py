# selgo-backend/motorcycle-service/main.py
"""
Main entry point for running the motorcycle service directly without Docker
Usage: python main.py
"""

import uvicorn
import os
from src.app import app
from src.database import create_tables

def main():
    """
    Main function to start the motorcycle service
    """
    print("🏍️  Starting Selgo Motorcycle Service...")
    
    # Create database tables on startup
    print("📊 Creating database tables...")
    try:
        create_tables()
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        print("⚠️  Make sure PostgreSQL is running and database exists")
        return
    
    # Configuration
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8003"))
    reload = os.getenv("ENVIRONMENT", "development") == "development"
    
    print(f"🌐 Server will start on: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔄 Auto-reload: {'Enabled' if reload else 'Disabled'}")
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
