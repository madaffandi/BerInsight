import { useState, useEffect, useMemo, Component } from 'react'
import Head from 'next/head'
import dynamic from 'next/dynamic'
import { registerChartJS } from '../utils/chartSetup'

// Dynamically import charts with no SSR
const Line = dynamic(() => import('react-chartjs-2').then(mod => mod.Line), { ssr: false })
const Bar = dynamic(() => import('react-chartjs-2').then(mod => mod.Bar), { ssr: false })
const Doughnut = dynamic(() => import('react-chartjs-2').then(mod => mod.Doughnut), { ssr: false })

// Simple CSS-based Tag Cloud component (no external dependencies)
const SimpleTagCloud = ({ words }: { words: Array<{ text: string; value: number }> }) => {
  if (!words || words.length === 0) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: '#888' }}>
        No keywords available. Try adjusting filters.
      </div>
    )
  }

  // Find max and min values for scaling
  const maxValue = Math.max(...words.map(w => w.value))
  const minValue = Math.min(...words.map(w => w.value))
  
  // Color palette
  const colors = ['#9333ea', '#c084fc', '#f59e0b', '#fbbf24', '#10b981', '#34d399', '#06b6d4', '#ec4899']
  
  // Limit to top 30 words for better display
  const displayWords = words.slice(0, 30)
  
  return (
    <div style={{
      display: 'flex',
      flexWrap: 'wrap',
      gap: '8px',
      padding: '15px',
      justifyContent: 'center',
      alignItems: 'center',
      maxHeight: '350px',
      overflow: 'auto'
    }}>
      {displayWords.map((word, index) => {
        // Calculate font size based on value (14-32px for more compact display)
        const scale = (word.value - minValue) / (maxValue - minValue || 1)
        const fontSize = 14 + (scale * 18)
        const color = colors[index % colors.length]
        
        return (
          <span
            key={`${word.text}-${index}`}
            style={{
              fontSize: `${fontSize}px`,
              color: color,
              fontWeight: '600',
              padding: '3px 8px',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              borderRadius: '4px',
              display: 'inline-block',
              lineHeight: '1.4'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'scale(1.05)'
              e.currentTarget.style.backgroundColor = `${color}20`
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'scale(1)'
              e.currentTarget.style.backgroundColor = 'transparent'
            }}
            title={`${word.text}: ${word.value} mentions`}
          >
            {word.text}
          </span>
        )
      })}
    </div>
  )
}

// Error boundary for WordCloud
class WordCloudErrorBoundary extends Component<{ children: React.ReactNode }, { hasError: boolean }> {
  constructor(props: { children: React.ReactNode }) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error('WordCloud error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '40px', textAlign: 'center', color: '#ef4444' }}>
          Unable to display word cloud. Please refresh the page.
        </div>
      )
    }

    return this.props.children
  }
}

interface HealthStatus {
  status: string
  time: string
}

interface Insight {
  title: string
  source: string
  summary: string
  type?: string
  product?: string
  feature?: string
  channel?: string
  social_media?: string
  sentiment?: string
  urgency_score?: number
  date?: string
  category?: string
}

interface InsightsData {
  last_updated: string
  items: Insight[]
}

