"""
Balance the distribution by adding more dummy data for non-Playstore platforms
"""

import json
import random
from datetime import datetime, timedelta

# Read existing data
data_path = '../data/insights.json'

with open(data_path, 'r') as f:
    data = json.load(f)

existing_insights = data['items']

# Calculate current distribution
current_distribution = {}
for item in existing_insights:
    platform = item.get('social_media', 'Unknown')
    current_distribution[platform] = current_distribution.get(platform, 0) + 1

print("Current distribution:")
total = len(existing_insights)
for platform, count in sorted(current_distribution.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / total) * 100
    print(f"  {platform}: {count} ({percentage:.1f}%)")

# Target: Add enough dummy data to balance distribution
# We want non-Playstore platforms to have more representation
# Target distribution: Playstore ~50%, Others ~50% combined

target_per_platform = 1200  # Target count for each non-Playstore platform

platforms_to_boost = {
    'Twitter': target_per_platform - current_distribution.get('Twitter', 0),
    'Facebook': target_per_platform - current_distribution.get('Facebook', 0),
    'Instagram': target_per_platform - current_distribution.get('Instagram', 0),
    'YouTube': target_per_platform - current_distribution.get('YouTube', 0),
    'Apple AppStore': target_per_platform - current_distribution.get('Apple AppStore', 0)
}

print(f"\nAdding dummy data to balance distribution:")
for platform, count_to_add in platforms_to_boost.items():
    print(f"  {platform}: adding {count_to_add} entries")

# Indonesian names for variety
first_names = [
    "Adi", "Ahmad", "Agus", "Andi", "Budi", "Bambang", "Citra", "Dewi", "Dian",
    "Eka", "Endang", "Fajar", "Fitri", "Gita", "Hendra", "Ika", "Indra", "Joko",
    "Kartika", "Lina", "Made", "Maya", "Nurul", "Omar", "Putri", "Raden", "Rina",
    "Sari", "Siti", "Tono", "Umar", "Vita", "Wati", "Yani", "Zahra"
]

last_names = [
    "Wijaya", "Santoso", "Pratama", "Kusuma", "Suryani", "Hartono", "Setiawan",
    "Permana", "Wibowo", "Budiman", "Sutrisno", "Rahayu", "Gunawan", "Hidayat"
]

products = ["BRImo", "Card", "Simpedes", "Britama", "Loan", "Deposito"]
features = ["Login", "Transfer", "QR Payment", "Top Up", "Account Info", "Performance", 
            "Customer Service", "General", "Withdrawal", "ATM"]
channels = ["BRImo", "BRILink", "Call Center", "Website", "ATM", "CERIA"]

# Review templates by sentiment
positive_templates = [
    "Sangat puas dengan layanan {product}. Fitur {feature} sangat membantu!",
    "{product} aplikasi terbaik! Fitur {feature} sangat berguna.",
    "Pelayanan {channel} sangat memuaskan. Terima kasih BRI!",
    "Suka banget dengan {feature}. {product} memudahkan transaksi saya.",
    "Recommended! {product} aplikasi yang wajib dimiliki. {feature} top!",
    "Mantap! {product} sangat user-friendly. {feature} mudah digunakan.",
    "Aplikasi {product} sangat membantu untuk transaksi sehari-hari.",
    "Terima kasih BRI untuk {product}. {feature} sangat inovatif!",
    "{product} adalah aplikasi banking terbaik yang pernah saya gunakan.",
    "Fitur {feature} di {product} sangat memudahkan. Mantap!"
]

neutral_templates = [
    "{product} cukup bagus, tapi {feature} perlu ditingkatkan.",
    "Aplikasi {product} oke, namun ada beberapa fitur yang bisa diperbaiki.",
    "Layanan {channel} cukup memuaskan, ada ruang untuk peningkatan.",
    "{feature} di {product} lumayan, tapi masih bisa lebih baik.",
    "Overall {product} bagus, mungkin {feature} bisa dioptimalkan lagi.",
    "{product} sudah bagus, tapi {feature} masih perlu perbaikan.",
    "Secara umum {product} memuaskan, namun {feature} bisa lebih responsive.",
    "{feature} cukup membantu, tapi UI/UX masih bisa ditingkatkan.",
]

negative_templates = [
    "{product} sering error di fitur {feature}. Mohon diperbaiki segera!",
    "Kecewa dengan {feature}. {product} sering bermasalah.",
    "Layanan {channel} mengecewakan. {feature} tidak berfungsi dengan baik.",
    "{product} perlu banyak perbaikan. {feature} sering crash.",
    "Sangat kecewa! {feature} di {product} tidak bisa diandalkan.",
    "{feature} error terus. Tolong perbaiki {product} ini!",
    "Aplikasi {product} lambat banget. {feature} susah diakses.",
    "{product} mengecewakan. {feature} sering gagal saat transaksi.",
    "Sudah berulang kali {feature} bermasalah. Kapan diperbaiki?",
    "{product} tidak stabil. {feature} sering hang dan force close."
]

# Generate balanced dummy data
dummy_insights = []
base_date = datetime.now()

for platform, count_to_add in platforms_to_boost.items():
    if count_to_add <= 0:
        continue
        
    for i in range(count_to_add):
        # Random rating and sentiment
        rating = random.choice([1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5])  # Weighted towards positive
        
        if rating >= 4:
            sentiment = "positive"
            templates = positive_templates
            types = ["insight", "suggestion"]
            categories = ["Positive Feedback", "Feature Request"]
            urgency = random.randint(10, 40)
        elif rating == 3:
            sentiment = "neutral"
            templates = neutral_templates
            types = ["suggestion", "insight"]
            categories = ["Feature Request", "General Feedback"]
            urgency = random.randint(40, 65)
        else:
            sentiment = "negative"
            templates = negative_templates
            types = ["complaint"]
            categories = ["Bug/Error", "Performance", "Service Issue"]
            urgency = random.randint(60, 90)
        
        product = random.choice(products)
        feature = random.choice(features)
        channel = random.choice(channels)
        
        review_template = random.choice(templates)
        review_text = review_template.format(product=product, feature=feature, channel=channel)
        
        user_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        summary = f"{user_name} ({rating}⭐): {review_text}"
        
        title = review_text[:80] + "..." if len(review_text) > 80 else review_text
        
        # Generate date (spread over last 12 months)
        days_ago = random.randint(1, 365)
        insight_date = (base_date - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        type_selected = random.choice(types)
        category = random.choice(categories)
        
        dummy_insight = {
            "title": title,
            "source": platform,
            "summary": summary,
            "type": type_selected,
            "product": product,
            "feature": feature,
            "channel": channel,
            "social_media": platform,
            "category": category,
            "sentiment": sentiment,
            "urgency_score": urgency,
            "date": insight_date,
            "rating": rating,
            "user": user_name
        }
        
        dummy_insights.append(dummy_insight)

print(f"\nGenerated {len(dummy_insights)} new dummy insights")

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

# Calculate new statistics
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

print(f"\n🌐 NEW Social Media Distribution:")
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

