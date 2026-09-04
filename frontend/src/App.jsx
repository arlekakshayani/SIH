import React, { useState, useEffect } from 'react'
import HeaderBanner from './components/HeaderBanner'
import Navbar from './components/Navbar'
import HeroSection from './components/HeroSection'
import LivePipelineHealth from './components/LivePipelineHealth'
import LiveDemoTable from './components/LiveDemoTable'
import Footer from './components/Footer'
import Dashboard from './components/Dashboard'
import RouteAnalytics from './components/RouteAnalytics'

export default function App() {
  // 'overview' | 'pipeline-health' | 'corridors' | 'radar' | 'dashboard'
  const [currentView, setCurrentView] = useState('overview')

  // Listen to hash changes for deep linking (#overview, #pipeline-health, #corridors, #radar, #dashboard)
  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.replace('#', '')
      if (['overview', 'pipeline-health', 'corridors', 'radar', 'dashboard'].includes(hash)) {
        setCurrentView(hash)
      }
    }

    const initialHash = window.location.hash.replace('#', '')
    if (['overview', 'pipeline-health', 'corridors', 'radar', 'dashboard'].includes(initialHash)) {
      setCurrentView(initialHash)
    }

    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [])

  // Navigation handler: directly switches the active view without page scrolling
  const handleNavigate = (view) => {
    window.location.hash = `#${view}`
    setCurrentView(view)
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-cyan-500 selection:text-slate-950">
      
      {/* 1. Official Header Banner */}
      <HeaderBanner />

      {/* 2. Top Navigation Bar with Direct View Switching Tabs */}
      <Navbar
        currentView={currentView}
        onNavigate={handleNavigate}
      />

      {/* 3. Main Content: Discrete View Panels (Zero Scrolling) */}
      <main className="flex-grow">
        {currentView === 'overview' && (
          <HeroSection onNavigate={handleNavigate} />
        )}

        {currentView === 'pipeline-health' && (
          <LivePipelineHealth />
        )}

        {currentView === 'corridors' && (
          <LiveDemoTable />
        )}

        {currentView === 'radar' && (
          <RouteAnalytics
            onBackToLanding={() => handleNavigate('overview')}
            onGoToDashboard={() => handleNavigate('dashboard')}
          />
        )}

        {currentView === 'dashboard' && (
          <Dashboard
            onBackToLanding={() => handleNavigate('overview')}
            onGoToRouteAnalytics={() => handleNavigate('radar')}
          />
        )}
      </main>

      {/* 4. Official Footer */}
      <Footer onOpenDashboard={() => handleNavigate('dashboard')} />

    </div>
  )
}