export default function Home() {
  const [mounted, setMounted] = useState(false)
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null)
  const [insights, setInsights] = useState<InsightsData | null>(null)
  const [isOffline, setIsOffline] = useState(false)
  const [loading, setLoading] = useState(true)
  
  // Filter states
  const [startDate, setStartDate] = useState<string>('')
  const [endDate, setEndDate] = useState<string>('')
  const [selectedProduct, setSelectedProduct] = useState<string>('all')
  const [selectedChannel, setSelectedChannel] = useState<string>('all')
  const [selectedSocialMedia, setSelectedSocialMedia] = useState<string>('all')
  const [selectedSentiment, setSelectedSentiment] = useState<string>('all')
  
  // Register Chart.js and prevent hydration mismatch
  useEffect(() => {
    registerChartJS()
    setMounted(true)
  }, [])

  // Filtered data based on user selections
  const filteredInsights = useMemo(() => {
    if (!insights || !insights.items) return []
    
    return insights.items.filter(item => {
      // Date filter
      if (startDate && item.date && item.date < startDate) return false
      if (endDate && item.date && item.date > endDate) return false
      
      // Product filter
      if (selectedProduct !== 'all' && item.product !== selectedProduct) return false
      
      // Channel filter
      if (selectedChannel !== 'all' && item.channel !== selectedChannel) return false
      
      // Social Media filter
      if (selectedSocialMedia !== 'all' && item.social_media !== selectedSocialMedia) return false
      
      // Sentiment filter
      if (selectedSentiment !== 'all' && item.sentiment !== selectedSentiment) return false
      
      return true
    })
  }, [insights, startDate, endDate, selectedProduct, selectedChannel, selectedSocialMedia, selectedSentiment])

  // Aggregate data for charts
  const socialMediaCounts = useMemo(() => {
    const counts: Record<string, number> = {
      'YouTube': 0,
      'Instagram': 0,
      'Twitter': 0,
      'Facebook': 0,
      'Apple AppStore': 0,
      'Google Playstore': 0
    }
    filteredInsights.forEach(item => {
      if (item.social_media && counts.hasOwnProperty(item.social_media)) {
        counts[item.social_media]++
      }
    })
    return counts
  }, [filteredInsights])

  const productCounts = useMemo(() => {
    const counts: Record<string, number> = {}
    filteredInsights.forEach(item => {
      if (item.product) {
        counts[item.product] = (counts[item.product] || 0) + 1
      }
    })
    return counts
  }, [filteredInsights])

  const channelCounts = useMemo(() => {
    const counts: Record<string, number> = {}
    filteredInsights.forEach(item => {
      if (item.channel) {
        counts[item.channel] = (counts[item.channel] || 0) + 1
      }
    })
    return counts
  }, [filteredInsights])

  const sentimentCounts = useMemo(() => {
    const counts = { positive: 0, neutral: 0, negative: 0 }
    filteredInsights.forEach(item => {
      const sentiment = item.sentiment?.toLowerCase()
      if (sentiment === 'positive') counts.positive++
      else if (sentiment === 'negative') counts.negative++
      else counts.neutral++
    })
    return counts
  }, [filteredInsights])

  // Customer Knowledge Analytics Data
  const socialMediaData = useMemo(() => ({
    labels: ['YouTube', 'Instagram', 'Twitter', 'Facebook', 'AppStore', 'Playstore'],
    datasets: [{
      label: 'Comments/Complaints',
      data: [
        socialMediaCounts['YouTube'],
        socialMediaCounts['Instagram'],
        socialMediaCounts['Twitter'],
        socialMediaCounts['Facebook'],
        socialMediaCounts['Apple AppStore'],
        socialMediaCounts['Google Playstore']
      ],
      backgroundColor: [
        'rgba(255, 0, 0, 0.8)',
        'rgba(225, 48, 108, 0.8)',
        'rgba(29, 161, 242, 0.8)',
        'rgba(24, 119, 242, 0.8)',
        'rgba(0, 0, 0, 0.8)',
        'rgba(52, 168, 83, 0.8)',
      ],
    }]
  }), [socialMediaCounts])

  const productData = useMemo(() => {
    const products = ['BRImo', 'Card', 'Qlola', 'Loan', 'Simpedes', 'Britama', 'Deposito']
    const colors = ['#0047BA', '#FF6B35', '#F7B801', '#00B4D8', '#7209B7', '#4CC9F0', '#06FFA5']
    return {
      labels: products,
      datasets: [{
        data: products.map(p => productCounts[p] || 0),
        backgroundColor: colors,
      }]
    }
  }, [productCounts])

  const channelData = useMemo(() => {
    const channels = ['BRImo', 'BRILink', 'CERIA', 'Qlola', 'MMS', 'Sabrina']
    const colors = [
      'rgba(0, 71, 186, 0.8)',
      'rgba(255, 107, 53, 0.8)',
      'rgba(247, 184, 1, 0.8)',
      'rgba(0, 180, 216, 0.8)',
      'rgba(114, 9, 183, 0.8)',
      'rgba(76, 201, 240, 0.8)',
    ]
    const borderColors = colors.map(c => c.replace('0.8', '1'))
    
    return {
      labels: channels,
      datasets: [{
        label: 'Interactions',
        data: channels.map(c => channelCounts[c] || 0),
        backgroundColor: colors,
        borderColor: borderColors,
        borderWidth: 2,
      }]
    }
  }, [channelCounts])

  const sentimentData = useMemo(() => ({
    labels: ['Positive', 'Neutral', 'Negative'],
    datasets: [{
      data: [sentimentCounts.positive, sentimentCounts.neutral, sentimentCounts.negative],
      backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
    }]
  }), [sentimentCounts])

  // Extract keywords from filtered insights for wordcloud
  const keywordsData = useMemo(() => {
    console.log('Calculating keywordsData from filteredInsights:', filteredInsights?.length || 0)
    
    if (!filteredInsights || filteredInsights.length === 0) {
      console.log('No filtered insights available')
      return []
    }
    
    const words: Record<string, number> = {}
    const commonWords = new Set(['di', 'dan', 'yang', 'untuk', 'dengan', 'tidak', 'pada', 'dari', 'ke', 'ini', 'itu', 'adalah', 'atau', 'saat', 'sejak', 'tapi', 'fitur', 'customer', 'service', 'bri', 'bank'])
    
    filteredInsights.forEach(item => {
      if (!item.title && !item.summary) return
      const text = `${item.title || ''} ${item.summary || ''}`.toLowerCase()
      const words_array = text.split(/\s+/)
      
      words_array.forEach(word => {
        const cleaned = word.replace(/[^a-z0-9]/g, '')
        if (cleaned.length > 3 && !commonWords.has(cleaned)) {
          words[cleaned] = (words[cleaned] || 0) + 1
        }
      })
    })
    
    const result = Object.entries(words)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 50)
      .map(([word, count]) => ({ 
        text: word, 
        value: count 
      }))
    
    console.log('Keywords data generated:', result.length, 'keywords')
    if (result.length > 0) {
      console.log('Sample keywords:', result.slice(0, 5))
    }
    
    return result
  }, [filteredInsights])

  // Calculate metrics from filtered data
  const totalFeedback = filteredInsights.length
  const totalSentiment = sentimentCounts.positive + sentimentCounts.neutral + sentimentCounts.negative
  const sentimentScore = totalSentiment > 0 
    ? ((sentimentCounts.positive * 5 + sentimentCounts.neutral * 3 + sentimentCounts.negative * 1) / totalSentiment).toFixed(1)
    : '0.0'
  const positivePercentage = totalSentiment > 0
    ? Math.round((sentimentCounts.positive / totalSentiment) * 100)
    : 0

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

  // Prevent flickering during hydration
  if (!mounted) {
    return null
  }

  return (
    <>
      <Head>
        <title>BerInsight - Customer Knowledge Analytics</title>
        <meta name="description" content="AI-Powered Customer Knowledge Analytics & Social Media Insights" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <div className="dashboard">
        <header className="dashboard-header">
          <h1>BerInsight Customer Knowledge Analytics</h1>
          <p>AI-Powered Customer Insights & Social Media Analytics</p>
          
          {/* Filter Panel */}
          <div className="filter-panel">
            <div className="filter-row">
              <div className="filter-item">
                <label>📅 Start Date:</label>
                <input 
                  type="date" 
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="filter-input"
                />
              </div>
              
              <div className="filter-item">
                <label>📅 End Date:</label>
                <input 
                  type="date" 
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  className="filter-input"
                />
              </div>
              
              <div className="filter-item">
                <label>📱 Product:</label>
                <select 
                  value={selectedProduct}
                  onChange={(e) => setSelectedProduct(e.target.value)}
                  className="filter-select"
                >
                  <option value="all">All Products</option>
                  <option value="BRImo">BRImo</option>
                  <option value="Card">Card</option>
                  <option value="Qlola">Qlola</option>
                  <option value="Loan">Loan</option>
                  <option value="Simpedes">Simpedes</option>
                  <option value="Britama">Britama</option>
                  <option value="Deposito">Deposito</option>
                </select>
              </div>
              
              <div className="filter-item">
                <label>🏪 Channel:</label>
                <select 
                  value={selectedChannel}
                  onChange={(e) => setSelectedChannel(e.target.value)}
                  className="filter-select"
                >
                  <option value="all">All Channels</option>
                  <option value="BRImo">BRImo</option>
                  <option value="BRILink">BRILink</option>
                  <option value="CERIA">CERIA</option>
                  <option value="Qlola">Qlola</option>
                  <option value="MMS">MMS</option>
                  <option value="Sabrina">Sabrina</option>
                </select>
              </div>
              
              <div className="filter-item">
                <label>📺 Social Media:</label>
                <select 
                  value={selectedSocialMedia}
                  onChange={(e) => setSelectedSocialMedia(e.target.value)}
                  className="filter-select"
                >
                  <option value="all">All Platforms</option>
                  <option value="YouTube">YouTube</option>
                  <option value="Instagram">Instagram</option>
                  <option value="Twitter">Twitter</option>
                  <option value="Facebook">Facebook</option>
                  <option value="Apple AppStore">Apple AppStore</option>
                  <option value="Google Playstore">Google Playstore</option>
                </select>
              </div>
              
              <div className="filter-item">
                <label>😊 Sentiment:</label>
                <select 
                  value={selectedSentiment}
                  onChange={(e) => setSelectedSentiment(e.target.value)}
                  className="filter-select"
                >
                  <option value="all">All Sentiments</option>
                  <option value="positive">Positive</option>
                  <option value="neutral">Neutral</option>
                  <option value="negative">Negative</option>
                </select>
              </div>
              
              <div className="filter-item">
                <button 
                  onClick={() => {
                    setStartDate('')
                    setEndDate('')
                    setSelectedProduct('all')
                    setSelectedChannel('all')
                    setSelectedSocialMedia('all')
                    setSelectedSentiment('all')
                  }}
                  className="filter-reset-btn"
                >
                  🔄 Reset Filters
                </button>
              </div>
            </div>
            
            <div className="filter-stats">
              <strong>Showing:</strong> {totalFeedback} items
              {(startDate || endDate || selectedProduct !== 'all' || selectedChannel !== 'all' || 
                selectedSocialMedia !== 'all' || selectedSentiment !== 'all') && 
                <span className="filtered-badge">Filtered</span>
              }
            </div>
          </div>
          
        </header>

        <div className="dashboard-grid">
          {/* Key Metrics Cards */}
          <div className="metrics-row">
            <div className="metric-card">
              <h3>Total Feedback</h3>
              <div className="metric-value">{totalFeedback.toLocaleString()}</div>
              <div className="metric-change positive">Real-time</div>
            </div>
            <div className="metric-card">
              <h3>Customer Satisfaction</h3>
              <div className="metric-value">{sentimentScore}/5.0</div>
              <div className="metric-change positive">{positivePercentage}% positive</div>
            </div>
            <div className="metric-card">
              <h3>Sentiment Score</h3>
              <div className="metric-value">{positivePercentage}%</div>
              <div className="metric-change positive">Positive rate</div>
            </div>
            <div className="metric-card">
              <h3>Data Points</h3>
              <div className="metric-value">{Object.keys(productCounts).length}</div>
              <div className="metric-change neutral">Products</div>
            </div>
          </div>

          {/* Main Analytics Grid: Left (Social Media), Center (Products), Right (Channels) */}
          <div className="analytics-grid">
            {/* Left: Social Media Platforms */}
            <div className="chart-container">
              <h3>Social Media Feedback</h3>
              <Bar data={socialMediaData} options={{
                ...chartOptions,
                plugins: {
                  ...chartOptions.plugins,
                  title: { display: true, text: 'Comments by Social Media Platform' },
                  legend: { display: false }
                }
              }} />
            </div>

            {/* Center: Product Categorization */}
            <div className="chart-container">
              <h3>Product Analysis</h3>
              <Doughnut data={productData} options={{
                ...chartOptions,
                plugins: {
                  ...chartOptions.plugins,
                  title: { display: true, text: 'Feedback by Product' }
                }
              }} />
            </div>

            {/* Right: Channel Distribution */}
            <div className="chart-container">
              <h3>Channel Distribution</h3>
              <Bar data={channelData} options={{
                ...chartOptions,
                plugins: {
                  ...chartOptions.plugins,
                  title: { display: true, text: 'Interactions by Channel' },
                  legend: { display: false }
                }
              }} />
            </div>
          </div>

          {/* Sentiment & Keywords Section - Merged into 2 columns */}
          <div className="sentiment-keywords-section">
            {/* Left: Sentiment Analysis */}
            <div className="sentiment-card">
              <h3>Sentiment Analysis</h3>
              <div className="sentiment-grid">
                <div className="sentiment-chart">
                  <Doughnut data={sentimentData} options={{
                    ...chartOptions,
                    plugins: {
                      ...chartOptions.plugins,
                      title: { display: false }
                    }
                  }} />
                </div>
                <div className="sentiment-stats">
                  <div className="sentiment-item positive">
                    <div className="sentiment-label">Positive</div>
                    <div className="sentiment-value">
                      {sentimentCounts.positive} ({totalSentiment > 0 ? Math.round((sentimentCounts.positive / totalSentiment) * 100) : 0}%)
                    </div>
                  </div>
                  <div className="sentiment-item neutral">
                    <div className="sentiment-label">Neutral</div>
                    <div className="sentiment-value">
                      {sentimentCounts.neutral} ({totalSentiment > 0 ? Math.round((sentimentCounts.neutral / totalSentiment) * 100) : 0}%)
                    </div>
                  </div>
                  <div className="sentiment-item negative">
                    <div className="sentiment-label">Negative</div>
                    <div className="sentiment-value">
                      {sentimentCounts.negative} ({totalSentiment > 0 ? Math.round((sentimentCounts.negative / totalSentiment) * 100) : 0}%)
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Right: Keywords Tag Cloud */}
            <div className="keywords-card">
              <h3>Most Mentioned Keywords</h3>
              <div className="wordcloud-container">
                <WordCloudErrorBoundary>
                  {!mounted ? (
                    <div style={{ padding: '40px', textAlign: 'center', color: '#888' }}>
                      Initializing...
                    </div>
                  ) : (
                    <SimpleTagCloud words={keywordsData} />
                  )}
                </WordCloudErrorBoundary>
              </div>
            </div>
          </div>

          {/* Highlighted Ideas Section */}
          <div className="ideas-section">
            <h3>Highlighted Ideas & Suggestions</h3>
            <div className="ideas-grid">
              <div className="idea-card priority-high">
                <div className="idea-header">
                  <span className="idea-badge">High Priority</span>
                  <span className="idea-product">BRImo</span>
                </div>
                <h4>Dark Mode Implementation</h4>
                <p>Multiple users requesting dark mode feature for better night-time usage. High engagement potential.</p>
                <div className="idea-meta">
                  <span>📱 45 mentions</span>
                  <span>⭐ 89% positive</span>
                </div>
              </div>
              <div className="idea-card priority-medium">
                <div className="idea-header">
                  <span className="idea-badge medium">Medium Priority</span>
                  <span className="idea-product">Card</span>
                </div>
                <h4>Biometric Authentication</h4>
                <p>Customers want fingerprint/face recognition for card transactions to enhance security.</p>
                <div className="idea-meta">
                  <span>🔐 32 mentions</span>
                  <span>⭐ 92% positive</span>
                </div>
              </div>
              <div className="idea-card priority-high">
                <div className="idea-header">
                  <span className="idea-badge">High Priority</span>
                  <span className="idea-product">Qlola</span>
                </div>
                <h4>Merchant Cashback Program</h4>
                <p>Request for enhanced cashback rewards at partner merchants to increase usage.</p>
                <div className="idea-meta">
                  <span>💰 38 mentions</span>
                  <span>⭐ 95% positive</span>
                </div>
              </div>
            </div>
          </div>

          {/* Insights Section */}
          {filteredInsights.length > 0 && (
            <div className="insights-section">
              <h2>Latest Customer Insights ({filteredInsights.length} items)</h2>
              <div className="insights-grid">
                {filteredInsights.slice(0, 6).map((insight, index) => (
                  <div key={index} className="insight-card">
                    <div className="insight-header">
                      <span className="insight-type">{insight.type}</span>
                      <span className={`insight-sentiment ${insight.sentiment || 'neutral'}`}>
                        {insight.sentiment || 'neutral'}
                      </span>
                    </div>
                    <h4>{insight.title}</h4>
                    <p className="insight-source">📍 {insight.source}</p>
                    <p className="insight-summary">{insight.summary}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  )
}
