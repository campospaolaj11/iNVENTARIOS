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
      <div className="card">
        {showSuccess && (
          <div className="mb-4 bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg flex items-center animate-slide-up">
            <span className="text-2xl mr-3">✓</span>
            <span className="font-medium">¡Producto agregado exitosamente!</span>
          </div>
        )}

        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-2xl font-bold text-gray-800 flex items-center">
              <span className="text-2xl mr-2">📋</span>
              Productos en Inventario
            </h3>
            <p className="text-gray-600 text-sm mt-1">
              {products.length} productos registrados
            </p>
          </div>
          <button 
            onClick={() => setIsModalOpen(true)}
            className="btn-primary flex items-center space-x-2"
          >
            <span>+</span>
            <span>Agregar Producto</span>
          </button>
        </div>

        <div className="overflow-x-auto rounded-lg border border-gray-200">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gradient-to-r from-gray-50 to-gray-100">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase">Código</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase">Nombre</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase">Categoría</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase">Stock</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase">Mínimo</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase">Ubicación</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase">Estado</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase">Acciones</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {products.map((product) => (
                <tr key={product.codigo} className="hover:bg-blue-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">{product.codigo}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">{product.nombre}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className="px-3 py-1 rounded-full bg-gray-100 text-gray-700 text-xs font-medium">
                      {product.categoria}
                    </span>
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm font-bold ${getStockStatus(product.stock_actual, product.stock_minimo)}`}>
                    {product.stock_actual}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 font-medium">{product.stock_minimo}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className="px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-xs font-medium">
                      {product.ubicacion_bodega}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    {product.stock_actual <= product.stock_minimo ? (
                      <span className="px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800">⚠️ Crítico</span>
                    ) : product.stock_actual <= product.stock_minimo * 1.5 ? (
                      <span className="px-2 py-1 text-xs font-semibold rounded-full bg-orange-100 text-orange-800">⚡ Bajo</span>
                    ) : (
                      <span className="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">✓ Normal</span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <button
                      onClick={() => handleDeleteProduct(product.codigo)}
                      className="text-red-600 hover:text-red-800 hover:bg-red-50 px-3 py-1 rounded transition-colors"
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
