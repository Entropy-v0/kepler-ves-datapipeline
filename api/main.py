import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from api.routes import router
from dotenv import load_dotenv

# Load environment variables for the API process
load_dotenv()

app = FastAPI(
    title="Kepler P2P API",
    description="API to access Binance P2P market data collected by Kepler Miner",
    version="1.0.0"
)

# Include routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    # Start the server (useful for local development)
    uvicorn.run(app, host="0.0.0.0", port=8000)
