"""
Add dummy data to diversify social media and channel distribution
"""

import json
import random
from datetime import datetime, timedelta

# Read existing data
data_path = '../data/insights.json'

with open(data_path, 'r') as f:
    data = json.load(f)

existing_insights = data['items']

# Dummy data templates for diverse social media platforms
dummy_templates = [
    # Twitter
    {
        "social_media": "Twitter",
        "channel": "BRImo",
        "templates": [
            {
                "title": "Aplikasi BRImo sangat membantu transaksi harian saya",
                "summary": "@BRIMobile (5⭐): Aplikasi BRImo sangat membantu transaksi harian saya. Interface mudah digunakan dan fitur lengkap. Terima kasih BRI!",
                "sentiment": "positive",
                "type": "insight",
                "product": "BRImo",
                "feature": "General",
                "category": "Positive Feedback",
                "urgency_score": 20,
                "rating": 5
            },
            {
                "title": "Kenapa transfer antar bank di BRImo sering pending?",
                "summary": "@CustomerBRI (2⭐): Kenapa transfer antar bank di BRImo sering pending? Sudah 2 jam belum masuk ke rekening tujuan. Mohon diperbaiki.",
                "sentiment": "negative",
                "type": "complaint",
                "product": "BRImo",
                "feature": "Transfer",
                "category": "Bug/Error",
                "urgency_score": 75,
                "rating": 2
            }
        ]
    },
    # Instagram
    {
        "social_media": "Instagram",
        "channel": "BRImo",
        "templates": [
            {
                "title": "Suka banget sama fitur QR payment BRImo",
                "summary": "@bri_official (5⭐): Suka banget sama fitur QR payment BRImo! Praktis buat bayar di merchant. Keep up the good work! 👍",
                "sentiment": "positive",
                "type": "insight",
                "product": "BRImo",
                "feature": "QR Payment",
                "category": "Positive Feedback",
                "urgency_score": 25,
                "rating": 5
            },
            {
                "title": "BRImo sering logout sendiri, tolong fix bug ini",
                "summary": "@briuser (3⭐): BRImo sering logout sendiri, tolong fix bug ini. Harus login ulang terus, ribet.",
                "sentiment": "neutral",
                "type": "complaint",
                "product": "BRImo",
                "feature": "Login",
                "category": "Bug/Error",
                "urgency_score": 60,
                "rating": 3
            }
        ]
    },
    # Facebook
    {
        "social_media": "Facebook",
        "channel": "Call Center",
        "templates": [
            {
                "title": "Customer service BRI sangat membantu menyelesaikan masalah",
                "summary": "Ahmad Wijaya (5⭐): Customer service BRI sangat membantu menyelesaikan masalah kartu ATM saya yang terblokir. Pelayanan ramah dan profesional.",
                "sentiment": "positive",
                "type": "insight",
                "product": "Card",
                "feature": "Customer Service",
                "category": "Positive Feedback",
                "urgency_score": 20,
                "rating": 5
            },
            {
                "title": "Call center susah dihubungi, selalu busy",
                "summary": "Budi Santoso (2⭐): Call center susah dihubungi, selalu busy. Sudah coba berkali-kali tetap tidak tersambung. Mohon ditingkatkan.",
                "sentiment": "negative",
                "type": "complaint",
                "product": "General",
                "feature": "Customer Service",
                "category": "Service Issue",
                "urgency_score": 70,
                "rating": 2
            }
        ]
    },
    # YouTube
    {
        "social_media": "YouTube",
        "channel": "BRImo",
        "templates": [
            {
                "title": "Tutorial BRImo di YouTube sangat jelas dan membantu",
                "summary": "Rina Wati (5⭐): Tutorial BRImo di YouTube sangat jelas dan membantu. Saya yang gaptek jadi bisa pakai aplikasi dengan mudah. Terima kasih BRI!",
                "sentiment": "positive",
                "type": "insight",
                "product": "BRImo",
                "feature": "General",
                "category": "Positive Feedback",
                "urgency_score": 15,
                "rating": 5
            },
            {
                "title": "Fitur tarik tunai tanpa kartu kok error terus?",
                "summary": "Dedi Kurniawan (2⭐): Fitur tarik tunai tanpa kartu kok error terus? Padahal saldo cukup. Mohon perbaiki fitur ini.",
                "sentiment": "negative",
                "type": "complaint",
                "product": "BRImo",
                "feature": "Withdrawal",
                "category": "Bug/Error",
                "urgency_score": 80,
                "rating": 2
            }
        ]
    },
    # BRILink Channel
    {
        "social_media": "Google Playstore",
        "channel": "BRILink",
        "templates": [
            {
                "title": "BRILink agent di desa saya sangat membantu",
                "summary": "Siti Aminah (5⭐): BRILink agent di desa saya sangat membantu. Transaksi jadi mudah tanpa harus ke kota. Semoga makin banyak agent BRILink.",
                "sentiment": "positive",
                "type": "insight",
                "product": "BRILink",
                "feature": "General",
                "category": "Positive Feedback",
                "urgency_score": 20,
                "rating": 5
            },
            {
                "title": "Sistem BRILink sering offline, menyulitkan transaksi",
                "summary": "Pak RT (2⭐): Sistem BRILink sering offline, menyulitkan transaksi warga. Tolong stabilkan sistemnya.",
                "sentiment": "negative",
                "type": "complaint",
                "product": "BRILink",
                "feature": "Performance",
                "category": "Bug/Error",
                "urgency_score": 75,
                "rating": 2
            }
        ]
    },
    # Website Channel
    {
        "social_media": "Twitter",
        "channel": "Website",
        "templates": [
            {
                "title": "Website BRI informatif dan mudah digunakan",
                "summary": "@briweb_user (4⭐): Website BRI informatif dan mudah digunakan. Info produk lengkap dan desain modern.",
                "sentiment": "positive",
                "type": "insight",
                "product": "General",
                "feature": "General",
                "category": "Positive Feedback",
                "urgency_score": 25,
                "rating": 4
            },
            {
                "title": "Website BRI loading lambat saat jam sibuk",
                "summary": "@webuser (3⭐): Website BRI loading lambat saat jam sibuk. Tolong optimasi server untuk traffic tinggi.",
                "sentiment": "neutral",
                "type": "suggestion",
                "product": "General",
                "feature": "Performance",
                "category": "Performance",
                "urgency_score": 55,
                "rating": 3
            }
        ]
    },
    # ATM Channel
    {
        "social_media": "Facebook",
        "channel": "ATM",
        "templates": [
            {
                "title": "ATM BRI tersebar luas dan mudah diakses",
                "summary": "Ibu Ratna (5⭐): ATM BRI tersebar luas dan mudah diakses. Di mana-mana ada, sangat memudahkan.",
                "sentiment": "positive",
                "type": "insight",
                "product": "Card",
                "feature": "General",
                "category": "Positive Feedback",
                "urgency_score": 15,
                "rating": 5
            },
            {
                "title": "ATM sering error dan makan kartu",
                "summary": "Bambang Setiawan (1⭐): ATM sering error dan makan kartu. Sudah 3 kali kejadian, sangat merepotkan!",
                "sentiment": "negative",
                "type": "complaint",
                "product": "Card",
                "feature": "ATM",
                "category": "Bug/Error",
                "urgency_score": 85,
                "rating": 1
            }
        ]
    },
    # CERIA Channel
    {
        "social_media": "Instagram",
        "channel": "CERIA",
        "templates": [
            {
                "title": "CERIA memudahkan cek saldo via SMS",
                "summary": "@ceria_user (4⭐): CERIA memudahkan cek saldo via SMS. Praktis tanpa perlu buka aplikasi.",
                "sentiment": "positive",
                "type": "insight",
                "product": "CERIA",
                "feature": "Account Info",
                "category": "Positive Feedback",
                "urgency_score": 20,
                "rating": 4
            }
        ]
    },
    # Deposito Product
    {
        "social_media": "Facebook",
        "channel": "Website",
        "templates": [
            {
                "title": "Bunga deposito BRI kompetitif",
                "summary": "Hendra Wijaya (5⭐): Bunga deposito BRI kompetitif dibanding bank lain. Proses pembukaan juga mudah.",
                "sentiment": "positive",
                "type": "insight",
                "product": "Deposito",
                "feature": "General",
                "category": "Positive Feedback",
                "urgency_score": 20,
                "rating": 5
            }
        ]
    },
    # Loan Product
    {
        "social_media": "Twitter",
        "channel": "Call Center",
        "templates": [
            {
                "title": "KUR BRI sangat membantu UMKM",
                "summary": "@umkm_id (5⭐): KUR BRI sangat membantu UMKM seperti saya. Bunga ringan dan proses cepat. Terima kasih BRI!",
                "sentiment": "positive",
                "type": "insight",
                "product": "Loan",
                "feature": "General",
                "category": "Positive Feedback",
                "urgency_score": 15,
                "rating": 5
            },
            {
                "title": "Proses pengajuan KUR terlalu lama",
                "summary": "@kur_applicant (3⭐): Proses pengajuan KUR terlalu lama, sudah 2 minggu belum ada kabar. Mohon dipercepat.",
                "sentiment": "neutral",
                "type": "complaint",
                "product": "Loan",
                "feature": "General",
                "category": "Service Issue",
                "urgency_score": 60,
                "rating": 3
            }
        ]
    },
    # Simpedes Product
    {
        "social_media": "Facebook",
        "channel": "BRILink",
        "templates": [
            {
                "title": "Simpedes cocok untuk tabungan harian",
                "summary": "Ibu Sari (4⭐): Simpedes cocok untuk tabungan harian. Biaya admin murah dan mudah diakses.",
                "sentiment": "positive",
                "type": "insight",
                "product": "Simpedes",
                "feature": "General",
                "category": "Positive Feedback",
                "urgency_score": 20,
                "rating": 4
            }
        ]
    },
    # Britama Product
    {
        "social_media": "Instagram",
        "channel": "Website",
        "templates": [
            {
                "title": "Britama benefit banyak untuk transaksi bisnis",
                "summary": "@bisnis_owner (5⭐): Britama benefit banyak untuk transaksi bisnis. Limit tinggi dan fitur lengkap.",
                "sentiment": "positive",
                "type": "insight",
                "product": "Britama",
                "feature": "General",
                "category": "Positive Feedback",
                "urgency_score": 20,
                "rating": 5
            }
        ]
    }
]

