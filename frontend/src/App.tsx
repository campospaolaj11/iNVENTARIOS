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
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <header className="page-header">
        <div className="container mx-auto px-4 py-8 relative z-10">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-white/20 backdrop-blur-sm p-3 rounded-xl">
                <span className="text-5xl">📦</span>
              </div>
              <div>
                <h1 className="text-4xl font-bold tracking-tight">Sistema de Inventarios</h1>
                <p className="text-primary-100 mt-1 text-lg">Dashboard de Control y Análisis en Tiempo Real</p>
              </div>
            </div>
            <div className="hidden md:flex items-center space-x-4">
              <div className="text-sm bg-white/20 backdrop-blur-sm px-4 py-2 rounded-lg border border-white/30">
                <span className="text-primary-100">Estado:</span>
                <span className="ml-2 font-semibold">{apiStatus}</span>
              </div>
              <div className="text-sm bg-white/20 backdrop-blur-sm px-4 py-2 rounded-lg border border-white/30">
                <span className="text-primary-100">Última actualización:</span>
                <span className="ml-2 font-semibold">{new Date().toLocaleDateString('es-MX')}</span>
              </div>
            </div>
          </div>
        </div>
        
        {/* Decoración ondas */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1440 120" className="w-full h-auto">
            <path fill="#f8fafc" fillOpacity="1" d="M0,64L48,69.3C96,75,192,85,288,80C384,75,480,53,576,48C672,43,768,53,864,58.7C960,64,1056,64,1152,58.7C1248,53,1344,43,1392,37.3L1440,32L1440,120L1392,120C1344,120,1248,120,1152,120C1056,120,960,120,864,120C768,120,672,120,576,120C480,120,384,120,288,120C192,120,96,120,48,120L0,120Z"></path>
          </svg>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 -mt-8 relative z-20">
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
