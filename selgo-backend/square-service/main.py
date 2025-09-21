import uvicorn
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    host = os.getenv("API_HOST", "localhost")
    port = int(os.getenv("API_PORT", "8000"))

    logger.info(f"Starting Boat Service on {host}:{port}")

    # Start the server
    uvicorn.run(
        "src.app:app",
        host=host,
        port=port,
        reload=True if os.getenv("ENVIRONMENT", "development") == "development" else False,
    )
