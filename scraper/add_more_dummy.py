"""
Add more diverse dummy data to balance the distribution
"""

import json
import random
from datetime import datetime, timedelta

# Read existing data
data_path = '../data/insights.json'

with open(data_path, 'r') as f:
    data = json.load(f)

existing_insights = data['items']

# Expanded dummy data - more entries per category
social_media_platforms = [
    "Twitter", "Facebook", "Instagram", "YouTube", 
    "Google Playstore", "Apple AppStore"
]

channels = [
    "BRImo", "BRILink", "Call Center", "Website", "ATM", "CERIA"
]

products = [
    "BRImo", "Card", "Simpedes", "Britama", "Loan", "Deposito"
]

features = [
    "Login", "Transfer", "QR Payment", "Top Up", "Account Info",
    "Performance", "Customer Service", "General", "Withdrawal", "ATM"
]

# Generate templates for each combination
dummy_insights = []
base_date = datetime.now()

# Generate 500 diverse dummy insights
for i in range(500):
    social_media = random.choice(social_media_platforms)
    # Bias towards non-Playstore
    if random.random() < 0.7:  # 70% chance to pick non-Playstore
        social_media = random.choice(["Twitter", "Facebook", "Instagram", "YouTube"])
    
    channel = random.choice(channels)
    # Bias towards diverse channels
    if random.random() < 0.6:  # 60% chance to pick non-BRImo
        channel = random.choice(["BRILink", "Call Center", "Website", "ATM", "CERIA"])
    
    product = random.choice(products)
    feature = random.choice(features)
    
    # Random rating and sentiment
    rating = random.choice([1, 2, 3, 4, 5])
    if rating >= 4:
        sentiment = "positive"
        types = ["insight", "suggestion"]
        categories = ["Positive Feedback", "Feature Request"]
        urgency = random.randint(10, 40)
    elif rating == 3:
        sentiment = "neutral"
        types = ["suggestion", "insight"]
        categories = ["Feature Request", "General Feedback"]
        urgency = random.randint(40, 65)
    else:
        sentiment = "negative"
        types = ["complaint"]
        categories = ["Bug/Error", "Performance", "Service Issue"]
        urgency = random.randint(60, 90)
    
    type_selected = random.choice(types)
    category = random.choice(categories)
    
    # Generate date (spread over last 12 months)
    days_ago = random.randint(1, 365)
    insight_date = (base_date - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    
    # Generate random Indonesian names
    first_names = ["Ahmad", "Budi", "Citra", "Dewi", "Eka", "Fajar", "Gita", "Hendra", 
                   "Ika", "Joko", "Kartika", "Lina", "Made", "Nurul", "Omar", "Putri",
                   "Raden", "Siti", "Tono", "Umar", "Vita", "Wati", "Yani", "Zahra"]
    last_names = ["Wijaya", "Santoso", "Pratama", "Kusuma", "Suryani", "Hartono", 
                  "Setiawan", "Permana", "Wibowo", "Budiman", "Sutrisno", "Rahayu"]
    
    user_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    
    # Generate review text based on sentiment
    if sentiment == "positive":
        reviews = [
            f"Sangat puas dengan layanan {product}. {feature} sangat membantu!",
            f"{product} aplikasi terbaik! Fitur {feature} sangat berguna.",
            f"Pelayanan {channel} sangat memuaskan. Terima kasih BRI!",
            f"Suka banget dengan {feature}. {product} memudahkan transaksi saya.",
            f"Recommended! {product} aplikasi yang wajib dimiliki. {feature} top!"
        ]
    elif sentiment == "neutral":
        reviews = [
            f"{product} cukup bagus, tapi {feature} perlu ditingkatkan.",
            f"Aplikasi {product} oke, namun ada beberapa fitur yang bisa diperbaiki.",
            f"Layanan {channel} cukup memuaskan, ada ruang untuk peningkatan.",
            f"{feature} di {product} lumayan, tapi masih bisa lebih baik.",
            f"Overall {product} bagus, mungkin {feature} bisa dioptimalkan lagi."
        ]
    else:
        reviews = [
            f"{product} sering error di fitur {feature}. Mohon diperbaiki segera!",
            f"Kecewa dengan {feature}. {product} sering bermasalah.",
            f"Layanan {channel} mengecewakan. {feature} tidak berfungsi dengan baik.",
            f"{product} perlu banyak perbaikan. {feature} sering crash.",
            f"Sangat kecewa! {feature} di {product} tidak bisa diandalkan."
        ]
    
    review_text = random.choice(reviews)
    title = review_text[:80] + "..." if len(review_text) > 80 else review_text
    summary = f"{user_name} ({rating}⭐): {review_text}"
    
    dummy_insight = {
        "title": title,
        "source": social_media,
        "summary": summary,
        "type": type_selected,
        "product": product,
        "feature": feature,
        "channel": channel,
        "social_media": social_media,
        "category": category,
        "sentiment": sentiment,
        "urgency_score": urgency,
        "date": insight_date,
        "rating": rating,
        "user": user_name
    }
    
    dummy_insights.append(dummy_insight)

print(f"Generated {len(dummy_insights)} diverse dummy insights")

# Add dummy insights to existing data
existing_insights.extend(dummy_insights)

# Update metadata
data['items'] = existing_insights
data['total_insights'] = len(existing_insights)
data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M WIB')

# Update sources
sources_set = set()
for item in existing_insights:
    if 'social_media' in item and item['social_media']:
        sources_set.add(item['social_media'])

data['sources']['platforms'] = sorted(list(sources_set))

# Calculate statistics
sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
channel_counts = {}
social_media_counts = {}
type_counts = {}

for item in existing_insights:
    sentiment = item.get('sentiment', 'neutral')
    sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
    
    channel = item.get('channel', 'Unknown')
    channel_counts[channel] = channel_counts.get(channel, 0) + 1
    
    social = item.get('social_media', 'Unknown')
    social_media_counts[social] = social_media_counts.get(social, 0) + 1
    
    itype = item.get('type', 'insight')
    type_counts[itype] = type_counts.get(itype, 0) + 1

# Add summary
data['summary'] = {
    'sentiment_distribution': sentiment_counts,
    'channel_distribution': channel_counts,
    'social_media_distribution': social_media_counts,
    'type_distribution': type_counts,
    'total_positive': sentiment_counts['positive'],
    'total_negative': sentiment_counts['negative'],
    'total_neutral': sentiment_counts['neutral']
}

# Save updated data
with open(data_path, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Successfully updated insights.json")
print(f"📊 Total insights: {len(existing_insights)}")

print(f"\n🌐 Social Media Distribution:")
for platform, count in sorted(social_media_counts.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / len(existing_insights)) * 100
    print(f"  - {platform}: {count} ({percentage:.1f}%)")

print(f"\n🏢 Channel Distribution:")
for channel, count in sorted(channel_counts.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / len(existing_insights)) * 100
    print(f"  - {channel}: {count} ({percentage:.1f}%)")

print(f"\n😊 Sentiment Distribution:")
for sentiment, count in sentiment_counts.items():
    percentage = (count / len(existing_insights)) * 100
    print(f"  - {sentiment.capitalize()}: {count} ({percentage:.1f}%)")

print(f"\n📝 Type Distribution:")
for itype, count in type_counts.items():
    percentage = (count / len(existing_insights)) * 100
    print(f"  - {itype.capitalize()}: {count} ({percentage:.1f}%)")

