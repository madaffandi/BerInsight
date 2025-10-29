import os
import json
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from collections import Counter

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
    type: Optional[str] = "insight"  # complaint, suggestion, insight
    product: Optional[str] = None
    feature: Optional[str] = None
    channel: Optional[str] = None  # BRImo, BRILink, CERIA, Qlola, MMS, Sabrina
    social_media: Optional[str] = None  # YouTube, Instagram, Twitter, Facebook, AppStore, Playstore
    sentiment: Optional[str] = "neutral"  # positive, neutral, negative
    urgency_score: Optional[int] = 50
    date: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[int] = None  # For CSV data - star rating
    user: Optional[str] = None  # For CSV data - reviewer name
    
    class Config:
        extra = "allow"  # Allow additional fields

class InsightsResponse(BaseModel):
    last_updated: str
    items: List[Insight]

class ComplaintItem(BaseModel):
    type: str
    product: str
    count: int
    percentage: float
    examples: List[str]

class ComplaintsResponse(BaseModel):
    total_complaints: int
    by_type: List[ComplaintItem]
    by_product: List[ComplaintItem]
    date_range: Dict[str, str]

class SuggestionItem(BaseModel):
    type: str
    product: str
    count: int
    priority: str
    examples: List[str]

class SuggestionsResponse(BaseModel):
    total_suggestions: int
    by_type: List[SuggestionItem]
    by_product: List[SuggestionItem]
    date_range: Dict[str, str]

class TrendPoint(BaseModel):
    date: str
    count: int
    sentiment_score: float

class ProductTrend(BaseModel):
    product: str
    feature: str
    data: List[TrendPoint]

class TrendsResponse(BaseModel):
    trends: List[ProductTrend]
    date_range: Dict[str, str]

class SentimentSummary(BaseModel):
    positive: int
    neutral: int
    negative: int
    total: int
    average_score: float
    top_keywords: List[Dict[str, Any]]

class DisposisiRequest(BaseModel):
    insight_id: str
    assigned_to: str
    division: str
    priority: str  # low, medium, high, critical
    due_date: str
    notes: Optional[str] = None

class DisposisiResponse(BaseModel):
    id: str
    status: str
    message: str
    assigned_to: str
    division: str

