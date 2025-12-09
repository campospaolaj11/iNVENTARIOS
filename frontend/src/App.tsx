import { useState, useEffect } from 'react'
import axios from 'axios'
import Dashboard from './components/Dashboard'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [apiStatus, setApiStatus] = useState<string>('checking...')

  useEffect(() => {
    // Verificar conexión con API
    axios.get(`${API_URL}/health`)
      .then(() => setApiStatus('✅ Conectado'))
      .catch(() => setApiStatus('📊 Modo Demo'))
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <header className="bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700 shadow-xl sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo y Título - Compacto */}
            <div className="flex items-center gap-4">
              <div className="relative group">
                <div className="absolute inset-0 bg-white/20 blur-lg rounded-xl"></div>
                <div className="relative bg-white/90 backdrop-blur-sm p-2.5 rounded-xl shadow-lg group-hover:scale-105 transition-transform">
                  <span className="text-3xl">📦</span>
                </div>
              </div>
              <div>
                <h1 className="text-2xl font-black text-white tracking-tight">
                  Sistema de Inventarios
                </h1>
                <p className="text-blue-100 text-xs font-medium mt-0.5">Dashboard Profesional</p>
              </div>
            </div>
            
            {/* Indicadores - Compactos */}
            <div className="flex items-center gap-3">
              <div className="bg-white/15 backdrop-blur-md px-4 py-2 rounded-lg border border-white/25 flex items-center gap-2">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-white text-sm font-semibold">{apiStatus}</span>
              </div>
              <div className="bg-white/15 backdrop-blur-md px-4 py-2 rounded-lg border border-white/25 flex items-center gap-2">
                <span className="text-xl">🕐</span>
                <span className="text-white text-sm font-semibold">
                  {new Date().toLocaleDateString('es-MX', { day: '2-digit', month: 'short' })}
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-6 py-8">
        <Dashboard />
      </main>

      <footer className="bg-gradient-to-r from-gray-800 via-gray-900 to-gray-800 text-gray-300 py-8 mt-16">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-center md:text-left mb-4 md:mb-0">
              <p className="font-semibold text-lg">Sistema de Inventarios Automatizado</p>
              <p className="text-gray-400 text-sm mt-1">© 2025 - Todos los derechos reservados</p>
            </div>
            <div className="flex items-center space-x-6">
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <span className="text-2xl">📊</span>
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <span className="text-2xl">📈</span>
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <span className="text-2xl">⚙️</span>
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
