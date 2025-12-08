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
    <div className="card">
      <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
        <span className="text-2xl mr-2">📊</span>
        Stock por Categoría
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis 
            dataKey="categoria" 
            tick={{ fill: '#64748b', fontSize: 12 }}
            axisLine={{ stroke: '#cbd5e1' }}
          />
          <YAxis 
            tick={{ fill: '#64748b', fontSize: 12 }}
            axisLine={{ stroke: '#cbd5e1' }}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e2e8f0',
              borderRadius: '8px',
              boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
            }}
          />
          <Legend 
            wrapperStyle={{
              paddingTop: '20px'
            }}
          />
          <Bar 
            dataKey="stock" 
            fill="#0ea5e9" 
            name="Stock Actual" 
            radius={[8, 8, 0, 0]}
          />
          <Bar 
            dataKey="minimo" 
            fill="#ef4444" 
            name="Stock Mínimo" 
            radius={[8, 8, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default InventoryChart
