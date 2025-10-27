import os
import json
import logging
import time
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment variables
DATA_PATH = os.getenv('DATA_PATH', '/data/insights.json')
TZ = os.getenv('TZ', 'Asia/Jakarta')

def get_jakarta_time() -> str:
    """Get current time in Jakarta timezone"""
    jakarta_tz = timezone(timedelta(hours=7))
    now = datetime.now(jakarta_tz)
    return now.strftime('%Y-%m-%d %H:%M WIB')

def fetch_sources() -> List[Dict[str, Any]]:
    """
    Fetch data from various sources.
    This is a stub implementation - replace with actual data sources.
    """
    logger.info("Fetching data from sources...")
    
    # Simulate API calls with retries
    insights = []
    
    # Banking Intelligence Data Sources - replace with real APIs
    sources = [
        {
            "name": "Social Media Intelligence",
            "url": "https://api.twitter.com/v2/tweets/search",
            "mock_data": {
                "title": "Social Media Sentiment Analysis",
                "source": "Twitter API + AI Analysis",
                "summary": "AI detected 15% increase in negative sentiment around banking services. Key concerns: mobile app performance and customer service wait times. Risk level: Medium."
            }
        },
        {
            "name": "Internal Risk Assessment",
            "url": "https://internal-api.bank.com/risk-assessment",
            "mock_data": {
                "title": "Credit Risk Alert",
                "source": "Internal Risk Management System",
                "summary": "Credit risk score increased by 0.3 points due to rising default rates in retail sector. Recommendation: Tighten lending criteria for high-risk segments."
            }
        },
        {
            "name": "Fraud Detection AI",
            "url": "https://ai-api.bank.com/fraud-detection",
            "mock_data": {
                "title": "Fraud Pattern Detection",
                "source": "AI Fraud Detection System",
                "summary": "AI identified new fraud pattern: 23 suspicious transactions detected using similar IP addresses and device fingerprints. Immediate investigation recommended."
            }
        },
        {
            "name": "Regulatory Compliance",
            "url": "https://compliance-api.bank.com/regulatory",
            "mock_data": {
                "title": "Compliance Monitoring Alert",
                "source": "Regulatory Compliance System",
                "summary": "New regulatory requirements detected. 3 transactions flagged for additional KYC verification. Compliance score: 98.5% (above threshold)."
            }
        },
        {
            "name": "Market Intelligence",
            "url": "https://market-api.bank.com/intelligence",
            "mock_data": {
                "title": "Market Risk Assessment",
                "source": "Market Intelligence Platform",
                "summary": "Interest rate volatility increased market risk by 12%. Portfolio exposure to high-risk assets requires immediate review and potential rebalancing."
            }
        }
    ]
    
    for i, source in enumerate(sources):
        try:
            # Simulate API call with timeout and retry
            response = fetch_with_retry(source["url"], timeout=5, max_retries=2, source_index=i)
            
            if response and response.get("success"):
                insights.append(response.get("data", source["mock_data"]))
            else:
                # Use mock data if API fails
                logger.warning(f"API call failed for {source['name']}, using mock data")
                insights.append(source["mock_data"])
                
        except Exception as e:
            logger.error(f"Error fetching from {source['name']}: {e}")
            # Use mock data as fallback
            insights.append(source["mock_data"])
    
    logger.info(f"Successfully fetched {len(insights)} insights")
    return insights

def fetch_with_retry(url: str, timeout: int = 5, max_retries: int = 3, source_index: int = 0) -> Dict[str, Any]:
    """
    Fetch data with retry logic and timeout.
    This is a stub - replace with actual API calls.
    """
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to fetch {url} (attempt {attempt + 1}/{max_retries})")
            
            # Simulate API call
            time.sleep(0.5)  # Simulate network delay
            
            # Mock successful response with banking data
            banking_insights = [
                {
                    "title": "Social Media Sentiment Analysis",
                    "source": "Twitter API + AI Analysis",
                    "summary": "AI detected 15% increase in negative sentiment around banking services. Key concerns: mobile app performance and customer service wait times. Risk level: Medium."
                },
                {
                    "title": "Credit Risk Alert",
                    "source": "Internal Risk Management System",
                    "summary": "Credit risk score increased by 0.3 points due to rising default rates in retail sector. Recommendation: Tighten lending criteria for high-risk segments."
                },
                {
                    "title": "Fraud Pattern Detection",
                    "source": "AI Fraud Detection System",
                    "summary": "AI identified new fraud pattern: 23 suspicious transactions detected using similar IP addresses and device fingerprints. Immediate investigation recommended."
                },
                {
                    "title": "Compliance Monitoring Alert",
                    "source": "Regulatory Compliance System",
                    "summary": "New regulatory requirements detected. 3 transactions flagged for additional KYC verification. Compliance score: 98.5% (above threshold)."
                },
                {
                    "title": "Market Risk Assessment",
                    "source": "Market Intelligence Platform",
                    "summary": "Interest rate volatility increased market risk by 12%. Portfolio exposure to high-risk assets requires immediate review and potential rebalancing."
                }
            ]
            
            return {
                "success": True,
                "data": banking_insights[source_index % len(banking_insights)]
            }
            
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout on attempt {attempt + 1} for {url}")
            if attempt < max_retries - 1:
                time.sleep(1 * (attempt + 1))  # Exponential backoff
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request error on attempt {attempt + 1} for {url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(1 * (attempt + 1))
        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt + 1} for {url}: {e}")
            break
    
    return {"success": False, "error": "All retry attempts failed"}

def save_insights(insights: List[Dict[str, Any]]) -> bool:
    """Save insights to persistent storage"""
    try:
        # Ensure data directory exists
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        
        # Prepare data structure
        data = {
            "last_updated": get_jakarta_time(),
            "items": insights
        }
        
        # Write to file atomically
        temp_path = f"{DATA_PATH}.tmp"
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Atomic move
        os.rename(temp_path, DATA_PATH)
        
        logger.info(f"Successfully saved insights to {DATA_PATH}")
        logger.info(f"Saved {len(insights)} insights")
        return True
        
    except Exception as e:
        logger.error(f"Error saving insights to {DATA_PATH}: {e}")
        return False

def main():
    """Main scraper function with retry wrapper"""
    logger.info("Starting BRInsight scraper...")
    logger.info(f"Data path: {DATA_PATH}")
    logger.info(f"Timezone: {TZ}")
    
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            logger.info(f"Scraper attempt {attempt + 1}/{max_attempts}")
            
            # Fetch insights from sources
            insights = fetch_sources()
            
            if not insights:
                logger.warning("No insights fetched, using fallback data")
                insights = [
                    {
                        "title": "System Status Update",
                        "source": "BRInsight System",
                        "summary": "Scraper is running but no external data sources are available. This is a fallback insight."
                    }
                ]
            
            # Save insights
            if save_insights(insights):
                logger.info("Scraper completed successfully")
                return True
            else:
                logger.error("Failed to save insights")
                
        except Exception as e:
            logger.error(f"Scraper attempt {attempt + 1} failed: {e}")
            if attempt < max_attempts - 1:
                logger.info(f"Retrying in 5 seconds...")
                time.sleep(5)
    
    logger.error("All scraper attempts failed")
    return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