# Initialize FastAPI app
app = FastAPI(
    title="BerInsight API",
    description="Customer Knowledge Analytics API for BerInsight Dashboard",
    version="2.0.0"
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
    logger.info(f"Starting BerInsight API on port {PORT}")
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

@app.get("/api/complaints")
async def get_complaints(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    """Get complaints analysis grouped by type and product"""
    try:
        # Load insights data
        if not os.path.exists(DATA_PATH):
            return ComplaintsResponse(
                total_complaints=0,
                by_type=[],
                by_product=[],
                date_range={"start": start_date or "N/A", "end": end_date or "N/A"}
            )
        
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        items = data.get('items', [])
        
        # Filter complaints and apply date range
        complaints = [item for item in items if item.get('type') == 'complaint']
        
        if start_date or end_date:
            filtered = []
            for complaint in complaints:
                item_date = complaint.get('date')
                if item_date:
                    if start_date and item_date < start_date:
                        continue
                    if end_date and item_date > end_date:
                        continue
                filtered.append(complaint)
            complaints = filtered
        
        total = len(complaints)
        
        # Group by type
        type_counter = Counter(c.get('category', 'Unknown') for c in complaints)
        by_type = [
            ComplaintItem(
                type=t,
                product="All",
                count=count,
                percentage=round((count / total * 100), 2) if total > 0 else 0,
                examples=[c['title'] for c in complaints if c.get('category') == t][:3]
            )
            for t, count in type_counter.most_common()
        ]
        
        # Group by product
        product_counter = Counter(c.get('product', 'Unknown') for c in complaints)
        by_product = [
            ComplaintItem(
                type="All",
                product=p,
                count=count,
                percentage=round((count / total * 100), 2) if total > 0 else 0,
                examples=[c['title'] for c in complaints if c.get('product') == p][:3]
            )
            for p, count in product_counter.most_common()
        ]
        
        return ComplaintsResponse(
            total_complaints=total,
            by_type=by_type,
            by_product=by_product,
            date_range={"start": start_date or "N/A", "end": end_date or "N/A"}
        )
        
    except Exception as e:
        logger.error(f"Error getting complaints: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/suggestions")
async def get_suggestions(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    """Get suggestions analysis grouped by type and product"""
    try:
        if not os.path.exists(DATA_PATH):
            return SuggestionsResponse(
                total_suggestions=0,
                by_type=[],
                by_product=[],
                date_range={"start": start_date or "N/A", "end": end_date or "N/A"}
            )
        
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        items = data.get('items', [])
        suggestions = [item for item in items if item.get('type') == 'suggestion']
        
        # Apply date filter
        if start_date or end_date:
            filtered = []
            for suggestion in suggestions:
                item_date = suggestion.get('date')
                if item_date:
                    if start_date and item_date < start_date:
                        continue
                    if end_date and item_date > end_date:
                        continue
                filtered.append(suggestion)
            suggestions = filtered
        
        total = len(suggestions)
        
        # Group by type
        type_counter = Counter(s.get('category', 'Unknown') for s in suggestions)
        by_type = [
            SuggestionItem(
                type=t,
                product="All",
                count=count,
                priority="medium",  # Could be calculated based on urgency_score
                examples=[s['title'] for s in suggestions if s.get('category') == t][:3]
            )
            for t, count in type_counter.most_common()
        ]
        
        # Group by product
        product_counter = Counter(s.get('product', 'Unknown') for s in suggestions)
        by_product = [
            SuggestionItem(
                type="All",
                product=p,
                count=count,
                priority="medium",
                examples=[s['title'] for s in suggestions if s.get('product') == p][:3]
            )
            for p, count in product_counter.most_common()
        ]
        
        return SuggestionsResponse(
            total_suggestions=total,
            by_type=by_type,
            by_product=by_product,
            date_range={"start": start_date or "N/A", "end": end_date or "N/A"}
        )
        
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trends")
async def get_trends(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    product: Optional[str] = Query(None)
):
    """Get product-feature trends over time"""
    try:
        if not os.path.exists(DATA_PATH):
            return TrendsResponse(
                trends=[],
                date_range={"start": start_date or "N/A", "end": end_date or "N/A"}
            )
        
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        items = data.get('items', [])
        
        # Filter by product if specified
        if product:
            items = [item for item in items if item.get('product') == product]
        
        # Group by product-feature and date
        trends_data = {}
        for item in items:
            prod = item.get('product', 'Unknown')
            feat = item.get('feature', 'General')
            date = item.get('date', datetime.now().strftime('%Y-%m-%d'))
            sentiment = item.get('sentiment', 'neutral')
            
            # Apply date filter
            if start_date and date < start_date:
                continue
            if end_date and date > end_date:
                continue
            
            key = f"{prod}|{feat}"
            if key not in trends_data:
                trends_data[key] = {}
            
            if date not in trends_data[key]:
                trends_data[key][date] = {'count': 0, 'sentiment_sum': 0}
            
            trends_data[key][date]['count'] += 1
            # Sentiment score: positive=1, neutral=0, negative=-1
            sentiment_value = 1 if sentiment == 'positive' else (-1 if sentiment == 'negative' else 0)
            trends_data[key][date]['sentiment_sum'] += sentiment_value
        
        # Convert to response format
        trends = []
        for key, dates_data in trends_data.items():
            prod, feat = key.split('|')
            trend_points = []
            
            for date, stats in sorted(dates_data.items()):
                trend_points.append(TrendPoint(
                    date=date,
                    count=stats['count'],
                    sentiment_score=round(stats['sentiment_sum'] / stats['count'], 2) if stats['count'] > 0 else 0
                ))
            
            trends.append(ProductTrend(
                product=prod,
                feature=feat,
                data=trend_points
            ))
        
        return TrendsResponse(
            trends=trends,
            date_range={"start": start_date or "N/A", "end": end_date or "N/A"}
        )
        
    except Exception as e:
        logger.error(f"Error getting trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sentiment")
async def get_sentiment_summary(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    """Get sentiment analysis summary"""
    try:
        if not os.path.exists(DATA_PATH):
            return SentimentSummary(
                positive=0,
                neutral=0,
                negative=0,
                total=0,
                average_score=0.0,
                top_keywords=[]
            )
        
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        items = data.get('items', [])
        
        # Apply date filter
        if start_date or end_date:
            filtered = []
            for item in items:
                item_date = item.get('date')
                if item_date:
                    if start_date and item_date < start_date:
                        continue
                    if end_date and item_date > end_date:
                        continue
                filtered.append(item)
            items = filtered
        
        # Count sentiments
        sentiment_counter = Counter(item.get('sentiment', 'neutral') for item in items)
        positive = sentiment_counter.get('positive', 0)
        neutral = sentiment_counter.get('neutral', 0)
        negative = sentiment_counter.get('negative', 0)
        total = len(items)
        
        # Calculate average score (positive=1, neutral=0, negative=-1)
        if total > 0:
            score_sum = positive * 1 + neutral * 0 + negative * (-1)
            average_score = round(score_sum / total, 2)
        else:
            average_score = 0.0
        
        # Extract top keywords (simplified - count words in titles)
        all_words = []
        for item in items:
            title = item.get('title', '')
            words = [w.lower() for w in title.split() if len(w) > 3]
            all_words.extend(words)
        
        word_counter = Counter(all_words)
        top_keywords = [
            {"word": word, "count": count}
            for word, count in word_counter.most_common(10)
        ]
        
        return SentimentSummary(
            positive=positive,
            neutral=neutral,
            negative=negative,
            total=total,
            average_score=average_score,
            top_keywords=top_keywords
        )
        
    except Exception as e:
        logger.error(f"Error getting sentiment summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/disposisi")
async def create_disposisi(request: DisposisiRequest):
    """Create disposisi assignment to PO/Division"""
    try:
        # In production, this would save to database
        # For now, we'll just return a success response
        disposisi_id = f"DISP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        logger.info(f"Creating disposisi: {disposisi_id} for {request.assigned_to}")
        
        return DisposisiResponse(
            id=disposisi_id,
            status="created",
            message=f"Disposisi berhasil dibuat dan dikirim ke {request.assigned_to}",
            assigned_to=request.assigned_to,
            division=request.division
        )
        
    except Exception as e:
        logger.error(f"Error creating disposisi: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "BerInsight API",
        "version": "2.0.0",
        "endpoints": {
            "health": "/healthz",
            "insights": "/insights",
            "complaints": "/api/complaints",
            "suggestions": "/api/suggestions",
            "trends": "/api/trends",
            "sentiment": "/api/sentiment",
            "disposisi": "/api/disposisi (POST)"
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
