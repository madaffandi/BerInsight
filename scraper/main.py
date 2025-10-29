import os
import json
import logging
import random
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any

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

def get_random_date(days_back=30) -> str:
    """Generate random date within last N days"""
    jakarta_tz = timezone(timedelta(hours=7))
    now = datetime.now(jakarta_tz)
    random_days = random.randint(0, days_back)
    date = now - timedelta(days=random_days)
    return date.strftime('%Y-%m-%d')

def generate_banking_data() -> List[Dict[str, Any]]:
    """
    Generate comprehensive customer knowledge analytics data
    Including: complaints, suggestions, and insights from various channels
    """
    logger.info("Generating customer knowledge analytics data...")
    
    data = []
    
    # BRI Products
    products = [
        "BRImo",
        "Card",
        "Qlola",
        "Loan",
        "Simpedes",
        "Britama",
        "Deposito"
    ]
    
    # BRI Channels
    channels = [
        "BRImo",
        "BRILink",
        "CERIA",
        "Qlola",
        "MMS",
        "Sabrina"
    ]
    
    # Social Media Platforms
    social_media = [
        "YouTube",
        "Instagram", 
        "Twitter",
        "Facebook",
        "Apple AppStore",
        "Google Playstore"
    ]
    
    features = {
        "BRImo": ["Login", "Transfer", "Bill Payment", "QR Payment", "Account Info", "Virtual Account"],
        "Card": ["Payment", "Limit Check", "Reward Points", "Statement", "Activation"],
        "Qlola": ["Merchant Payment", "Top Up", "Transaction History", "Cashback"],
        "Loan": ["Application", "Disbursement", "Payment", "Status Check", "Restructuring"],
        "Simpedes": ["Account Opening", "Savings", "Withdrawal", "Interest"],
        "Britama": ["Account Management", "Transfer", "Monthly Fee", "Benefits"],
        "Deposito": ["Opening", "Renewal", "Interest Rate", "Withdrawal"]
    }
    
    # Complaint Types
    complaint_types = [
        {"category": "Performance Issue", "urgency_base": 70},
        {"category": "Bug/Error", "urgency_base": 85},
        {"category": "Security Concern", "urgency_base": 95},
        {"category": "UI/UX Problem", "urgency_base": 50},
        {"category": "Service Unavailable", "urgency_base": 90},
        {"category": "Transaction Failed", "urgency_base": 95},
        {"category": "Poor Customer Service", "urgency_base": 60},
        {"category": "Unclear Information", "urgency_base": 40}
    ]
    
    complaint_templates = [
        "Aplikasi {product} sering crash saat menggunakan fitur {feature}",
        "Error 'Connection Timeout' terus muncul di {product} - {feature}",
        "Transaksi {feature} di {product} gagal tapi saldo terpotong",
        "Fitur {feature} tidak berfungsi dengan baik di {product}",
        "{product} sangat lambat ketika akses {feature}",
        "Tidak bisa login ke {product} sejak update terakhir",
        "Data di {feature} tidak akurat di {product}",
        "Customer service di {channel} tidak responsif untuk masalah {product}",
        "{feature} di {product} sering error saat peak hours",
        "Proses {feature} terlalu lama di {product}"
    ]
    
    # Generate 200 Complaints
    for _ in range(200):
        product = random.choice(products)
        channel = random.choice(channels)
        platform = random.choice(social_media)
        feature = random.choice(features.get(product, ["General"]))
        complaint_type = random.choice(complaint_types)
        sentiment = random.choices(
            ["negative", "neutral"],
            weights=[0.8, 0.2]
        )[0]
        
        title = random.choice(complaint_templates).format(
            product=product,
            feature=feature,
            channel=channel
        )
        
        data.append({
            "title": title,
            "source": platform,
            "summary": f"Customer reported issue with {feature} in {product} via {channel}. Category: {complaint_type['category']}. Requires immediate attention from product team.",
            "type": "complaint",
            "product": product,
            "feature": feature,
            "channel": channel,
            "social_media": platform,
            "category": complaint_type["category"],
            "sentiment": sentiment,
            "urgency_score": min(100, complaint_type["urgency_base"] + random.randint(-10, 10)),
            "date": get_random_date(30)
        })
    
    # Suggestion Types
    suggestion_types = [
        {"category": "Feature Request", "priority_base": 70},
        {"category": "UX Improvement", "priority_base": 60},
        {"category": "New Product Idea", "priority_base": 50},
        {"category": "Integration Request", "priority_base": 65},
        {"category": "Performance Enhancement", "priority_base": 75},
        {"category": "Security Enhancement", "priority_base": 90},
        {"category": "Accessibility", "priority_base": 55}
    ]
    
    suggestion_templates = [
        "Tambahkan fitur {feature} di {product} untuk kemudahan transaksi",
        "Integrasikan {product} dengan e-wallet populer",
        "Perbaiki UI {feature} di {product} agar lebih user-friendly",
        "Tambahkan notifikasi real-time untuk {feature}",
        "Sediakan dark mode untuk {product}",
        "Tingkatkan keamanan {feature} dengan biometric authentication",
        "Buat tutorial interaktif untuk fitur {feature}",
        "Tambahkan widget {product} di home screen",
        "Permudah proses {feature} di {channel}",
        "Sinkronisasi {product} dengan {channel} lebih cepat"
    ]
    
    # Generate 100 Suggestions
    for _ in range(100):
        product = random.choice(products)
        channel = random.choice(channels)
        platform = random.choice(social_media)
        feature = random.choice(features.get(product, ["General"]))
        suggestion_type = random.choice(suggestion_types)
        sentiment = random.choices(
            ["positive", "neutral"],
            weights=[0.7, 0.3]
        )[0]
        
        title = random.choice(suggestion_templates).format(
            product=product,
            feature=feature,
            channel=channel
        )
        
        data.append({
            "title": title,
            "source": platform,
            "summary": f"Customer suggestion for {feature} improvement in {product} via {channel}. Type: {suggestion_type['category']}. Potential high impact on user satisfaction.",
            "type": "suggestion",
            "product": product,
            "feature": feature,
            "channel": channel,
            "social_media": platform,
            "category": suggestion_type["category"],
            "sentiment": sentiment,
            "urgency_score": min(100, suggestion_type["priority_base"] + random.randint(-15, 15)),
            "date": get_random_date(30)
        })
    
    # Generate 20 General Insights (from AI analysis)
    insight_templates = [
        {
            "title": "Social Media Sentiment Trending Positive",
            "source": "AI Social Listening",
            "summary": "AI detected 15% increase in positive sentiment around {product} on {platform}. Main appreciation: {feature} improvements.",
            "category": "Social Media Intelligence"
        },
        {
            "title": "Customer Experience Excellence",
            "source": "AI Analytics Engine",
            "summary": "Customer satisfaction score for {product} via {channel} improved by 12%. Key driver: {feature} enhancement.",
            "category": "Customer Analytics"
        },
        {
            "title": "Product Innovation Opportunity",
            "source": "Market Intelligence Platform",
            "summary": "Market analysis shows high demand for {feature} in {product}. Recommendation: prioritize development.",
            "category": "Market Intelligence"
        },
        {
            "title": "Channel Performance Insight",
            "source": "Analytics Platform",
            "summary": "{channel} showing 20% increase in {product} adoption. {feature} is most used functionality.",
            "category": "Channel Analytics"
        },
        {
            "title": "Customer Journey Optimization",
            "source": "UX Analytics",
            "summary": "Users accessing {product} via {channel} show 30% faster completion for {feature}. Best practice identified.",
            "category": "UX Intelligence"
        }
    ]
    
    for _ in range(50):
        product = random.choice(products)
        channel = random.choice(channels)
        platform = random.choice(social_media)
        feature = random.choice(features.get(product, ["General"]))
        template = random.choice(insight_templates)
        sentiment = random.choices(
            ["positive", "neutral", "negative"],
            weights=[0.5, 0.3, 0.2]
        )[0]
        
        data.append({
            "title": template["title"],
            "source": template["source"],
            "summary": template["summary"].format(product=product, feature=feature, channel=channel, platform=platform),
            "type": "insight",
            "product": product,
            "feature": feature,
            "channel": channel,
            "social_media": platform,
            "category": template["category"],
            "sentiment": sentiment,
            "urgency_score": random.randint(40, 90),
            "date": get_random_date(15)
        })
    
    logger.info(f"Generated {len(data)} data points (50 complaints, 30 suggestions, 20 insights)")
    return data

def main():
    """Main scraper function"""
    logger.info("Starting BerInsight scraper...")
    logger.info(f"Data path: {DATA_PATH}")
    logger.info(f"Timezone: {TZ}")
    
    try:
        # Generate banking intelligence data
        insights_items = generate_banking_data()
        
        # Prepare output data
        insights_data = {
            "last_updated": get_jakarta_time(),
            "items": insights_items
        }
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(DATA_PATH) if os.path.dirname(DATA_PATH) else '.', exist_ok=True)
        
        # Save to file
        with open(DATA_PATH, "w", encoding='utf-8') as f:
            json.dump(insights_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Successfully saved {len(insights_items)} items to {DATA_PATH}")
        logger.info("Scraper completed successfully")
        
    except Exception as e:
        logger.error(f"Error in scraper: {e}")
        raise

if __name__ == "__main__":
    main()
