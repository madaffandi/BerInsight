import pandas as pd
import json
import re
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
import os

# Keywords for feature detection
FEATURE_KEYWORDS = {
    "Login": ["login", "masuk", "sign in", "username", "password", "fingerprint", "biometric"],
    "Transfer": ["transfer", "kirim", "tf", "trf", "send money"],
    "QR Payment": ["qris", "qr", "scan", "barcode"],
    "Top Up": ["top up", "isi ulang", "topup", "e-wallet", "gopay", "ovo", "dana", "shopeepay"],
    "Bill Payment": ["bayar", "tagihan", "listrik", "pdam", "bpjs", "telkom", "token", "pbb"],
    "Account Info": ["saldo", "balance", "mutasi", "rekening", "account"],
    "Notification": ["notif", "notifikasi", "pemberitahuan", "push notification"],
    "Performance": ["lemot", "lambat", "lag", "slow", "loading", "lama", "eror", "error", "crash", "force close"],
    "Security": ["keamanan", "security", "hack", "penipuan", "fraud", "otp"],
    "UI/UX": ["tampilan", "interface", "ui", "ux", "design", "navigasi"],
    "Withdrawal": ["tarik tunai", "withdraw", "atm", "cardless"],
    "Customer Service": ["cs", "customer service", "call center", "bantuan", "help", "support"],
    "Card": ["kartu", "card", "kredit", "debit", "brizzi"],
    "Brizzi": ["brizzi", "e-money", "nfc"],
    "Virtual Account": ["va", "virtual account", "briva"]
}

PRODUCT_KEYWORDS = {
    "BRImo": ["brimo", "aplikasi"],
    "Card": ["kartu", "card", "brizzi", "kredit", "debit"],
    "Simpedes": ["simpedes"],
    "Britama": ["britama"],
    "Loan": ["kredit", "pinjaman", "loan", "kpr"],
    "Deposito": ["deposito", "deposit"]
}

CHANNEL_KEYWORDS = {
    "BRImo": ["brimo", "mobile", "aplikasi"],
    "ATM": ["atm", "mesin"],
    "Call Center": ["call center", "cs", "customer service", "telepon", "1500017"],
    "BRILink": ["brilink", "agen"],
    "Website": ["website", "web", "browser", "internet banking"]
}

CATEGORY_KEYWORDS = {
    "Bug/Error": ["error", "eror", "crash", "force close", "gagal", "bug", "rusak", "tidak bisa"],
    "Performance Issue": ["lemot", "lambat", "lag", "slow", "loading lama"],
    "Security Concern": ["keamanan", "security", "hack", "penipuan", "fraud"],
    "UI/UX Problem": ["tampilan", "interface", "ui", "ux", "design", "navigasi"],
    "Service Unavailable": ["tidak bisa", "ga bisa", "cannot", "unavailable", "down"],
    "Transaction Failed": ["transaksi gagal", "transfer gagal", "failed", "saldo terpotong"],
    "Poor Customer Service": ["cs", "customer service buruk", "tidak responsif"],
    "Feature Request": ["tambahkan", "add", "minta", "request", "saran", "suggestion"],
    "Payment Issue": ["bayar", "payment", "qris", "pembayaran"]
}

def get_jakarta_time() -> str:
    """Get current time in Jakarta timezone"""
    jakarta_tz = timezone(timedelta(hours=7))
    now = datetime.now(jakarta_tz)
    return now.strftime('%Y-%m-%d %H:%M WIB')

def parse_date(date_str: str) -> str:
    """Parse date string to YYYY-MM-DD format"""
    try:
        if pd.isna(date_str):
            return datetime.now().strftime('%Y-%m-%d')
        
        # Try parsing ISO format
        date_obj = pd.to_datetime(date_str)
        return date_obj.strftime('%Y-%m-%d')
    except:
        return datetime.now().strftime('%Y-%m-%d')

def detect_keywords(text: str, keyword_dict: Dict[str, List[str]]) -> str:
    """Detect which category text belongs to based on keywords"""
    if not text or pd.isna(text):
        return "General"
    
    text_lower = str(text).lower()
    matches = {}
    
    for category, keywords in keyword_dict.items():
        count = sum(1 for keyword in keywords if keyword in text_lower)
        if count > 0:
            matches[category] = count
    
    if matches:
        return max(matches, key=matches.get)
    return "General"

def get_sentiment_from_rating(rating: int) -> str:
    """Convert rating to sentiment"""
    try:
        rating = int(rating)
        if rating <= 2:
            return "negative"
        elif rating == 3:
            return "neutral"
        else:
            return "positive"
    except:
        return "neutral"

def get_urgency_score(rating: int, category: str) -> int:
    """Calculate urgency score based on rating and category"""
    base_score = 50
    
    # Adjust by rating
    if rating <= 2:
        base_score += 30
    elif rating == 3:
        base_score += 10
    
    # Adjust by category
    urgency_map = {
        "Bug/Error": 85,
        "Security Concern": 95,
        "Service Unavailable": 90,
        "Transaction Failed": 95,
        "Performance Issue": 70,
        "Payment Issue": 80,
        "Poor Customer Service": 60,
        "UI/UX Problem": 50,
        "Feature Request": 40
    }
    
    if category in urgency_map:
        base_score = urgency_map[category]
    
    return min(100, base_score)

def determine_type(rating: int, text: str, category: str) -> str:
    """Determine if it's a complaint, suggestion, or insight"""
    if not text or pd.isna(text):
        return "complaint" if rating <= 3 else "insight"
    
    text_lower = str(text).lower()
    
    suggestion_words = ["tambahkan", "add", "saran", "suggestion", "request", "minta", "harusnya", "seharusnya", "tolong", "mohon"]
    if any(word in text_lower for word in suggestion_words) and rating >= 3:
        return "suggestion"
    
    if rating <= 3 or category in ["Bug/Error", "Performance Issue", "Service Unavailable", "Transaction Failed", "Poor Customer Service"]:
        return "complaint"
    
    return "insight"

