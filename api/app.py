import os
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment variables
DATA_PATH = os.getenv('DATA_PATH', '/data/insights.json')
PORT = int(os.getenv('PORT', 8000))

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    time: str

class Insight(BaseModel):
    title: str
    source: str
    summary: str

class InsightsResponse(BaseModel):
    last_updated: str
    items: List[Insight]

# Initialize FastAPI app
app = FastAPI(
    title="BRInsight API",
    description="Business Intelligence API for BRInsight Dashboard",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info(f"Starting BRInsight API on port {PORT}")
    logger.info(f"Data path: {DATA_PATH}")
    
    # Check if data file exists
    if os.path.exists(DATA_PATH):
        logger.info(f"Data file exists at {DATA_PATH}")
    else:
        logger.warning(f"Data file not found at {DATA_PATH}")

@app.get("/healthz", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="ok",
        time=datetime.now(timezone.utc).isoformat()
    )

@app.get("/insights", response_model=InsightsResponse)
async def get_insights():
    """Get insights data from persistent storage"""
    try:
        if not os.path.exists(DATA_PATH):
            logger.warning(f"Data file not found at {DATA_PATH}, returning empty response")
            return InsightsResponse(
                last_updated="never",
                items=[]
            )
        
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate data structure
        if not isinstance(data, dict) or 'items' not in data:
            logger.error(f"Invalid data structure in {DATA_PATH}")
            return InsightsResponse(
                last_updated="never",
                items=[]
            )
        
        # Ensure items is a list
        items = data.get('items', [])
        if not isinstance(items, list):
            items = []
        
        # Validate each insight item
        validated_items = []
        for item in items:
            if isinstance(item, dict) and all(key in item for key in ['title', 'source', 'summary']):
                validated_items.append(Insight(**item))
        
        return InsightsResponse(
            last_updated=data.get('last_updated', 'unknown'),
            items=validated_items
        )
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in {DATA_PATH}: {e}")
        return InsightsResponse(
            last_updated="never",
            items=[]
        )
    except Exception as e:
        logger.error(f"Error reading insights data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "BRInsight API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/healthz",
            "insights": "/insights"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
