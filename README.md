# 📦 Sistema de Inventarios Automatizado

Sistema completo de gestión de inventarios con automatización Excel, API REST y Dashboard Web interactivo.

## 🏗️ Arquitectura

```
Excel (CSV/Datos) → Python Scripts → SQL Server → API FastAPI → Dashboard React
```

## 📁 Estructura del Proyecto

```
inventarios/
├── backend/              # API REST con FastAPI (Python)
├── frontend/             # Dashboard web con React + TypeScript
├── excel-automation/     # Scripts Python para automatización Excel
├── database/            # Schemas y scripts SQL Server
└── README.md
```

## 🚀 Stack Tecnológico

### Backend
- **Python 3.11+** con FastAPI
- **SQL Server** (pyodbc/sqlalchemy)
- **Pydantic** para validación de datos

### Frontend
- **React 18** con TypeScript
- **Vite** como bundler
- **Chart.js / Recharts** para visualización
- **Tailwind CSS** para estilos
- **Axios** para peticiones HTTP

### Automatización
- **pandas** - Procesamiento de datos
- **openpyxl** - Lectura/escritura Excel
- **schedule** - Tareas programadas

## 📊 KPIs Principales

| KPI | Descripción |
|-----|-------------|
| Stock Crítico | Nivel mínimo antes de ruptura de inventario |
| Rotación | Velocidad de salida de productos |
| Costos de Almacén | Costo por mantener stock en bodega |
| Pedidos Sugeridos | Productos que deben reabastecerse |

## 🔧 Instalación

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Editar .env con credenciales SQL Server
python main.py
```

### Frontend
```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

### Excel Automation
```bash
cd excel-automation
pip install -r requirements.txt
python excel_templates.py
```

## 🚀 Deploy en Producción

Este proyecto está preparado para desplegarse en:
- **Frontend**: Netlify (gratis, con CDN global)
- **Backend**: Railway (gratis hasta 500 horas/mes)
- **Database**: Azure SQL Database o SQL Server local

### Deploy Rápido a Netlify

```bash
# Desde la carpeta raíz
cd frontend
npm run build

# Arrastrar carpeta 'dist' a: https://app.netlify.com/drop
```

### Deploy Backend a Railway

```bash
# Push a GitHub y conectar con Railway
git push origin main

# O usar Railway CLI
railway up
```

📖 **Ver guía completa en `DEPLOY.md`**

## 🌐 URLs de Producción

- **Demo Frontend**: [Tu URL de Netlify]
- **API Backend**: [Tu URL de Railway]
- **API Docs**: [Tu URL de Railway]/docs

## ✨ Características para Deploy

- ✅ Frontend funciona **sin backend** usando mock data
- ✅ Configuración automática de Netlify con `netlify.toml`
- ✅ Backend listo para Railway/Render con `Procfile`
- ✅ CORS configurado para producción
- ✅ Variables de entorno separadas por ambiente
- ✅ Build optimizado para producción


## 🗄️ Base de Datos

Configurar SQL Server:
1. Crear base de datos `InventariosDB`
2. Ejecutar scripts en `database/schema.sql`
3. Configurar conexión en `backend/.env`

## 📝 Variables de Entorno

Crear archivo `.env` en `/backend`:
```
DATABASE_SERVER=localhost
DATABASE_NAME=InventariosDB
DATABASE_USER=tu_usuario
DATABASE_PASSWORD=tu_password
SECRET_KEY=tu_clave_secreta
```

## 🎯 Roadmap

- [x] Estructura base del proyecto
- [ ] API REST con endpoints CRUD
- [ ] Conexión SQL Server
- [ ] Scripts automatización Excel
- [ ] Dashboard React con gráficas
- [ ] Deploy en Netlify/Vercel

## 👨‍💻 Desarrollo

**Backend**: `http://localhost:8000`  
**Frontend**: `http://localhost:5173`  
**API Docs**: `http://localhost:8000/docs`

---

*Proyecto desarrollado como demostración de automatización industrial e integración de sistemas*
