import { useState, useEffect } from 'react'
import AddProductModal, { NewProduct } from './AddProductModal'

interface Product {
  id?: number
  codigo: string
  nombre: string
  stock_actual: number
  stock_minimo: number
  categoria: string
  ubicacion_bodega: string
  descripcion?: string
}

function ProductsTable() {
  const [products, setProducts] = useState<Product[]>([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [showSuccess, setShowSuccess] = useState(false)

  useEffect(() => {
    loadProducts()
  }, [])

  const loadProducts = async () => {
    try {
      const response = await fetch('/mock-data.json')
      const data = await response.json()
      
      const savedProducts = localStorage.getItem('inventario_productos')
      if (savedProducts) {
        const parsedProducts = JSON.parse(savedProducts)
        setProducts(parsedProducts)
      } else {
        setProducts(data.productos.slice(0, 10))
      }
    } catch (error) {
      console.error('Error cargando productos:', error)
    }
  }

  const handleAddProduct = (newProduct: NewProduct) => {
    const productWithId: Product = {
      ...newProduct,
      id: Date.now()
    }
    
    const updatedProducts = [...products, productWithId]
    setProducts(updatedProducts)
    localStorage.setItem('inventario_productos', JSON.stringify(updatedProducts))
    
    setShowSuccess(true)
    setTimeout(() => setShowSuccess(false), 3000)
  }

  const handleDeleteProduct = (codigo: string) => {
    if (confirm(`¿Estás seguro de eliminar el producto ${codigo}?`)) {
      const updatedProducts = products.filter(p => p.codigo !== codigo)
      setProducts(updatedProducts)
      localStorage.setItem('inventario_productos', JSON.stringify(updatedProducts))
    }
  }

  const getStockStatus = (actual: number, minimo: number) => {
    if (actual <= minimo) return 'text-red-600 font-bold'
    if (actual <= minimo * 1.5) return 'text-orange-600 font-semibold'
    return 'text-green-600'
  }

  return (
    <>
      <div className="card relative overflow-hidden">
        {/* Decoración de fondo */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full -mr-32 -mt-32 opacity-30"></div>
        
        {showSuccess && (
          <div className="mb-6 bg-gradient-to-r from-green-50 to-emerald-50 border-l-4 border-green-500 text-green-800 px-6 py-4 rounded-xl shadow-lg flex items-center animate-slide-up">
            <div className="flex items-center gap-4">
              <div className="text-3xl">✓</div>
              <div>
                <p className="font-bold text-lg">¡Éxito!</p>
                <p className="text-sm text-green-700">Producto agregado exitosamente al inventario</p>
              </div>
            </div>
          </div>
        )}

        <div className="relative flex flex-col md:flex-row items-start md:items-center justify-between mb-8 gap-4">
          <div>
            <h3 className="text-3xl font-black text-gray-800 flex items-center gap-3">
              <span className="text-4xl">📋</span>
              <span className="bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
                Productos en Inventario
              </span>
            </h3>
            <div className="flex items-center gap-3 mt-3">
              <div className="px-4 py-1.5 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-full text-sm font-bold shadow-lg">
                {products.length} productos
              </div>
              <div className="text-sm text-gray-500 font-medium">
                Actualizado en tiempo real
              </div>
            </div>
          </div>
          <button 
            onClick={() => setIsModalOpen(true)}
            className="group relative px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300 font-bold text-sm overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-600 to-blue-600 opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div className="relative flex items-center gap-2">
              <span className="text-xl">+</span>
              <span>Agregar Producto</span>
            </div>
          </button>
        </div>

        <div className="overflow-x-auto rounded-xl border-2 border-gray-200 shadow-xl">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gradient-to-r from-gray-800 to-gray-700">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-black text-white uppercase tracking-wider">Código</th>
                <th className="px-6 py-4 text-left text-xs font-black text-white uppercase tracking-wider">Nombre</th>
                <th className="px-6 py-4 text-left text-xs font-black text-white uppercase tracking-wider">Categoría</th>
                <th className="px-6 py-4 text-left text-xs font-black text-white uppercase tracking-wider">Stock</th>
                <th className="px-6 py-4 text-left text-xs font-black text-white uppercase tracking-wider">Mínimo</th>
                <th className="px-6 py-4 text-left text-xs font-black text-white uppercase tracking-wider">Ubicación</th>
                <th className="px-6 py-4 text-left text-xs font-black text-white uppercase tracking-wider">Estado</th>
                <th className="px-6 py-4 text-left text-xs font-black text-white uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-100">{products.map((product) => (
                <tr key={product.codigo} className="hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50 transition-all duration-200 group">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="text-sm font-black text-gray-900 bg-gray-100 px-3 py-1 rounded-lg">{product.codigo}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-bold">{product.nombre}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className="px-3 py-1.5 rounded-lg bg-gradient-to-r from-gray-100 to-gray-200 text-gray-800 text-xs font-bold shadow-sm">
                      {product.categoria}
                    </span>
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm font-black ${getStockStatus(product.stock_actual, product.stock_minimo)}`}>
                    {product.stock_actual}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700 font-bold">{product.stock_minimo}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className="px-3 py-1.5 rounded-lg bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-800 text-xs font-bold shadow-sm">
                      {product.ubicacion_bodega}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    {product.stock_actual <= product.stock_minimo ? (
                      <span className="px-3 py-1.5 text-xs font-black rounded-lg bg-gradient-to-r from-red-100 to-red-200 text-red-800 shadow-md">⚠️ Crítico</span>
                    ) : product.stock_actual <= product.stock_minimo * 1.5 ? (
                      <span className="px-3 py-1.5 text-xs font-black rounded-lg bg-gradient-to-r from-orange-100 to-orange-200 text-orange-800 shadow-md">⚡ Bajo</span>
                    ) : (
                      <span className="px-3 py-1.5 text-xs font-black rounded-lg bg-gradient-to-r from-green-100 to-emerald-200 text-green-800 shadow-md">✓ Normal</span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <button
                      onClick={() => handleDeleteProduct(product.codigo)}
                      className="text-red-600 hover:text-white hover:bg-red-600 px-3 py-2 rounded-lg transition-all duration-200 font-bold shadow-sm hover:shadow-lg transform hover:scale-110"
                      title="Eliminar producto"
                    >
                      🗑️
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <AddProductModal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onAdd={handleAddProduct}
      />
    </>
  )
}

export default ProductsTable
