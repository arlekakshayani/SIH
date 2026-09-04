import React, { useState } from 'react'
import { Plane, Activity, Table, Terminal, Menu, X, ArrowRight } from 'lucide-react'

export default function Navbar({ currentView, onNavigate }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navItems = [
    { id: 'overview', name: 'Overview' },
    { id: 'pipeline-health', name: 'Pipeline Health' },
    { id: 'corridors', name: 'Live Corridors' },
  ]

  return (
    <nav className="sticky top-0 z-40 w-full backdrop-blur-xl bg-slate-950/90 border-b border-slate-800 transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 sm:h-20">
          
          {/* Logo & Seal */}
          <button
            onClick={() => onNavigate('overview')}
            className="flex items-center gap-3 group text-left focus:outline-none"
          >
            <div className="relative flex items-center justify-center w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-gradient-to-br from-slate-900 via-slate-800 to-slate-950 border border-cyan-500/40 shadow-lg shadow-cyan-500/10 group-hover:border-cyan-400 transition-all">
              <Plane className="w-5 h-5 text-cyan-400 transform -rotate-45 group-hover:scale-110 transition-transform" />
              <div className="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-amber-500 flex items-center justify-center text-[8px] font-black text-slate-950">
                IN
              </div>
            </div>
            
            <div className="flex flex-col">
              <div className="flex items-center gap-2">
                <span className="text-lg sm:text-xl font-bold font-heading tracking-tight text-white group-hover:text-cyan-300 transition-colors">
                  AirIndex <span className="text-amber-400">MoSPI</span>
                </span>
                <span className="hidden sm:inline-block px-1.5 py-0.5 rounded text-[10px] font-mono font-semibold bg-cyan-950/80 text-cyan-300 border border-cyan-500/30">
                  SIH26056
                </span>
              </div>
              <span className="text-[11px] text-slate-400 font-medium tracking-wide">
                National Airfare CPI Augmentation System
              </span>
            </div>
          </button>

          {/* Desktop Navigation Tabs (Direct View Switching, Zero Scrolling) */}
          <div className="hidden md:flex items-center gap-2 bg-slate-900/80 p-1 rounded-xl border border-slate-800/90">
            {navItems.map((item) => {
              const isActive = currentView === item.id
              return (
                <button
                  key={item.id}
                  onClick={() => onNavigate(item.id)}
                  className={`px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-slate-800 text-cyan-300 font-bold border border-cyan-500/40 shadow-sm shadow-cyan-500/20'
                      : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                  }`}
                >
                  {item.name}
                </button>
              )
            })}
          </div>

          {/* Action Navigation Buttons */}
          <div className="hidden md:flex items-center gap-3">
            <button
              onClick={() => onNavigate('radar')}
              className={`inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-semibold transition-all ${
                currentView === 'radar'
                  ? 'bg-purple-600 text-white shadow-md shadow-purple-500/25 border border-purple-400'
                  : 'text-purple-300 bg-slate-900 hover:bg-slate-800 border border-purple-500/40 hover:border-purple-400'
              }`}
            >
              <Plane className="w-3.5 h-3.5 transform -rotate-45" />
              <span>Route Radar</span>
            </button>

            <button
              onClick={() => onNavigate('dashboard')}
              className={`group relative inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all active:scale-95 ${
                currentView === 'dashboard'
                  ? 'bg-amber-400 text-slate-950 shadow-lg shadow-amber-500/30 font-bold'
                  : 'text-slate-950 bg-gradient-to-r from-amber-400 via-amber-500 to-amber-400 hover:from-amber-300 hover:to-amber-500 shadow-md shadow-amber-500/20'
              }`}
            >
              <Terminal className="w-4 h-4" />
              <span>Executive Dashboard</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
            </button>
          </div>

          {/* Mobile Menu Toggle */}
          <div className="md:hidden flex items-center gap-2">
            <button
              onClick={() => onNavigate('dashboard')}
              className="px-2.5 py-1.5 rounded-lg text-xs font-semibold text-slate-950 bg-amber-400 hover:bg-amber-300"
            >
              Dashboard
            </button>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 focus:outline-none"
              aria-label="Toggle Navigation"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-slate-950 border-b border-slate-800 px-4 pt-3 pb-5 space-y-2">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => {
                setMobileMenuOpen(false)
                onNavigate(item.id)
              }}
              className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium ${
                currentView === item.id
                  ? 'bg-slate-800 text-cyan-300 font-bold'
                  : 'text-slate-300 hover:text-white hover:bg-slate-900'
              }`}
            >
              {item.name}
            </button>
          ))}

          <button
            onClick={() => {
              setMobileMenuOpen(false)
              onNavigate('radar')
            }}
            className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium ${
              currentView === 'radar'
                ? 'bg-purple-900/60 text-purple-300 font-bold'
                : 'text-purple-300 hover:bg-slate-900'
            }`}
          >
            Route Radar
          </button>

          <div className="pt-2 border-t border-slate-800">
            <button
              onClick={() => {
                setMobileMenuOpen(false)
                onNavigate('dashboard')
              }}
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-sm font-semibold text-slate-950 bg-amber-400"
            >
              <Terminal className="w-4 h-4" />
              Executive Dashboard
            </button>
          </div>
        </div>
      )}
    </nav>
  )
}
