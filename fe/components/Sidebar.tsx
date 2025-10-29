import { useRouter } from 'next/router'
import { useState } from 'react'

interface SidebarProps {
  activePage: 'dashboard' | 'call-to-action'
}

export default function Sidebar({ activePage }: SidebarProps) {
  const router = useRouter()
  const [isCollapsed, setIsCollapsed] = useState(false)

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊', path: '/' },
    { id: 'call-to-action', label: 'Call to Action', icon: '🎯', path: '/call-to-action' }
  ]

  return (
    <>
    <div style={{
      width: isCollapsed ? '80px' : '260px',
      height: '100vh',
      background: 'linear-gradient(180deg, #1a1a2e 0%, #16213e 100%)',
      position: 'fixed',
      left: 0,
      top: 0,
      display: 'flex',
      flexDirection: 'column',
      padding: isCollapsed ? '24px 8px' : '24px 16px',
      boxShadow: '4px 0 12px rgba(0,0,0,0.1)',
      zIndex: 1000,
      transition: 'all 0.3s ease'
    }}>
      {/* Toggle Button */}
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        style={{
          position: 'absolute',
          right: '-16px',
          top: '20px',
          width: '32px',
          height: '32px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #9333ea 0%, #c084fc 100%)',
          border: 'none',
          color: 'white',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '16px',
          boxShadow: '0 4px 8px rgba(147, 51, 234, 0.3)',
          zIndex: 1001,
          transition: 'transform 0.3s ease'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.1)'
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1)'
        }}
        title={isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
      >
        {isCollapsed ? '→' : '←'}
      </button>

      {/* Logo */}
      <div style={{
        marginBottom: '40px',
        padding: '12px',
        textAlign: 'center',
        overflow: 'hidden'
      }}>
        {!isCollapsed ? (
          <img 
            src="https://i.postimg.cc/NMjWTcGw/Ber-Insight-logo-final.png" 
            alt="BerInsight" 
            style={{ width: '180px', height: 'auto' }}
          />
        ) : (
          <img 
            src="https://i.postimg.cc/NMjWTcGw/Ber-Insight-logo-final.png" 
            alt="B" 
            style={{ width: '40px', height: 'auto' }}
          />
        )}
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
                padding: isCollapsed ? '14px 8px' : '14px 20px',
                marginBottom: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: isCollapsed ? 'center' : 'flex-start',
                gap: isCollapsed ? '0' : '12px',
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
              title={isCollapsed ? item.label : ''}
            >
              <span style={{ fontSize: '20px' }}>{item.icon}</span>
              {!isCollapsed && <span>{item.label}</span>}
            </button>
          )
        })}
      </nav>

      {/* Footer */}
      {!isCollapsed && (
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
      )}
    </div>
    
    {/* Spacer div to push content */}
    <div style={{ 
      width: isCollapsed ? '80px' : '260px',
      transition: 'width 0.3s ease'
    }} />
    </>
  )
}