# Generate dummy insights
dummy_insights = []
base_date = datetime.now()

for idx, template_group in enumerate(dummy_templates):
    social_media = template_group['social_media']
    channel = template_group['channel']
    
    for template_idx, template in enumerate(template_group['templates']):
        # Generate date (spread over last 6 months)
        days_ago = random.randint(1, 180)
        insight_date = (base_date - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        dummy_insight = {
            "title": template['title'],
            "source": social_media,
            "summary": template['summary'],
            "type": template['type'],
            "product": template['product'],
            "feature": template['feature'],
            "channel": channel,
            "social_media": social_media,
            "category": template['category'],
            "sentiment": template['sentiment'],
            "urgency_score": template['urgency_score'],
            "date": insight_date,
            "rating": template['rating'],
            "user": template['summary'].split('(')[0].strip()
        }
        
        dummy_insights.append(dummy_insight)

print(f"Generated {len(dummy_insights)} dummy insights")

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
data['sources']['total_files'] = data['sources'].get('total_files', 4)

# Calculate statistics
sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
channel_counts = {}
social_media_counts = {}

for item in existing_insights:
    sentiment = item.get('sentiment', 'neutral')
    sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
    
    channel = item.get('channel', 'Unknown')
    channel_counts[channel] = channel_counts.get(channel, 0) + 1
    
    social = item.get('social_media', 'Unknown')
    social_media_counts[social] = social_media_counts.get(social, 0) + 1

# Add summary
data['summary'] = {
    'sentiment_distribution': sentiment_counts,
    'channel_distribution': channel_counts,
    'social_media_distribution': social_media_counts,
    'total_positive': sentiment_counts['positive'],
    'total_negative': sentiment_counts['negative'],
    'total_neutral': sentiment_counts['neutral']
}

# Save updated data
with open(data_path, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Successfully updated insights.json")
print(f"Total insights: {len(existing_insights)}")
print(f"\n📊 Social Media Distribution:")
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

