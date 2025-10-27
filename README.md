# BRInsight - Banking Intelligence Dashboard

A modern, AI-powered banking intelligence platform for social media monitoring, risk assessment, and fraud detection. Built for hackathon demo with React/Next.js frontend, FastAPI backend, and Python data scraper.

## 🏗️ Architecture

```
brinsight/
├── fe/                 # Next.js Frontend (Static Export)
├── api/                # FastAPI Backend
├── scraper/            # Python Data Scraper
├── data/               # Shared Persistent Storage
└── README.md
```

## 🚀 Quick Start (Local Development)

### Prerequisites
- Node.js 18+ 
- Python 3.11+
- Git

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd brinsight
cp env.example .env
```

### 2. Frontend (Next.js)
```bash
cd fe
npm install
npm run dev          # Development server on http://localhost:3000
npm run build        # Build for production
npm run start        # Serve static build
```

### 3. Backend API (FastAPI)
```bash
cd api
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
# API available at http://localhost:8000
```

### 4. Data Scraper (Python)
```bash
cd scraper
pip install -r requirements.txt
python main.py
# Creates/updates /data/insights.json
```

### 5. Test the System
1. Start the API: `cd api && uvicorn app:app --host 0.0.0.0 --port 8000`
2. Run scraper: `cd scraper && python main.py`
3. Start frontend: `cd fe && npm run dev`
4. Visit http://localhost:3000

## 🚂 Railway Deployment

### 1. Create Railway Project
1. Go to [Railway.app](https://railway.app)
2. Create new project
3. Connect your GitHub repository

### 2. Deploy Services

#### Frontend Service
- **Service Type**: Nixpacks (Auto-detect)
- **Root Directory**: `fe/`
- **Build Command**: `npm run build`
- **Start Command**: `npm run start`
- **Environment Variables**:
  - `NEXT_PUBLIC_API_BASE`: `https://your-api-service.up.railway.app`

#### API Service
- **Service Type**: Dockerfile
- **Root Directory**: `api/`
- **Dockerfile**: `api/Dockerfile`
- **Port**: `8000`
- **Environment Variables**:
  - `DATA_PATH`: `/data/insights.json`
  - `TZ`: `Asia/Jakarta`

#### Scraper Service
- **Service Type**: Dockerfile
- **Root Directory**: `scraper/`
- **Dockerfile**: `scraper/Dockerfile`
- **No Port** (Cron job)
- **Environment Variables**:
  - `DATA_PATH`: `/data/insights.json`
  - `TZ`: `Asia/Jakarta`

### 3. Setup Persistent Storage
1. Add **Persistent Volume** to your project
2. Mount to `/data` on both `api` and `scraper` services
3. This allows data sharing between API and scraper

### 4. Setup Cron Job
1. Go to scraper service settings
2. Add **Cron Job**:
   - **Schedule**: `*/10 * * * *` (every 10 minutes)
   - **Command**: `python main.py`

### 5. Environment Variables Checklist
```
Project-wide:
✅ TZ=Asia/Jakarta

Frontend:
✅ NEXT_PUBLIC_API_BASE=https://your-api-service.up.railway.app

API:
✅ DATA_PATH=/data/insights.json

Scraper:
✅ DATA_PATH=/data/insights.json
```

## 📊 Features

### Frontend Dashboard
- **Real-time Status**: API health and last updated time
- **Interactive Charts**: Line, Bar, and Doughnut charts
- **Key Metrics**: Revenue, users, orders, conversion rate
- **Insights Feed**: Dynamic insights from scraper
- **Offline Fallback**: Graceful degradation with cached data
- **Responsive Design**: Mobile-first, fullscreen layout

### API Endpoints
- `GET /healthz` - Health check with timestamp
- `GET /insights` - Business insights data
- `GET /` - API information

### Data Scraper
- **Retry Logic**: 3 attempts with exponential backoff
- **Timeout Handling**: 5-second timeouts
- **Mock Data**: Fallback when external APIs fail
- **Atomic Writes**: Safe file operations
- **Timezone Support**: Asia/Jakarta (UTC+7)

## 🔧 Configuration

### Environment Variables
See `env.example` for all required variables.

### Data Format
```json
{
  "last_updated": "2024-01-15 14:30 WIB",
  "items": [
    {
      "title": "Market Growth Analysis",
      "source": "Internal Analytics", 
      "summary": "Q4 showed 15% growth in user engagement..."
    }
  ]
}
```

## 🛠️ Development

### Adding New Data Sources
1. Edit `scraper/main.py`
2. Add new source to `fetch_sources()`
3. Implement actual API calls in `fetch_with_retry()`

### Customizing Dashboard
1. Edit `fe/pages/index.tsx` for layout
2. Modify `fe/styles/globals.css` for styling
3. Add new chart types in the charts section

### API Extensions
1. Add new endpoints in `api/app.py`
2. Update Pydantic models as needed
3. Add authentication if required

## 🚨 Troubleshooting

### Common Issues
1. **CORS Errors**: Check API CORS settings
2. **Data Not Loading**: Verify persistent storage mount
3. **Scraper Failing**: Check cron job configuration
4. **Build Failures**: Ensure all dependencies installed

### Logs
- **API Logs**: Check Railway service logs
- **Scraper Logs**: View cron job execution logs
- **Frontend Logs**: Browser console

## 📈 Monitoring

### Health Checks
- API: `GET /healthz`
- Frontend: Status indicator in UI
- Scraper: Check last updated time

### Performance
- API response time: < 200ms
- Scraper execution: < 30s
- Frontend load time: < 3s

## 🔒 Security Notes

- CORS allows all origins (configure for production)
- No authentication implemented (add as needed)
- Environment variables for sensitive data
- No hardcoded secrets

## 📝 License

MIT License - Feel free to use for hackathons and demos!

---

**Built for Railway Hobby Plan ($5/month)** 🚂