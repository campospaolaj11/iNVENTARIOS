import { useState, useEffect } from 'react'
import axios from 'axios'
import StatsCard from './StatsCard'
import ProductsTable from './ProductsTable'
import InventoryChart from './InventoryChart'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const USE_MOCK_DATA = !import.meta.env.VITE_API_URL || import.meta.env.VITE_USE_MOCK === 'true'

interface KPI {
  total_productos: number
  productos_criticos: number
  valor_inventario: number
  costo_almacenamiento_total: number
}

function Dashboard() {
  const [kpis, setKpis] = useState<KPI | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadKPIs()
  }, [])

  const loadKPIs = async () => {
    try {
      if (USE_MOCK_DATA) {
        // Cargar datos desde archivo JSON local
        const response = await fetch('/mock-data.json')
        const data = await response.json()
        setKpis(data.kpis)
      } else {
        // Cargar datos desde API
        const response = await axios.get(`${API_URL}/api/kpis`)
        setKpis(response.data)
      }
      
      setLoading(false)
    } catch (error) {
      console.error('Error cargando KPIs:', error)
      // Fallback a datos mock si falla la API
      const response = await fetch('/mock-data.json')
      const data = await response.json()
      setKpis(data.kpis)
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="space-y-8">
        {/* Loading Skeletons */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="loading-skeleton h-32 rounded-xl"></div>
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="loading-skeleton h-96 rounded-xl"></div>
          <div className="loading-skeleton h-96 rounded-xl"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8 animate-fade-in">
      {/* KPIs Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Productos"
          value={kpis?.total_productos || 0}
          icon="📦"
          color="blue"
        />
        <StatsCard
          title="Stock Crítico"
          value={kpis?.productos_criticos || 0}
          icon="⚠️"
          color="red"
        />
        <StatsCard
          title="Valor Inventario"
          value={`$${(kpis?.valor_inventario || 0).toLocaleString('es-MX')}`}
          icon="💰"
          color="green"
        />
        <StatsCard
          title="Costo Almacenamiento"
          value={`$${(kpis?.costo_almacenamiento_total || 0).toLocaleString('es-MX')}`}
          icon="🏭"
          color="orange"
        />
      </div>

      {/* Sección de Análisis - ULTRA MEJORADA */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-violet-600 via-purple-600 to-fuchsia-600 p-10 shadow-2xl group">
        {/* Patrón animado de fondo */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0 animate-pulse" style={{
            backgroundImage: 'radial-gradient(circle at 20% 50%, white 2px, transparent 2px), radial-gradient(circle at 80% 80%, white 2px, transparent 2px), radial-gradient(circle at 40% 20%, white 1px, transparent 1px)',
            backgroundSize: '50px 50px, 80px 80px, 100px 100px'
          }}></div>
        </div>
        
        {/* Círculos decorativos flotantes */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -mr-32 -mt-32 group-hover:scale-150 transition-transform duration-700"></div>
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/10 rounded-full -ml-24 -mb-24 group-hover:scale-150 transition-transform duration-700"></div>
        <div className="absolute top-1/2 left-1/2 w-32 h-32 bg-white/5 rounded-full -ml-16 -mt-16 animate-pulse"></div>
        
        {/* Contenido */}
        <div className="relative z-10">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            {/* Lado izquierdo - Texto */}
            <div className="flex-1">
              <div className="flex items-center gap-4 mb-3">
                <div className="relative">
                  <div className="absolute inset-0 bg-white/30 blur-xl rounded-full"></div>
                  <div className="relative bg-white/20 backdrop-blur-md p-4 rounded-2xl border border-white/30 shadow-2xl">
                    <span className="text-5xl filter drop-shadow-lg">📊</span>
                  </div>
                </div>
                <div>
                  <h2 className="text-4xl md:text-5xl font-black text-white drop-shadow-lg mb-1">
                    Análisis de Inventario
                  </h2>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                    <span className="text-white/90 text-sm font-semibold">Datos en tiempo real</span>
                  </div>
                </div>
              </div>
              <p className="text-white/95 text-lg md:text-xl font-medium leading-relaxed max-w-2xl">
                Visualización profesional y detallada del estado completo de tu inventario con métricas actualizadas al instante
              </p>
            </div>
            
            {/* Lado derecho - Stats rápidos */}
            <div className="flex gap-4">
              <div className="bg-white/20 backdrop-blur-md rounded-2xl p-6 border border-white/30 shadow-xl hover:scale-105 transition-transform">
                <div className="text-center">
                  <div className="text-3xl font-black text-white mb-1">{kpis?.total_productos || 0}</div>
                  <div className="text-white/80 text-xs font-semibold uppercase tracking-wide">Productos</div>
                </div>
              </div>
              <div className="bg-white/20 backdrop-blur-md rounded-2xl p-6 border border-white/30 shadow-xl hover:scale-105 transition-transform">
                <div className="text-center">
                  <div className="text-3xl font-black text-white mb-1">{kpis?.productos_criticos || 0}</div>
                  <div className="text-white/80 text-xs font-semibold uppercase tracking-wide">Alertas</div>
                </div>
              </div>
              <div className="bg-white/20 backdrop-blur-md rounded-2xl p-6 border border-white/30 shadow-xl hover:scale-105 transition-transform">
                <div className="text-center">
                  <div className="text-3xl font-black text-white mb-1">5</div>
                  <div className="text-white/80 text-xs font-semibold uppercase tracking-wide">Categorías</div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Barra de información adicional */}
          <div className="mt-6 flex flex-wrap items-center gap-4 pt-6 border-t border-white/20">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-blue-400"></div>
              <span className="text-white/90 text-sm font-medium">Stock Actual</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-red-400"></div>
              <span className="text-white/90 text-sm font-medium">Stock Mínimo</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-green-400"></div>
              <span className="text-white/90 text-sm font-medium">Stock Óptimo</span>
            </div>
            <div className="ml-auto flex items-center gap-2 bg-white/10 px-4 py-2 rounded-full">
              <span className="text-white/80 text-sm">Última actualización:</span>
              <span className="text-white font-bold text-sm">{new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' })}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Gráficas */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <InventoryChart />
        <div className="card relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-purple-200 to-pink-200 rounded-full -mr-16 -mt-16 opacity-50 group-hover:scale-150 transition-transform duration-500"></div>
          <div className="relative">
            <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <span className="text-3xl">📈</span>
              <span>Rotación de Inventario</span>
            </h3>
            <div className="h-64 flex items-center justify-center bg-gradient-to-br from-purple-50 via-pink-50 to-purple-100 rounded-xl border-2 border-dashed border-purple-200 relative overflow-hidden">
              <div className="absolute inset-0 opacity-10">
                <div className="absolute inset-0" style={{
                  backgroundImage: 'radial-gradient(circle at 2px 2px, currentColor 1px, transparent 0)',
                  backgroundSize: '24px 24px',
                  color: '#a855f7'
                }}></div>
              </div>
              <div className="text-center relative z-10">
                <div className="text-7xl mb-4 floating">🔄</div>
                <p className="text-gray-700 font-bold text-lg">Gráfica de rotación</p>
                <p className="text-purple-600 text-sm mt-2 font-semibold">(Próximamente)</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabla de Productos */}
      <ProductsTable />
    </div>
  )
}

export default Dashboard
