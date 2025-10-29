import { useRouter } from 'next/router'
import Image from 'next/image'

interface SidebarProps {
  activePage: 'dashboard' | 'call-to-action'
}

export default function Sidebar({ activePage }: SidebarProps) {
  const router = useRouter()

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊', path: '/' },
    { id: 'call-to-action', label: 'Call to Action', icon: '🎯', path: '/call-to-action' }
  ]

  return (
    <div style={{
      width: '260px',
      height: '100vh',
      background: 'linear-gradient(180deg, #1a1a2e 0%, #16213e 100%)',
      position: 'fixed',
      left: 0,
      top: 0,
      display: 'flex',
      flexDirection: 'column',
      padding: '24px 16px',
      boxShadow: '4px 0 12px rgba(0,0,0,0.1)',
      zIndex: 1000
    }}>
      {/* Logo */}
      <div style={{
        marginBottom: '40px',
        padding: '12px',
        textAlign: 'center'
      }}>
        <img 
          src="/BerInsight/assets/berinsight-logo.svg" 
          alt="BerInsight" 
          style={{ width: '180px', height: 'auto' }}
        />
      </div>

      {/* Menu Items */}
      <nav style={{ flex: 1 }}>
        {menuItems.map((item) => {
          const isActive = activePage === item.id
          return (
            <button
              key={item.id}
              onClick={() => router.push(item.path)}
              style={{
                width: '100%',
                padding: '14px 20px',
                marginBottom: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                background: isActive 
                  ? 'linear-gradient(135deg, #9333ea 0%, #c084fc 100%)' 
                  : 'transparent',
                color: isActive ? '#ffffff' : '#a0aec0',
                border: 'none',
                borderRadius: '12px',
                fontSize: '16px',
                fontWeight: isActive ? '600' : '500',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                textAlign: 'left',
                boxShadow: isActive ? '0 4px 12px rgba(147, 51, 234, 0.3)' : 'none'
              }}
              onMouseEnter={(e) => {
                if (!isActive) {
                  e.currentTarget.style.background = 'rgba(147, 51, 234, 0.1)'
                  e.currentTarget.style.color = '#ffffff'
                }
              }}
              onMouseLeave={(e) => {
                if (!isActive) {
                  e.currentTarget.style.background = 'transparent'
                  e.currentTarget.style.color = '#a0aec0'
                }
              }}
            >
              <span style={{ fontSize: '20px' }}>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          )
        })}
      </nav>

      {/* Footer */}
      <div style={{
        padding: '16px',
        borderTop: '1px solid rgba(255,255,255,0.1)',
        color: '#718096',
        fontSize: '12px',
        textAlign: 'center'
      }}>
        <p style={{ margin: 0 }}>© 2025 BerInsight</p>
        <p style={{ margin: '4px 0 0 0' }}>Smart Media Insights</p>
      </div>
    </div>
  )
}

