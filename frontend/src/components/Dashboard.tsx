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

      {/* Sección de Análisis */}
      <div className="card">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">📊 Análisis de Inventario</h2>
        <p className="text-gray-600 mb-6">Visualización en tiempo real del estado de tu inventario</p>
      </div>

      {/* Gráficas */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <InventoryChart />
        <div className="card">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <span className="text-2xl mr-2">📈</span>
            Rotación de Inventario
          </h3>
          <div className="h-64 flex items-center justify-center bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg">
            <div className="text-center">
              <div className="text-6xl mb-4">🔄</div>
              <p className="text-gray-600 font-medium">Gráfica de rotación</p>
              <p className="text-gray-400 text-sm mt-2">(Próximamente)</p>
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
