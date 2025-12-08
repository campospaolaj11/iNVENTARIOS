import React, { useState } from 'react';
import { Camera, Package, MapPin, History, X, Check } from 'lucide-react';

interface ProductoEscaneado {
  codigo: string;
  nombre: string;
  stock_actual: number;
  stock_minimo: number;
  ubicacion_bodega: string;
  categoria: string;
  precio_venta: number;
}

interface ScanResult {
  tipo: 'producto' | 'ubicacion';
  encontrado: boolean;
  data: ProductoEscaneado | any;
  acciones_disponibles?: Array<{
    id: string;
    label: string;
    color: string;
  }>;
}

const ScannerComponent: React.FC = () => {
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState<ScanResult | null>(null);
  const [movimiento, setMovimiento] = useState<{
    tipo: 'ENTRADA' | 'SALIDA';
    cantidad: number;
  }>({ tipo: 'ENTRADA', cantidad: 0 });

  // Simulador de escaneo (en móvil real usarías la cámara)
  const handleScan = async (codigo: string) => {
    try {
      // Llamar a la API
      const response = await fetch(`http://localhost:8000/api/scanner/escanear?codigo=${codigo}`);
      const data: ScanResult = await response.json();
      
      setResult(data);
      setScanning(false);
    } catch (error) {
      console.error('Error al escanear:', error);
      alert('Error al procesar el código');
    }
  };

  // Simulador de entrada manual
  const handleManualInput = () => {
    const codigo = prompt('Ingresa el código manualmente:');
    if (codigo) {
      handleScan(codigo);
    }
  };

  const handleMovimientoRapido = async () => {
    if (!result || result.tipo !== 'producto') return;

    try {
      const response = await fetch('http://localhost:8000/api/scanner/movimiento-rapido', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          codigo_producto: result.data.codigo,
          tipo_movimiento: movimiento.tipo,
          cantidad: movimiento.cantidad,
          usuario_movil: 'Usuario Móvil'
        })
      });

      const data = await response.json();
      
      if (data.exito) {
        alert(`✅ ${data.mensaje}\nNuevo stock: ${data.nuevo_stock}`);
        setResult(null);
        setMovimiento({ tipo: 'ENTRADA', cantidad: 0 });
      }
    } catch (error) {
      alert('Error al registrar movimiento');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Package className="w-6 h-6 text-blue-600" />
            <h1 className="text-xl font-bold text-gray-800">Scanner Inventario</h1>
          </div>
          <button
            onClick={() => setScanning(!scanning)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700 transition"
          >
            <Camera className="w-5 h-5" />
            {scanning ? 'Detener' : 'Escanear'}
          </button>
        </div>
      </div>

      {/* Scanner Simulado */}
      {scanning && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-4">
          <div className="border-4 border-dashed border-blue-400 rounded-lg p-8 text-center">
            <Camera className="w-16 h-16 text-blue-600 mx-auto mb-4 animate-pulse" />
            <p className="text-gray-600 mb-4">Apunta la cámara al código QR/Barras</p>
            
            {/* Botones de simulación */}
            <div className="flex gap-2 justify-center">
              <button
                onClick={() => handleScan('PROD001')}
                className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600"
              >
                Simular Producto
              </button>
              <button
                onClick={() => handleScan('A-01')}
                className="bg-purple-500 text-white px-4 py-2 rounded-lg hover:bg-purple-600"
              >
                Simular Ubicación
              </button>
              <button
                onClick={handleManualInput}
                className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
              >
                Entrada Manual
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Resultado del Escaneo */}
      {result && result.tipo === 'producto' && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-4 animate-fade-in">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h2 className="text-2xl font-bold text-gray-800">{result.data.nombre}</h2>
              <p className="text-gray-500">Código: {result.data.codigo}</p>
            </div>
            <button
              onClick={() => setResult(null)}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Información del Producto */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-blue-50 rounded-lg p-4">
              <p className="text-sm text-gray-600">Stock Actual</p>
              <p className="text-2xl font-bold text-blue-600">{result.data.stock_actual}</p>
            </div>
            <div className="bg-orange-50 rounded-lg p-4">
              <p className="text-sm text-gray-600">Stock Mínimo</p>
              <p className="text-2xl font-bold text-orange-600">{result.data.stock_minimo}</p>
            </div>
            <div className="bg-green-50 rounded-lg p-4">
              <p className="text-sm text-gray-600">Precio Venta</p>
              <p className="text-2xl font-bold text-green-600">${result.data.precio_venta}</p>
            </div>
            <div className="bg-purple-50 rounded-lg p-4 flex items-center gap-2">
              <MapPin className="w-5 h-5 text-purple-600" />
              <div>
                <p className="text-sm text-gray-600">Ubicación</p>
                <p className="text-lg font-bold text-purple-600">{result.data.ubicacion_bodega}</p>
              </div>
            </div>
          </div>

          {/* Movimiento Rápido */}
          <div className="border-t pt-4">
            <h3 className="text-lg font-semibold mb-3">Movimiento Rápido</h3>
            
            <div className="flex gap-2 mb-3">
              <button
                onClick={() => setMovimiento({ ...movimiento, tipo: 'ENTRADA' })}
                className={`flex-1 py-3 rounded-lg font-semibold transition ${
                  movimiento.tipo === 'ENTRADA'
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                ➕ Entrada
              </button>
              <button
                onClick={() => setMovimiento({ ...movimiento, tipo: 'SALIDA' })}
                className={`flex-1 py-3 rounded-lg font-semibold transition ${
                  movimiento.tipo === 'SALIDA'
                    ? 'bg-red-500 text-white'
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                ➖ Salida
              </button>
            </div>

            <div className="flex gap-2">
              <input
                type="number"
                value={movimiento.cantidad}
                onChange={(e) => setMovimiento({ ...movimiento, cantidad: parseInt(e.target.value) || 0 })}
                className="flex-1 border border-gray-300 rounded-lg px-4 py-3 text-lg"
                placeholder="Cantidad"
                min="1"
              />
              <button
                onClick={handleMovimientoRapido}
                disabled={movimiento.cantidad <= 0}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <Check className="w-5 h-5" />
                Confirmar
              </button>
            </div>
          </div>

          {/* Acciones Disponibles */}
          {result.acciones_disponibles && (
            <div className="border-t pt-4 mt-4">
              <h3 className="text-sm font-semibold text-gray-600 mb-2">Otras Acciones</h3>
              <div className="grid grid-cols-2 gap-2">
                {result.acciones_disponibles.map((accion) => (
                  <button
                    key={accion.id}
                    className={`py-2 px-3 rounded-lg text-sm font-medium bg-${accion.color}-50 text-${accion.color}-600 hover:bg-${accion.color}-100`}
                  >
                    {accion.label}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Resultado de Ubicación */}
      {result && result.tipo === 'ubicacion' && (
        <div className="bg-white rounded-lg shadow-md p-6 animate-fade-in">
          <div className="flex justify-between items-start mb-4">
            <div className="flex items-center gap-2">
              <MapPin className="w-8 h-8 text-purple-600" />
              <div>
                <h2 className="text-2xl font-bold text-gray-800">Ubicación {result.data.ubicacion}</h2>
                <p className="text-gray-500">{result.data.total_productos} productos</p>
              </div>
            </div>
            <button
              onClick={() => setResult(null)}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          <div className="space-y-2">
            {result.data.productos.map((prod: any) => (
              <div key={prod.codigo} className="bg-gray-50 rounded-lg p-3 flex justify-between items-center">
                <div>
                  <p className="font-semibold">{prod.nombre}</p>
                  <p className="text-sm text-gray-500">{prod.codigo}</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-blue-600">{prod.stock}</p>
                  <p className="text-xs text-gray-500">unidades</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Botón de Historial */}
      <button className="fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 transition">
        <History className="w-6 h-6" />
      </button>
    </div>
  );
};

export default ScannerComponent;
