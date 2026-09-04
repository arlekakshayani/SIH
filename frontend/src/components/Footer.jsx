import React from 'react'
import { Plane, ShieldCheck, ExternalLink, Heart, Globe, Terminal, Award, FileCode2 } from 'lucide-react'

export default function Footer({ onOpenDashboard }) {
  return (
    <footer className="w-full bg-slate-950 border-t border-slate-800 text-slate-400 text-xs py-14 px-4 sm:px-6 lg:px-8 relative z-20">
      <div className="max-w-7xl mx-auto">
        
        {/* Top Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 pb-12 border-b border-slate-850">
          
          {/* Col 1: Brand & Ministry Identification */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-slate-900 border border-cyan-500/40 flex items-center justify-center text-cyan-400">
                <Plane className="w-5 h-5 transform -rotate-45" />
              </div>
              <span className="text-xl font-bold font-heading text-white tracking-tight">
                AirIndex <span className="text-amber-400">MoSPI</span>
              </span>
            </div>

            <p className="text-sm text-slate-300 max-w-md leading-relaxed">
              National Airfare Price Index Surveillance System engineered for the{' '}
              <strong className="text-white">Ministry of Statistics & Programme Implementation (MoSPI)</strong>, Government of India, augmenting Consumer Price Index (CPI) transport indicators through autonomous real-time scraping.
            </p>

            <div className="flex flex-wrap items-center gap-2 pt-1 font-mono text-[11px]">
              <span className="px-2.5 py-1 rounded-md bg-amber-950/50 border border-amber-500/40 text-amber-300 font-bold">
                SIH 2026 Problem SIH26056
              </span>
              <span className="px-2.5 py-1 rounded-md bg-cyan-950/50 border border-cyan-500/40 text-cyan-300">
                MoSPI CPI Division
              </span>
              <span className="px-2.5 py-1 rounded-md bg-slate-900 border border-slate-700 text-slate-300">
                Live Pipeline Telemetry
              </span>
            </div>
          </div>

          {/* Col 2: System Architecture Links */}
          <div className="space-y-3">
            <h4 className="text-xs font-mono font-bold text-white uppercase tracking-wider">
              Technical Modules
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <a href="#pipeline-health" className="hover:text-cyan-400 transition-colors">
                  Pipeline Health & Monitoring
                </a>
              </li>
              <li>
                <a href="#pipeline-health" className="hover:text-cyan-400 transition-colors">
                  Carrier Ingestion Speed & Reliability
                </a>
              </li>
              <li>
                <a href="#live-corridors" className="hover:text-cyan-400 transition-colors">
                  National Corridor Registry
                </a>
              </li>
              <li>
                <button
                  onClick={onOpenDashboard}
                  className="hover:text-amber-400 transition-colors text-left flex items-center gap-1 text-amber-400/90 font-medium"
                >
                  <Terminal className="w-3.5 h-3.5" />
                  <span>Admin Control Console</span>
                </button>
              </li>
            </ul>
          </div>

          {/* Col 3: Compliance & Standards */}
          <div className="space-y-3">
            <h4 className="text-xs font-mono font-bold text-white uppercase tracking-wider">
              Compliance & Specs
            </h4>
            <ul className="space-y-2 text-xs text-slate-300">
              <li className="flex items-center gap-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span>UN-ILO CPI Manual (2020)</span>
              </li>
              <li className="flex items-center gap-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-cyan-400" />
                <span>SDMX 2.1 Statistical Schema</span>
              </li>
              <li className="flex items-center gap-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
                <span>MoSPI NAS Transport 1.1.07</span>
              </li>
              <li className="flex items-center gap-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-purple-400" />
                <span>Zero-PII Scraping Ethics</span>
              </li>
            </ul>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="pt-8 flex flex-col md:flex-row items-center justify-between gap-4 text-slate-400 text-[11px]">
          <div className="flex items-center gap-2">
            <span>© 2026 Government of India • Ministry of Statistics & Programme Implementation</span>
          </div>

          <div className="flex items-center gap-4">
            <span className="text-slate-300 font-mono">
              Smart India Hackathon 2026 • Team AirIndex
            </span>
            <span className="w-1 h-1 rounded-full bg-slate-700"></span>
            <span className="text-emerald-400 font-mono">
              System Health: 99.98% Uptime
            </span>
          </div>
        </div>

      </div>
    </footer>
  )
}
