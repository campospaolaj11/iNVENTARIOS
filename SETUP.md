# 🚀 Guía de Instalación y Configuración

## Prerrequisitos

- **Python 3.11+** instalado
- **Node.js 18+** y npm
- **SQL Server** (Express, Developer o Enterprise)
- **Git** (opcional)

---

## 📦 1. Configurar Base de Datos (SQL Server)

### Paso 1: Crear la base de datos
```sql
-- Abrir SQL Server Management Studio (SSMS)
-- Conectarse a tu instancia de SQL Server
-- Ejecutar el script:
```

Ejecutar el archivo: `database/schema.sql`

Esto creará:
- Base de datos `InventariosDB`
- Tablas: `productos`, `movimientos`, `kpis`
- Vistas y stored procedures
- Datos de ejemplo

### Paso 2: Verificar la conexión
Anotar:
- **Servidor**: `localhost` o tu servidor SQL
- **Usuario**: generalmente `sa` o tu usuario
- **Contraseña**: tu contraseña de SQL Server

---

## 🐍 2. Configurar Backend (Python + FastAPI)

### Paso 1: Crear entorno virtual
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
```

### Paso 2: Instalar dependencias
```powershell
pip install -r requirements.txt
```

### Paso 3: Configurar variables de entorno
```powershell
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env con tus credenciales de SQL Server
notepad .env
```

Modificar en `.env`:
```
DATABASE_SERVER=localhost
DATABASE_NAME=InventariosDB
DATABASE_USER=sa
DATABASE_PASSWORD=tu_password_aqui
```

### Paso 4: Probar la API
```powershell
python main.py
```

Abrir: http://localhost:8000/docs

---

## ⚛️ 3. Configurar Frontend (React + TypeScript)

### Paso 1: Instalar dependencias
```powershell
cd ..\frontend
npm install
```

### Paso 2: Configurar variables de entorno
```powershell
copy .env.example .env
```

### Paso 3: Ejecutar desarrollo
```powershell
npm run dev
```

Abrir: http://localhost:5173

---

## 🤖 4. Automatización Excel (Python Scripts)

### Paso 1: Instalar dependencias
```powershell
cd ..\excel-automation
pip install -r requirements.txt
```

### Paso 2: Crear template de Excel
```powershell
python excel_templates.py
```

Esto genera: `template_inventario.xlsx`

### Paso 3: Importar datos desde Excel
```powershell
python excel_to_db.py
```

---

## 🎯 Verificación Completa

### 1. Backend funcionando
```
http://localhost:8000/health
```
Debería retornar: `{"status": "healthy"}`

### 2. Frontend funcionando
```
http://localhost:5173
```
Debería mostrar el dashboard con KPIs

### 3. Base de datos
Verificar en SSMS:
```sql
USE InventariosDB;
SELECT * FROM productos;
```

---

## 📝 Comandos Rápidos

### Iniciar todo el proyecto:

**Terminal 1 - Backend:**
```powershell
cd backend
venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

---

## 🔧 Solución de Problemas

### Error de conexión SQL Server
- Verificar que SQL Server esté corriendo
- Verificar credenciales en `.env`
- Verificar que el puerto 1433 esté abierto
- Instalar: `ODBC Driver 17 for SQL Server`

### Error en Python
```powershell
# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

### Error en npm
```powershell
# Limpiar caché
npm cache clean --force
rm -rf node_modules
npm install
```

---

## 📚 Próximos Pasos

1. ✅ Conectar API con SQL Server (endpoints CRUD)
2. ✅ Integrar frontend con API real
3. ✅ Automatización programada de Excel
4. ✅ Deploy en Netlify/Vercel

---

**¿Listo para empezar? Ejecuta los comandos de instalación! 🚀**
