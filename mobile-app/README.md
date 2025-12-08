# Scanner Móvil con QR/Barras - React Native

Esta carpeta contendrá la aplicación móvil para escanear códigos QR/barras.

## 📱 Crear App Móvil

### Opción 1: React Native con Expo (Recomendado - Más rápido)

```bash
# Instalar Expo CLI globalmente
npm install -g expo-cli

# Crear proyecto
npx create-expo-app@latest InventarioScannerApp --template blank-typescript

# Entrar al proyecto
cd InventarioScannerApp

# Instalar dependencias para scanner
npx expo install expo-camera expo-barcode-scanner expo-image-picker

# Instalar axios para API calls
npm install axios

# Ejecutar
npx expo start
```

### Opción 2: React Native CLI (Más control)

```bash
# Instalar React Native CLI
npm install -g react-native-cli

# Crear proyecto
npx react-native init InventarioScanner --template react-native-template-typescript

cd InventarioScanner

# Instalar dependencias
npm install react-native-vision-camera
npm install react-native-screens react-navigation
npm install axios
```

## 🚀 Pasos Siguientes

1. **Ejecutar el comando de creación** (Opción 1 recomendada)
2. **Escanear QR** con tu móvil usando la app Expo Go
3. **Desarrollar componentes**:
   - ScannerScreen (pantalla principal)
   - ProductDetailScreen (detalles del producto)
   - MovimientoRapidoScreen (agregar/quitar stock)
   - HistorialScreen (ver movimientos)

## 📋 Código Base del Scanner (Expo)

```typescript
// App.tsx
import React, { useState, useEffect } from 'react';
import { Text, View, StyleSheet, Button } from 'react-native';
import { BarCodeScanner } from 'expo-barcode-scanner';

export default function App() {
  const [hasPermission, setHasPermission] = useState(null);
  const [scanned, setScanned] = useState(false);

  useEffect(() => {
    (async () => {
      const { status } = await BarCodeScanner.requestPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const handleBarCodeScanned = async ({ type, data }) => {
    setScanned(true);
    
    // Llamar a la API
    try {
      const response = await fetch('YOUR_API_URL/api/scanner/escanear?codigo=' + data);
      const resultado = await response.json();
      
      alert(`Producto encontrado: ${resultado.data.nombre}`);
    } catch (error) {
      alert('Error al buscar producto');
    }
    
    setScanned(false);
  };

  if (hasPermission === null) {
    return <Text>Solicitando permiso de cámara...</Text>;
  }
  if (hasPermission === false) {
    return <Text>No hay acceso a la cámara</Text>;
  }

  return (
    <View style={styles.container}>
      <BarCodeScanner
        onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
        style={StyleSheet.absoluteFillObject}
      />
      {scanned && <Button title={'Escanear de nuevo'} onPress={() => setScanned(false)} />}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
  },
});
```

## 🎯 Funcionalidades a Implementar

- [x] Escaneo de QR/Barras
- [ ] Búsqueda de productos
- [ ] Registro de movimientos rápidos
- [ ] Inventario físico (conteo)
- [ ] Historial de movimientos
- [ ] Modo offline (SQLite local)
- [ ] Sincronización con servidor

## 📸 Probar sin app móvil

Puedes probar la funcionalidad usando:
- **Webcam** en tu computadora
- **Simulador de móvil** en VS Code
- **Chrome DevTools** con emulación de dispositivo móvil
