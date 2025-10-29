# 🚀 Cara Buka BerInsight Dashboard

## ✅ Status Server

Kedua server sudah berjalan:

- **API Server:** http://localhost:8000
- **Frontend:** http://localhost:3000

---

## 🌐 URL Dashboard Yang BENAR:

# http://localhost:3000/BerInsight/

⬆️ **PENTING:** Perhatikan ada `/BerInsight/` di akhir!

---

## Kalau "Connection Refused" atau Error:

### 1. Check apakah server masih jalan:

```bash
# Check API (harus return: {"status":"ok",...})
curl http://localhost:8000/healthz

# Check Frontend (harus return HTML)
curl http://localhost:3000/BerInsight/
```

### 2. Kalau API tidak jalan, restart:

```bash
cd /Users/achmadaffandi/FNDLABS/cursor/BerInsight/api
DATA_PATH=/Users/achmadaffandi/FNDLABS/cursor/BerInsight/data/insights.json \
python3 -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

### 3. Kalau Frontend tidak jalan, restart:

```bash
cd /Users/achmadaffandi/FNDLABS/cursor/BerInsight/fe
PORT=3000 npm run dev
```

### 4. Kalau ada port conflict (Address already in use):

```bash
# Kill process di port yang bentrok
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# Tunggu 2 detik
sleep 2

# Restart servers
```

---

## Yang Akan Kamu Lihat di Dashboard:

### 📊 **Main Grid (3 Kolom)**

```
┌─────────────────────┬─────────────────────┬─────────────────────┐
│  LEFT               │  CENTER             │  RIGHT              │
│  Social Media       │  Product            │  Channel            │
│  Feedback           │  Analysis           │  Distribution       │
│  ─────────────────  │  ─────────────────  │  ─────────────────  │
│                     │                     │                     │
│  Bar Chart:         │  Doughnut Chart:    │  Bar Chart:         │
│  📺 YouTube         │  📱 BRImo           │  📱 BRImo           │
│  📷 Instagram       │  💳 Card            │  🏪 BRILink         │
│  🐦 Twitter         │  🛍️ Qlola           │  📞 CERIA           │
│  📘 Facebook        │  💰 Loan            │  🛒 Qlola           │
│  🍎 AppStore        │  🏦 Simpedes        │  💬 MMS             │
│  🤖 Playstore       │  💼 Britama         │  🤖 Sabrina         │
│                     │  💵 Deposito        │                     │
└─────────────────────┴─────────────────────┴─────────────────────┘
```

### 😊 **Sentiment Analysis**
- Pie chart dengan breakdown:
  - 🟢 Positive: 65% (5,395)
  - 🟡 Neutral: 25% (2,075)
  - 🔴 Negative: 10% (830)

### 🏷️ **Most Keywords**
Purple gradient tags dengan hover effect:
- Transfer • Login • Payment • Error • Slow • QR • Account • Balance

### 💡 **Highlighted Ideas**
3 featured idea cards:
- 🌙 Dark Mode (High Priority - BRImo)
- 🔐 Biometric Auth (Medium Priority - Card)
- 💰 Cashback Program (High Priority - Qlola)

### 📝 **Customer Insights**
6 insight cards dengan:
- Type badges (complaint/suggestion/insight)
- Sentiment indicators
- Source platform

---

## Troubleshooting Browser:

### Kalau masih blank/tidak muncul chart:

1. **Hard Refresh:**
   - Mac: `Cmd + Shift + R`
   - Windows: `Ctrl + Shift + R`

2. **Clear Cache:**
   - Chrome: Settings → Privacy → Clear browsing data

3. **Buka di Incognito:**
   - Chrome: `Cmd/Ctrl + Shift + N`

4. **Check Browser Console (F12):**
   - Lihat ada error merah tidak
   - Kalau ada CORS error, pastikan API jalan

---

## Quick Check Commands:

```bash
# Check semua ports
lsof -i:3000  # Frontend should be running
lsof -i:8000  # API should be running

# Test API
curl http://localhost:8000/healthz
curl http://localhost:8000/insights | head -50

# Test Frontend
curl http://localhost:3000/BerInsight/ | head -20
```

---

## URLs Lengkap:

- **Dashboard:** http://localhost:3000/BerInsight/
- **API Health:** http://localhost:8000/healthz
- **API Insights:** http://localhost:8000/insights
- **API Docs:** http://localhost:8000/docs

---

## Data Structure Baru:

Setiap item sekarang punya:
```json
{
  "title": "Customer complaint/suggestion",
  "source": "YouTube",           // Social Media Platform ✨
  "product": "BRImo",            // BRI Product ✨
  "channel": "BRILink",          // BRI Channel ✨
  "sentiment": "positive",       // Sentiment ✨
  "type": "complaint",
  "category": "Performance Issue"
}
```

Total: **100 items** (50 complaints + 30 suggestions + 20 insights)

---

**INGAT:** URL yang benar adalah http://localhost:3000/BerInsight/ (dengan /BerInsight/ di akhir!)

