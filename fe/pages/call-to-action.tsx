import { useState, useEffect, useMemo } from 'react'
import Head from 'next/head'
import Sidebar from '../components/Sidebar'

interface Insight {
  id: string
  title: string
  summary: string
  source: string
  url: string
  published_date: string
  scraped_at: string
  tags: string[]
  sentiment?: string
  social_media?: string
  product?: string
  channel?: string
}

interface PrioritizedInsight extends Insight {
  priority: 'high' | 'medium' | 'low'
  recommendedTeam: string
  actionItems: string[]
  impact: string
}

export default function CallToAction() {
  const [insights, setInsights] = useState<Insight[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedPriority, setSelectedPriority] = useState<string>('all')
  const [selectedTeam, setSelectedTeam] = useState<string>('all')

  useEffect(() => {
    fetchInsights()
  }, [])

  const fetchInsights = async () => {
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'
      
      const healthResponse = await fetch(`${apiBase}/healthz`)
      if (healthResponse.ok) {
        const insightsResponse = await fetch(`${apiBase}/insights`)
        if (insightsResponse.ok) {
          const data = await insightsResponse.json()
          setInsights(data.insights || [])
        }
      }
    } catch (error) {
      console.error('Error fetching insights:', error)
      try {
        const response = await fetch('/BerInsight/fallback.json')
        const data = await response.json()
        setInsights(data.insights || [])
      } catch (fallbackError) {
        console.error('Error loading fallback data:', fallbackError)
      }
    } finally {
      setLoading(false)
    }
  }

  // Prioritize and assign insights
  const prioritizedInsights = useMemo<PrioritizedInsight[]>(() => {
    return insights.map((insight) => {
      // Determine priority based on sentiment and keywords
      let priority: 'high' | 'medium' | 'low' = 'medium'
      const sentiment = insight.sentiment?.toLowerCase() || ''
      const content = `${insight.title} ${insight.summary}`.toLowerCase()
      
      // High priority: negative sentiment or urgent keywords
      if (sentiment === 'negative' || 
          content.includes('urgent') || 
          content.includes('critical') || 
          content.includes('issue') ||
          content.includes('problem')) {
        priority = 'high'
      }
      // Low priority: positive sentiment with no urgent keywords
      else if (sentiment === 'positive') {
        priority = 'low'
      }

      // Assign to team based on tags and content
      let recommendedTeam = 'General'
      const tags = insight.tags.map(t => t.toLowerCase())
      
      if (tags.some(t => t.includes('product') || t.includes('feature')) || 
          insight.product || 
          content.includes('product') || 
          content.includes('feature')) {
        recommendedTeam = 'Product Team'
      } else if (tags.some(t => t.includes('market') || t.includes('customer')) ||
                 content.includes('market') || 
                 content.includes('customer')) {
        recommendedTeam = 'Marketing Team'
      } else if (tags.some(t => t.includes('tech') || t.includes('development')) ||
                 content.includes('technical') || 
                 content.includes('development')) {
        recommendedTeam = 'Engineering Team'
      } else if (tags.some(t => t.includes('support') || t.includes('service')) ||
                 sentiment === 'negative') {
        recommendedTeam = 'Customer Support'
      }

      // Generate action items
      const actionItems: string[] = []
      if (priority === 'high') {
        actionItems.push('Review immediately')
        actionItems.push('Assign team lead')
      }
      if (sentiment === 'negative') {
        actionItems.push('Investigate root cause')
        actionItems.push('Prepare response plan')
      }
      if (content.includes('competitor')) {
        actionItems.push('Competitive analysis')
      }
      actionItems.push('Monitor trends')

      // Impact assessment
      let impact = 'Medium impact on business metrics'
      if (priority === 'high') {
        impact = 'High impact - requires immediate attention'
      } else if (priority === 'low') {
        impact = 'Low impact - monitor and track'
      }

      return {
        ...insight,
        priority,
        recommendedTeam,
        actionItems,
        impact
      }
    }).sort((a, b) => {
      // Sort by priority: high > medium > low
      const priorityOrder = { high: 0, medium: 1, low: 2 }
      return priorityOrder[a.priority] - priorityOrder[b.priority]
    })
  }, [insights])

  // Filter insights
  const filteredInsights = useMemo(() => {
    return prioritizedInsights.filter(insight => {
      if (selectedPriority !== 'all' && insight.priority !== selectedPriority) return false
      if (selectedTeam !== 'all' && insight.recommendedTeam !== selectedTeam) return false
      return true
    })
  }, [prioritizedInsights, selectedPriority, selectedTeam])

  // Statistics
  const stats = useMemo(() => {
    const total = prioritizedInsights.length
    const high = prioritizedInsights.filter(i => i.priority === 'high').length
    const medium = prioritizedInsights.filter(i => i.priority === 'medium').length
    const low = prioritizedInsights.filter(i => i.priority === 'low').length
    
    const teamDistribution: { [key: string]: number } = {}
    prioritizedInsights.forEach(i => {
      teamDistribution[i.recommendedTeam] = (teamDistribution[i.recommendedTeam] || 0) + 1
    })

    return { total, high, medium, low, teamDistribution }
  }, [prioritizedInsights])

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return '#ef4444'
      case 'medium': return '#f59e0b'
      case 'low': return '#10b981'
      default: return '#6b7280'
    }
  }

  const getPriorityBg = (priority: string) => {
    switch (priority) {
      case 'high': return '#fee2e2'
      case 'medium': return '#fef3c7'
      case 'low': return '#d1fae5'
      default: return '#f3f4f6'
    }
  }

  return (
    <>
      <Head>
        <title>Call to Action - BerInsight</title>
        <meta name="description" content="Prioritized insights and action items" />
      </Head>

      <div style={{ display: 'flex', minHeight: '100vh', background: '#f8f9fa' }}>
        <Sidebar activePage="call-to-action" />
        
        <div style={{ marginLeft: '260px', flex: 1, padding: '32px' }}>
          {/* Header */}
          <div style={{ marginBottom: '32px' }}>
            <h1 style={{ 
              fontSize: '32px', 
              fontWeight: '700', 
              margin: '0 0 8px 0',
              background: 'linear-gradient(135deg, #9333ea 0%, #f59e0b 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}>
              Call to Action
            </h1>
            <p style={{ fontSize: '16px', color: '#64748b', margin: 0 }}>
              Prioritized insights with recommended teams and action items
            </p>
          </div>

          {/* Stats Cards */}
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
            gap: '20px', 
            marginBottom: '32px' 
          }}>
            <div style={{ 
              background: 'white', 
              padding: '24px', 
              borderRadius: '16px', 
              boxShadow: '0 4px 12px rgba(0,0,0,0.08)' 
            }}>
              <div style={{ fontSize: '14px', color: '#64748b', marginBottom: '8px' }}>Total Insights</div>
              <div style={{ fontSize: '32px', fontWeight: '700', color: '#1e293b' }}>{stats.total}</div>
            </div>

            <div style={{ 
              background: 'white', 
              padding: '24px', 
              borderRadius: '16px', 
              boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
              border: '2px solid #fee2e2'
            }}>
              <div style={{ fontSize: '14px', color: '#ef4444', marginBottom: '8px' }}>High Priority</div>
              <div style={{ fontSize: '32px', fontWeight: '700', color: '#ef4444' }}>{stats.high}</div>
            </div>

            <div style={{ 
              background: 'white', 
              padding: '24px', 
              borderRadius: '16px', 
              boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
              border: '2px solid #fef3c7'
            }}>
              <div style={{ fontSize: '14px', color: '#f59e0b', marginBottom: '8px' }}>Medium Priority</div>
              <div style={{ fontSize: '32px', fontWeight: '700', color: '#f59e0b' }}>{stats.medium}</div>
            </div>

            <div style={{ 
              background: 'white', 
              padding: '24px', 
              borderRadius: '16px', 
              boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
              border: '2px solid #d1fae5'
            }}>
              <div style={{ fontSize: '14px', color: '#10b981', marginBottom: '8px' }}>Low Priority</div>
              <div style={{ fontSize: '32px', fontWeight: '700', color: '#10b981' }}>{stats.low}</div>
            </div>
          </div>

          {/* Filters */}
          <div style={{ 
            background: 'white', 
            padding: '20px', 
            borderRadius: '16px', 
            boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
            marginBottom: '24px',
            display: 'flex',
            gap: '16px',
            flexWrap: 'wrap'
          }}>
            <div>
              <label style={{ fontSize: '14px', fontWeight: '600', color: '#475569', marginBottom: '8px', display: 'block' }}>
                Priority Level
              </label>
              <select 
                value={selectedPriority}
                onChange={(e) => setSelectedPriority(e.target.value)}
                style={{
                  padding: '10px 16px',
                  borderRadius: '8px',
                  border: '1px solid #e2e8f0',
                  fontSize: '14px',
                  cursor: 'pointer',
                  background: 'white'
                }}
              >
                <option value="all">All Priorities</option>
                <option value="high">High Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="low">Low Priority</option>
              </select>
            </div>

            <div>
              <label style={{ fontSize: '14px', fontWeight: '600', color: '#475569', marginBottom: '8px', display: 'block' }}>
                Assigned Team
              </label>
              <select 
                value={selectedTeam}
                onChange={(e) => setSelectedTeam(e.target.value)}
                style={{
                  padding: '10px 16px',
                  borderRadius: '8px',
                  border: '1px solid #e2e8f0',
                  fontSize: '14px',
                  cursor: 'pointer',
                  background: 'white'
                }}
              >
                <option value="all">All Teams</option>
                {Object.keys(stats.teamDistribution).map(team => (
                  <option key={team} value={team}>{team} ({stats.teamDistribution[team]})</option>
                ))}
              </select>
            </div>
          </div>

          {/* Insights List */}
          {loading ? (
            <div style={{ textAlign: 'center', padding: '60px', color: '#64748b' }}>
              Loading insights...
            </div>
          ) : filteredInsights.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '60px', color: '#64748b' }}>
              No insights match the selected filters.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {filteredInsights.map((insight) => (
                <div 
                  key={insight.id}
                  style={{
                    background: 'white',
                    borderRadius: '16px',
                    padding: '24px',
                    boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
                    borderLeft: `4px solid ${getPriorityColor(insight.priority)}`
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
                    <div style={{ flex: 1 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                        <span style={{
                          padding: '4px 12px',
                          borderRadius: '12px',
                          fontSize: '12px',
                          fontWeight: '600',
                          color: getPriorityColor(insight.priority),
                          background: getPriorityBg(insight.priority),
                          textTransform: 'uppercase'
                        }}>
                          {insight.priority} Priority
                        </span>
                        <span style={{
                          padding: '4px 12px',
                          borderRadius: '12px',
                          fontSize: '12px',
                          fontWeight: '600',
                          color: '#9333ea',
                          background: '#f3e8ff'
                        }}>
                          {insight.recommendedTeam}
                        </span>
                      </div>
                      <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#1e293b', margin: '0 0 8px 0' }}>
                        {insight.title}
                      </h3>
                      <p style={{ fontSize: '14px', color: '#64748b', margin: '0 0 16px 0', lineHeight: '1.6' }}>
                        {insight.summary}
                      </p>
                    </div>
                  </div>

                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
                    gap: '16px',
                    padding: '16px',
                    background: '#f8fafc',
                    borderRadius: '12px',
                    marginBottom: '16px'
                  }}>
                    <div>
                      <div style={{ fontSize: '12px', fontWeight: '600', color: '#475569', marginBottom: '8px' }}>
                        📋 Action Items
                      </div>
                      <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '14px', color: '#64748b' }}>
                        {insight.actionItems.map((item, idx) => (
                          <li key={idx}>{item}</li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <div style={{ fontSize: '12px', fontWeight: '600', color: '#475569', marginBottom: '8px' }}>
                        📊 Impact Assessment
                      </div>
                      <p style={{ margin: 0, fontSize: '14px', color: '#64748b' }}>
                        {insight.impact}
                      </p>
                    </div>
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '12px', color: '#94a3b8' }}>
                    <div>
                      <strong>Source:</strong> {insight.source} | <strong>Date:</strong> {new Date(insight.published_date).toLocaleDateString()}
                    </div>
                    <a 
                      href={insight.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      style={{
                        color: '#9333ea',
                        textDecoration: 'none',
                        fontWeight: '600',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}
                    >
                      View Source →
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  )
}