def clean_text(text: str) -> str:
    """Clean and truncate text"""
    if not text or pd.isna(text):
        return "No review text provided"
    
    text = str(text).strip()
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Truncate if too long
    if len(text) > 300:
        text = text[:297] + "..."
    return text

def process_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """Process a single CSV file and convert to insights format"""
    print(f"\n📂 Processing: {file_path}")
    
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except:
        try:
            df = pd.read_csv(file_path, encoding='latin-1')
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return []
    
    print(f"   Found {len(df)} rows")
    
    insights = []
    source_platform = "Google Playstore"  # Default
    
    # Detect source from filename
    filename = os.path.basename(file_path).lower()
    if "ios" in filename or "appstore" in filename or "apple" in filename:
        source_platform = "Apple AppStore"
    
    for idx, row in df.iterrows():
        try:
            # Skip if no review text
            if pd.isna(row.get('Review Text')) or str(row.get('Review Text')).strip() == '':
                continue
            
            rating = int(row.get('Rating', 3))
            review_text = clean_text(row.get('Review Text'))
            date = parse_date(row.get('Date'))
            user_name = str(row.get('User Name', 'Anonymous')).strip()
            
            # Detect features, products, categories
            feature = detect_keywords(review_text, FEATURE_KEYWORDS)
            product = detect_keywords(review_text, PRODUCT_KEYWORDS)
            channel = detect_keywords(review_text, CHANNEL_KEYWORDS)
            category = detect_keywords(review_text, CATEGORY_KEYWORDS)
            
            # Default to BRImo if no specific product detected
            if product == "General":
                product = "BRImo"
            
            # Get sentiment and type
            sentiment = get_sentiment_from_rating(rating)
            insight_type = determine_type(rating, review_text, category)
            urgency_score = get_urgency_score(rating, category)
            
            # Create title (first 100 chars or summary)
            title = review_text[:100] if len(review_text) > 100 else review_text
            if len(review_text) > 100:
                title = title.rsplit(' ', 1)[0] + "..."
            
            # Create insight object
            insight = {
                "title": title,
                "source": source_platform,
                "summary": f"{user_name} ({rating}⭐): {review_text}",
                "type": insight_type,
                "product": product,
                "feature": feature,
                "channel": channel,
                "social_media": source_platform,
                "category": category,
                "sentiment": sentiment,
                "urgency_score": urgency_score,
                "date": date,
                "rating": rating,
                "user": user_name
            }
            
            insights.append(insight)
            
        except Exception as e:
            print(f"   ⚠️  Error processing row {idx}: {e}")
            continue
    
    print(f"   ✅ Processed {len(insights)} valid insights")
    return insights

def convert_csv_to_insights(csv_files: List[str], output_path: str):
    """Convert multiple CSV files to insights.json format"""
    print("=" * 60)
    print("🚀 BerInsight CSV to Insights Converter")
    print("=" * 60)
    
    all_insights = []
    
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            print(f"❌ File not found: {csv_file}")
            continue
        
        insights = process_csv_file(csv_file)
        all_insights.extend(insights)
    
    # Sort by date (most recent first)
    all_insights.sort(key=lambda x: x['date'], reverse=True)
    
    # Create final output
    output_data = {
        "last_updated": get_jakarta_time(),
        "total_insights": len(all_insights),
        "sources": {
            "total_files": len(csv_files),
            "platforms": list(set(insight['social_media'] for insight in all_insights))
        },
        "items": all_insights
    }
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print("✅ CONVERSION COMPLETE")
    print("=" * 60)
    print(f"📊 Total Insights: {len(all_insights)}")
    print(f"📁 Output: {output_path}")
    print(f"📅 Last Updated: {get_jakarta_time()}")
    
    # Print summary statistics
    print("\n📈 Summary Statistics:")
    print(f"   • Complaints: {sum(1 for i in all_insights if i['type'] == 'complaint')}")
    print(f"   • Suggestions: {sum(1 for i in all_insights if i['type'] == 'suggestion')}")
    print(f"   • Insights: {sum(1 for i in all_insights if i['type'] == 'insight')}")
    print(f"\n   • Positive: {sum(1 for i in all_insights if i['sentiment'] == 'positive')}")
    print(f"   • Neutral: {sum(1 for i in all_insights if i['sentiment'] == 'neutral')}")
    print(f"   • Negative: {sum(1 for i in all_insights if i['sentiment'] == 'negative')}")
    
    # Top features
    feature_counts = {}
    for insight in all_insights:
        feature = insight['feature']
        feature_counts[feature] = feature_counts.get(feature, 0) + 1
    
    print(f"\n🔥 Top 5 Features:")
    for feature, count in sorted(feature_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   • {feature}: {count} mentions")
    
    print("=" * 60)

if __name__ == "__main__":
    # Define CSV file paths (relative to Downloads folder)
    downloads_path = os.path.expanduser("~/Downloads")
    
    csv_files = [
        os.path.join(downloads_path, "reviews-ios (1).csv"),
        os.path.join(downloads_path, "reviews (1).csv"),
        os.path.join(downloads_path, "android-brimo-reviews-2024-2025.csv"),
        os.path.join(downloads_path, "1_10_brimo_appstore_reviews.csv")
    ]
    
    # Output path
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "insights.json")
    
    # Convert
    convert_csv_to_insights(csv_files, output_path)
    
    print("\n✨ Ready to use with BerInsight!")
    print("   Run your API server and frontend to see the real data.\n")

