import { useState } from 'react'

interface AddProductModalProps {
  isOpen: boolean
  onClose: () => void
  onAdd: (product: NewProduct) => void
}

export interface NewProduct {
  codigo: string
  nombre: string
  categoria: string
  stock_actual: number
  stock_minimo: number
  costo_unitario: number
  precio_venta: number
  ubicacion_bodega: string
  descripcion?: string
}

function AddProductModal({ isOpen, onClose, onAdd }: AddProductModalProps) {
  const [formData, setFormData] = useState<NewProduct>({
    codigo: '',
    nombre: '',
    categoria: 'Ferretería',
    stock_actual: 0,
    stock_minimo: 10,
    costo_unitario: 0,
    precio_venta: 0,
    ubicacion_bodega: '',
    descripcion: ''
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onAdd(formData)
    // Reset form
    setFormData({
      codigo: '',
      nombre: '',
      categoria: 'Ferretería',
      stock_actual: 0,
      stock_minimo: 10,
      costo_unitario: 0,
      precio_venta: 0,
      ubicacion_bodega: '',
      descripcion: ''
    })
    onClose()
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: ['stock_actual', 'stock_minimo', 'costo_unitario', 'precio_venta'].includes(name) 
        ? parseFloat(value) || 0 
        : value
    }))
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 animate-fade-in">
      <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto animate-slide-up">
        <div className="sticky top-0 bg-gradient-to-r from-primary-600 to-primary-700 text-white px-6 py-4 rounded-t-xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <span className="text-3xl">📦</span>
              <h2 className="text-2xl font-bold">Agregar Nuevo Producto</h2>
            </div>
            <button 
              onClick={onClose}
              className="text-white hover:bg-white/20 rounded-lg p-2 transition-colors"
            >
              <span className="text-2xl">✕</span>
            </button>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Código */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Código del Producto *
              </label>
              <input
                type="text"
                name="codigo"
                value={formData.codigo}
                onChange={handleChange}
                required
                placeholder="PROD001"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
            </div>

            {/* Nombre */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Nombre del Producto *
              </label>
              <input
                type="text"
                name="nombre"
                value={formData.nombre}
                onChange={handleChange}
                required
                placeholder="Tornillo M8x20"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
            </div>

            {/* Categoría */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Categoría *
              </label>
              <select
                name="categoria"
                value={formData.categoria}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              >
                <option value="Ferretería">Ferretería</option>
                <option value="Eléctricos">Eléctricos</option>
                <option value="Plomería">Plomería</option>
                <option value="Pintura">Pintura</option>
                <option value="Herramientas">Herramientas</option>
              </select>
            </div>

            {/* Ubicación */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Ubicación Bodega *
              </label>
              <input
                type="text"
                name="ubicacion_bodega"
                value={formData.ubicacion_bodega}
                onChange={handleChange}
                required
                placeholder="A-01"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
            </div>

            {/* Stock Actual */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Stock Actual *
              </label>
              <input
                type="number"
                name="stock_actual"
                value={formData.stock_actual}
                onChange={handleChange}
                required
                min="0"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
            </div>

            {/* Stock Mínimo */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Stock Mínimo *
              </label>
              <input
                type="number"
                name="stock_minimo"
                value={formData.stock_minimo}
                onChange={handleChange}
                required
                min="0"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
            </div>

            {/* Costo Unitario */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Costo Unitario ($) *
              </label>
              <input
                type="number"
                name="costo_unitario"
                value={formData.costo_unitario}
                onChange={handleChange}
                required
                min="0"
                step="0.01"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
            </div>

            {/* Precio Venta */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Precio Venta ($) *
              </label>
              <input
                type="number"
                name="precio_venta"
                value={formData.precio_venta}
                onChange={handleChange}
                required
                min="0"
                step="0.01"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
            </div>
          </div>

          {/* Descripción */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Descripción
            </label>
            <textarea
              name="descripcion"
              value={formData.descripcion}
              onChange={handleChange}
              rows={3}
              placeholder="Descripción detallada del producto..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
            />
          </div>

          {/* Botones */}
          <div className="flex items-center justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="btn-primary"
            >
              ✓ Agregar Producto
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default AddProductModal
