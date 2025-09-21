# src/main.py
from .app import app

if __name__ == "__main__":
    # This won't be executed when imported by the root main.py
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)