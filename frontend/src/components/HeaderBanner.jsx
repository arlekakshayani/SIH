import React, { useState, useEffect } from 'react'
import { Activity, ShieldCheck, Clock } from 'lucide-react'

export default function HeaderBanner() {
  const [time, setTime] = useState('')

  useEffect(() => {
    const updateTime = () => {
      const now = new Date()
      setTime(
        now.toLocaleTimeString('en-IN', {
          timeZone: 'Asia/Kolkata',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: true,
        }) + ' IST'
      )
    }
    updateTime()
    const timer = setInterval(updateTime, 1000)
    return () => clearInterval(timer)
  }, [])

  return (
    <header className="w-full bg-slate-950 border-b border-slate-800/80 text-xs py-2 px-4 sm:px-6 relative z-50">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-2 text-slate-400">
        
        {/* Left: Government of India Emblem text & Ministry */}
        <div className="flex items-center gap-2.5">
          <div className="flex items-center gap-2">
            {/* Ashoka Pillar Lion Capital Emblem Representation */}
            <div className="w-5 h-5 rounded-full bg-amber-500/10 border border-amber-500/40 flex items-center justify-center text-[10px] font-bold text-amber-400">
              🏛️
            </div>
            <span className="font-semibold text-slate-200 tracking-wide">
              सत्यमेव जयते
            </span>
          </div>
          <span className="text-slate-600">|</span>
          <span className="text-slate-300 font-medium">
            Government of India
          </span>
          <span className="hidden sm:inline text-slate-600">•</span>
          <span className="hidden sm:inline text-amber-400/90 font-medium">
            Ministry of Statistics & Programme Implementation (MoSPI)
          </span>
        </div>

        {/* Right: Operational Status & System Metric */}
        <div className="flex items-center gap-4 text-[11px]">
          <div className="hidden lg:flex items-center gap-1.5 text-slate-400">
            <Clock className="w-3.5 h-3.5 text-cyan-400" />
            <span className="font-mono text-slate-300">{time || '03:30:00 PM IST'}</span>
          </div>

          <div className="flex items-center gap-2 px-2.5 py-1 rounded-full bg-emerald-950/50 border border-emerald-500/30 text-emerald-300">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="font-medium tracking-wide">
              14 Scraping Engines Operational
            </span>
          </div>
        </div>

      </div>
    </header>
  )
}
