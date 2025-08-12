# File: job-service/src/main.py

from .app import app

if __name__ == "__main__":
    import uvicorn
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    host = os.getenv("API_HOST", "localhost")
    port = int(os.getenv("API_PORT", "8002"))
    
    uvicorn.run(app, host=host, port=port)