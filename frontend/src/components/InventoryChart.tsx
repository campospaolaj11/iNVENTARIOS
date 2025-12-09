import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface CategoryData {
  categoria: string
  stock: number
  minimo: number
}

function InventoryChart() {
  const [data, setData] = useState<CategoryData[]>([])

  useEffect(() => {
    loadChartData()
  }, [])

  const loadChartData = async () => {
    try {
      const response = await fetch('/mock-data.json')
      const jsonData = await response.json()
      setData(jsonData.stock_por_categoria)
    } catch (error) {
      console.error('Error cargando datos del gráfico:', error)
    }
  }

  return (
    <div className="card relative overflow-hidden group">
      <div className="absolute top-0 left-0 w-32 h-32 bg-gradient-to-br from-blue-200 to-cyan-200 rounded-full -ml-16 -mt-16 opacity-50 group-hover:scale-150 transition-transform duration-500"></div>
      
      <div className="relative">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
              <span className="text-3xl">📊</span>
              <span className="bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
                Stock por Categoría
              </span>
            </h3>
            <p className="text-sm text-gray-500 mt-1 font-medium">Comparativa de stock actual vs mínimo</p>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-blue-500"></div>
            <span className="text-xs text-gray-600 font-medium">Actual</span>
            <div className="w-3 h-3 rounded-full bg-red-500 ml-2"></div>
            <span className="text-xs text-gray-600 font-medium">Mínimo</span>
          </div>
        </div>
        
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <defs>
              <linearGradient id="stockGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#0ea5e9" stopOpacity={1}/>
                <stop offset="100%" stopColor="#06b6d4" stopOpacity={1}/>
              </linearGradient>
              <linearGradient id="minimoGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#ef4444" stopOpacity={1}/>
                <stop offset="100%" stopColor="#f97316" stopOpacity={1}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis 
              dataKey="categoria" 
              tick={{ fill: '#475569', fontSize: 12, fontWeight: 600 }}
              axisLine={{ stroke: '#cbd5e1' }}
            />
            <YAxis 
              tick={{ fill: '#475569', fontSize: 12, fontWeight: 600 }}
              axisLine={{ stroke: '#cbd5e1' }}
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'white',
                border: '2px solid #e2e8f0',
                borderRadius: '12px',
                boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
                padding: '12px'
              }}
              cursor={{ fill: 'rgba(59, 130, 246, 0.1)' }}
            />
            <Legend 
              wrapperStyle={{
                paddingTop: '24px',
                fontWeight: 600
              }}
            />
            <Bar 
              dataKey="stock" 
              fill="url(#stockGradient)" 
              name="Stock Actual" 
              radius={[10, 10, 0, 0]}
            />
            <Bar 
              dataKey="minimo" 
              fill="url(#minimoGradient)" 
              name="Stock Mínimo" 
              radius={[10, 10, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default InventoryChart
