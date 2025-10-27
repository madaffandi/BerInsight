import { useState, useEffect } from 'react'
import Head from 'next/head'
import { Line, Bar, Doughnut } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

interface HealthStatus {
  status: string
  time: string
}

interface Insight {
  title: string
  source: string
  summary: string
}

interface InsightsData {
  last_updated: string
  items: Insight[]
}

export default function Home() {
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null)
  const [insights, setInsights] = useState<InsightsData | null>(null)
  const [isOffline, setIsOffline] = useState(false)
  const [loading, setLoading] = useState(true)

  // Banking Intelligence Data
  const riskTrendData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
      {
        label: 'Credit Risk Score',
        data: [7.8, 7.5, 7.2, 6.9, 7.1, 6.8, 7.0, 6.7, 6.9, 6.5, 6.8, 7.2],
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.4,
      },
      {
        label: 'Market Risk Score',
        data: [6.5, 6.8, 7.1, 7.4, 7.0, 7.3, 7.1, 7.5, 7.2, 7.6, 7.4, 7.0],
        borderColor: 'rgb(54, 162, 235)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        tension: 0.4,
      }
    ]
  }

  const socialMentionsData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: 'Social Media Mentions',
        data: [1200, 1900, 3000, 5000, 2000, 300, 800],
        backgroundColor: [
          'rgba(255, 99, 132, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 205, 86, 0.8)',
          'rgba(75, 192, 192, 0.8)',
          'rgba(153, 102, 255, 0.8)',
          'rgba(255, 159, 64, 0.8)',
          'rgba(199, 199, 199, 0.8)',
        ],
      }
    ]
  }

  const riskCategoryData = {
    labels: ['Credit Risk', 'Market Risk', 'Operational Risk', 'Liquidity Risk', 'Compliance Risk', 'Cyber Risk'],
    datasets: [
      {
        data: [35, 25, 15, 12, 8, 5],
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#FF9F40',
        ],
      }
    ]
  }

  const fraudDetectionData = {
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    datasets: [
      {
        label: 'Fraud Detection Rate (%)',
        data: [94.5, 96.2, 95.8, 97.1],
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
      }
    ]
  }

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Chart Title',
      },
    },
  }

  const fetchWithTimeout = async (url: string, timeout = 3000) => {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), timeout)
    
    try {
      const response = await fetch(url, { signal: controller.signal })
      clearTimeout(timeoutId)
      return response
    } catch (error) {
      clearTimeout(timeoutId)
      throw error
    }
  }

  const fetchHealthStatus = async () => {
    try {
      const response = await fetchWithTimeout(`${process.env.NEXT_PUBLIC_API_BASE}/healthz`)
      if (response.ok) {
        const data = await response.json()
        setHealthStatus(data)
      }
    } catch (error) {
      console.error('Failed to fetch health status:', error)
    }
  }

  const fetchInsights = async () => {
    try {
      const response = await fetchWithTimeout(`${process.env.NEXT_PUBLIC_API_BASE}/insights`)
      if (response.ok) {
        const data = await response.json()
        setInsights(data)
        setIsOffline(false)
      }
    } catch (error) {
      console.error('Failed to fetch insights, trying fallback:', error)
      try {
        const fallbackResponse = await fetch('/fallback.json')
        if (fallbackResponse.ok) {
          const fallbackData = await fallbackResponse.json()
          setInsights(fallbackData)
          setIsOffline(true)
        }
      } catch (fallbackError) {
        console.error('Fallback also failed:', fallbackError)
      }
    }
  }

  useEffect(() => {
    const loadData = async () => {
      setLoading(true)
      await Promise.all([fetchHealthStatus(), fetchInsights()])
      setLoading(false)
    }
    loadData()
  }, [])

  const formatTime = (timeString: string) => {
    try {
      const date = new Date(timeString)
      return date.toLocaleString('id-ID', { 
        timeZone: 'Asia/Jakarta',
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }) + ' WIB'
    } catch {
      return timeString
    }
  }

  return (
    <>
      <Head>
        <title>BRInsight - Banking Intelligence Dashboard</title>
        <meta name="description" content="AI-Powered Banking Intelligence & Social Media Analytics" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <div className="dashboard">
        <header className="dashboard-header">
          <h1>BRInsight Banking Intelligence</h1>
          <p>AI-Powered Social Media Analytics & Risk Intelligence</p>
          <div className="status-bar">
            <div className="status-item">
              <strong>API Status:</strong> 
              <span className={healthStatus ? 'status-ok' : 'status-error'}>
                {healthStatus ? healthStatus.status : 'Checking...'}
              </span>
            </div>
            <div className="status-item">
              <strong>Last Updated:</strong> 
              <span className={insights ? 'status-ok' : 'status-error'}>
                {insights ? formatTime(insights.last_updated) : 'Loading...'}
              </span>
              {isOffline && <span className="offline-badge">(offline fallback)</span>}
            </div>
          </div>
        </header>

        <div className="dashboard-grid">
          {/* Key Metrics Cards */}
          <div className="metrics-row">
            <div className="metric-card">
              <h3>Risk Score</h3>
              <div className="metric-value">7.2/10</div>
              <div className="metric-change positive">-0.3</div>
            </div>
            <div className="metric-card">
              <h3>Social Mentions</h3>
              <div className="metric-value">15,420</div>
              <div className="metric-change positive">+8.2%</div>
            </div>
            <div className="metric-card">
              <h3>Fraud Alerts</h3>
              <div className="metric-value">23</div>
              <div className="metric-change negative">+12%</div>
            </div>
            <div className="metric-card">
              <h3>Customer Sentiment</h3>
              <div className="metric-value">4.7/5.0</div>
              <div className="metric-change positive">+0.4</div>
            </div>
          </div>

          {/* Charts Row 1 */}
          <div className="charts-row">
            <div className="chart-container">
              <h3>Risk Assessment Trends</h3>
              <Line data={riskTrendData} options={{
                ...chartOptions,
                plugins: {
                  ...chartOptions.plugins,
                  title: { display: true, text: 'Monthly Risk Score Trends' }
                }
              }} />
            </div>
            <div className="chart-container">
              <h3>Social Media Mentions</h3>
              <Bar data={socialMentionsData} options={{
                ...chartOptions,
                plugins: {
                  ...chartOptions.plugins,
                  title: { display: true, text: 'Daily Social Media Activity' }
                }
              }} />
            </div>
          </div>

          {/* Charts Row 2 */}
          <div className="charts-row">
            <div className="chart-container">
              <h3>Risk Categories Distribution</h3>
              <Doughnut data={riskCategoryData} options={{
                ...chartOptions,
                plugins: {
                  ...chartOptions.plugins,
                  title: { display: true, text: 'Risk Distribution by Category' }
                }
              }} />
            </div>
            <div className="chart-container">
              <h3>Fraud Detection Performance</h3>
              <Bar data={fraudDetectionData} options={{
                ...chartOptions,
                plugins: {
                  ...chartOptions.plugins,
                  title: { display: true, text: 'Fraud Detection Rate by Quarter' }
                }
              }} />
            </div>
          </div>

          {/* Insights Section */}
          {insights && insights.items.length > 0 && (
            <div className="insights-section">
              <h2>Latest Insights</h2>
              <div className="insights-grid">
                {insights.items.map((insight, index) => (
                  <div key={index} className="insight-card">
                    <h4>{insight.title}</h4>
                    <p className="insight-source">Source: {insight.source}</p>
                    <p className="insight-summary">{insight.summary}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Additional Metrics */}
          <div className="additional-metrics">
            <div className="metric-card">
              <h3>Compliance Score</h3>
              <div className="metric-value">98.5%</div>
            </div>
            <div className="metric-card">
              <h3>AI Accuracy</h3>
              <div className="metric-value">94.2%</div>
            </div>
            <div className="metric-card">
              <h3>False Positive Rate</h3>
              <div className="metric-value">2.1%</div>
            </div>
            <div className="metric-card">
              <h3>Processing Time</h3>
              <div className="metric-value">1.2s</div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
