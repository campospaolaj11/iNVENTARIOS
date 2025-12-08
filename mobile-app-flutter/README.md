# App Móvil Flutter - Scanner de Inventarios 📱

Aplicación móvil desarrollada en Flutter para escanear códigos QR/Barras del sistema de inventarios.

## 🚀 Características

- ✅ Scanner QR/Barras en tiempo real
- ✅ Detalle completo de productos
- ✅ Movimientos rápidos (entrada/salida)
- ✅ Historial de movimientos
- ✅ Entrada manual de códigos
- ✅ Detección de stock crítico
- ✅ Diseño Material Design 3
- ✅ Modo offline (próximamente)

## 📋 Prerequisitos

1. **Flutter SDK** (3.0.0 o superior)
   ```bash
   # Descargar de: https://flutter.dev/docs/get-started/install
   ```

2. **Android Studio** (para desarrollo Android)
   - Android SDK
   - Emulador Android

3. **Xcode** (solo macOS, para desarrollo iOS)

4. **Editor de código**: VS Code o Android Studio

## 🔧 Instalación

### 1. Verificar instalación de Flutter

```bash
flutter doctor
```

Asegúrate de que todos los checks estén en verde ✅

### 2. Crear proyecto (YA ESTÁ CREADO)

Los archivos ya están listos en `mobile-app-flutter/`

### 3. Instalar dependencias

```bash
cd mobile-app-flutter
flutter pub get
```

### 4. Configurar URL de tu API

Edita `lib/services/api_service.dart`:

```dart
static const String baseUrl = 'https://TU_API_URL/api';
// Cambia esto por la URL de tu backend desplegado
```

## 📱 Ejecutar la App

### En Emulador Android

```bash
# Listar emuladores disponibles
flutter emulators

# Iniciar emulador
flutter emulators --launch <emulator_id>

# Ejecutar app
flutter run
```

### En Dispositivo Físico Android

1. Habilita **Depuración USB** en tu teléfono Android
2. Conecta el teléfono a tu PC con USB
3. Ejecuta:

```bash
flutter devices  # Verificar que se detecta
flutter run
```

### En iOS (solo macOS)

```bash
# Abrir simulador iOS
open -a Simulator

# Ejecutar app
flutter run
```

## 🔨 Compilar APK (Android)

### APK para desarrollo (debug)

```bash
flutter build apk --debug
```

### APK para producción (release)

```bash
flutter build apk --release
```

El APK se generará en: `build/app/outputs/flutter-apk/app-release.apk`

### AAB para Google Play Store

```bash
flutter build appbundle --release
```

## 📦 Estructura del Proyecto

```
mobile-app-flutter/
├── lib/
│   ├── main.dart                  # Entry point
│   ├── models/                    # Modelos de datos
│   │   ├── producto.dart
│   │   ├── movimiento.dart
│   │   └── scan_result.dart
│   ├── screens/                   # Pantallas
│   │   ├── home_screen.dart       # Pantalla principal
│   │   ├── scanner_screen.dart    # Scanner QR
│   │   ├── product_detail_screen.dart
│   │   ├── movement_screen.dart
│   │   └── history_screen.dart
│   ├── services/                  # Servicios
│   │   └── api_service.dart       # Comunicación con API
│   └── providers/                 # Estado global
│       └── inventory_provider.dart
├── android/                       # Configuración Android
├── ios/                          # Configuración iOS
└── pubspec.yaml                  # Dependencias
```

## 🎨 Dependencias Principales

- **mobile_scanner**: Scanner QR/Barras nativo
- **provider**: Gestión de estado
- **http**: Cliente HTTP
- **shared_preferences**: Almacenamiento local
- **intl**: Formateo de fechas

## 🔑 Permisos Configurados

### Android
- ✅ `CAMERA` - Acceso a cámara
- ✅ `INTERNET` - Conexión a internet
- ✅ `ACCESS_NETWORK_STATE` - Estado de red

### iOS
- ✅ `NSCameraUsageDescription` - Acceso a cámara
- ✅ `NSPhotoLibraryUsageDescription` - Acceso a fotos

## 🧪 Probar sin Backend

La app incluye datos de prueba. Puedes usarla sin conexión al backend para:

1. Ver UI y navegación
2. Probar scanner (simulado)
3. Validar flujos de trabajo

## 🚀 Desplegar

### Google Play Store

1. Genera keystore:
   ```bash
   keytool -genkey -v -keystore ~/upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
   ```

2. Configura `android/key.properties`

3. Build AAB:
   ```bash
   flutter build appbundle --release
   ```

4. Sube a Google Play Console

### Apple App Store

1. Configura certificados en Xcode
2. Build para iOS:
   ```bash
   flutter build ios --release
   ```

3. Sube con Xcode a App Store Connect

## 📸 Screenshots

_(Agrega capturas de pantalla aquí)_

## 🐛 Troubleshooting

### Error: "Gradle sync failed"

```bash
cd android
./gradlew clean
cd ..
flutter pub get
```

### Error: "Camera permission denied"

- Verifica que los permisos estén en AndroidManifest.xml
- En iOS, verifica Info.plist

### Error: "API connection failed"

- Verifica la URL en `api_service.dart`
- Asegúrate que el backend esté corriendo
- Verifica que el emulador tenga internet

## 📞 Soporte

Para más ayuda:
- [Documentación Flutter](https://flutter.dev/docs)
- [Flutter DevTools](https://flutter.dev/docs/development/tools/devtools)

## 🎯 Próximas Funcionalidades

- [ ] Modo offline con SQLite
- [ ] Sincronización automática
- [ ] Notificaciones push
- [ ] Firma digital en movimientos
- [ ] Exportar reportes PDF
- [ ] Múltiples idiomas
- [ ] Dark mode

---

**Desarrollado con** ❤️ **usando Flutter**
