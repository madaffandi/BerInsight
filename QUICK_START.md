# 🚀 Quick Start - BerInsight Dashboard

## Servers are Running!

✅ **Frontend:** http://localhost:3000
✅ **API:** http://localhost:8000

## Apa yang Baru? 🎉

### 1. **Main Analytics Grid (3 Kolom)**

```
┌──────────────────┬──────────────────┬──────────────────┐
│   KIRI (LEFT)    │  TENGAH (CENTER) │  KANAN (RIGHT)   │
├──────────────────┼──────────────────┼──────────────────┤
│ Social Media     │ Product Analysis │ Channel Distrib. │
│ Feedback         │                  │                  │
│                  │                  │                  │
│ Bar Chart:       │ Doughnut Chart:  │ Bar Chart:       │
│ - YouTube        │ - BRImo          │ - BRImo          │
│ - Instagram      │ - Card           │ - BRILink        │
│ - Twitter        │ - Qlola          │ - CERIA          │
│ - Facebook       │ - Loan           │ - Qlola          │
│ - AppStore       │ - Simpedes       │ - MMS            │
│ - Playstore      │ - Britama        │ - Sabrina        │
│                  │ - Deposito       │                  │
└──────────────────┴──────────────────┴──────────────────┘
```

### 2. **Sentiment Analysis Section**

```
┌─────────────────────────────────────────────────┐
│         Sentiment Analysis                      │
│                                                 │
│  [Pie Chart]         Positive: 5,395 (65%)     │
│                      Neutral:  2,075 (25%)     │
│                      Negative:   830 (10%)     │
└─────────────────────────────────────────────────┘
```

### 3. **Most Keywords Section**

```
┌─────────────────────────────────────────────────┐
│         Most Mentioned Keywords                 │
│                                                 │
│  [Transfer] [Login] [Payment] [Error] [Slow]   │
│  [QR] [Account] [Balance] [Security] [Update]  │
└─────────────────────────────────────────────────┘
```

### 4. **Highlighted Ideas Section**

```
┌─────────────────────────────────────────────────┐
│      Highlighted Ideas & Suggestions            │
│                                                 │
│  ┌─────────────────┬─────────────────┐         │
│  │ Dark Mode       │ Biometric Auth  │         │
│  │ [High Priority] │ [Medium]        │         │
│  │ BRImo           │ Card            │         │
│  │ 📱 45 mentions  │ 🔐 32 mentions  │         │
│  └─────────────────┴─────────────────┘         │
└─────────────────────────────────────────────────┘
```

## Cara Lihat Dashboard

1. **Buka browser:** http://localhost:3000

2. **Scroll untuk melihat:**
   - ⬆️ Top: 4 metric cards (Total Feedback, Customer Satisfaction, etc.)
   - 📊 Main Grid: 3 charts (Social Media | Products | Channels)
   - 😊 Sentiment Analysis dengan pie chart
   - 🏷️ Keywords dengan purple gradient tags
   - 💡 Highlighted Ideas dengan priority badges
   - 📝 Customer Insights cards di bottom

## Struktur Data Baru

```json
{
  "title": "Customer service di BRImo tidak responsif untuk masalah Loan",
  "source": "Apple AppStore",        // ← Social Media Platform
  "product": "Loan",                 // ← BRI Product
  "channel": "BRImo",                // ← BRI Channel
  "sentiment": "negative",           // ← Sentiment
  "category": "Security Concern"
}
```

## Features yang Sudah Ada ✅

- ✅ Social Media breakdown (6 platforms)
- ✅ Product categorization (7 products)
- ✅ Channel distribution (6 channels)
- ✅ Sentiment analysis (Positive/Neutral/Negative)
- ✅ Top keywords dengan hover effects
- ✅ Highlighted ideas dengan priority system
- ✅ Enhanced insights cards dengan badges
- ✅ Responsive design (mobile-friendly)

## Troubleshooting

### Jika dashboard tidak muncul:

1. **Check API Status:**
   ```bash
   curl http://localhost:8000/healthz
   ```

2. **Check Data:**
   ```bash
   curl http://localhost:8000/insights
   ```

3. **Restart Frontend:**
   ```bash
   cd fe
   npm run dev
   ```

4. **Clear Browser Cache:**
   - Chrome: Ctrl+Shift+R (Windows) / Cmd+Shift+R (Mac)
   - Hard refresh

### Jika chart tidak muncul:

1. Check console for errors (F12)
2. Pastikan Chart.js loaded
3. Refresh halaman

## Data yang Tersedia

- **Total Items:** 100
  - 50 Complaints
  - 30 Suggestions
  - 20 Insights

- **Time Range:** Last 30 days
- **Platforms:** All 6 social media platforms
- **Products:** All 7 BRI products
- **Channels:** All 6 BRI channels

## Next Steps

Kalau mau customize:
- Edit data di `/data/insights.json`
- Atau run scraper: `cd scraper && DATA_PATH=../data/insights.json python3 main.py`
- Refresh dashboard

---

**Dashboard URL:** http://localhost:3000
**API Docs:** http://localhost:8000/docs

