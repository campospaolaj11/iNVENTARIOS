# 🚀 Guía de Deploy a Netlify + Railway

## Arquitectura de Deploy

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Netlify   │────────▶│   Railway    │────────▶│ SQL Server  │
│  (Frontend) │         │  (Backend)   │         │  (Database) │
└─────────────┘         └──────────────┘         └─────────────┘
     React                   FastAPI                 Azure/Local
```

---

## 📦 1. Deploy Backend en Railway

Railway es ideal para hostear el backend Python con SQL Server.

### Paso 1: Crear cuenta en Railway
1. Ir a: https://railway.app/
2. Crear cuenta con GitHub
3. Verificar email

### Paso 2: Crear nuevo proyecto
```bash
# Instalar Railway CLI (opcional)
npm install -g @railway/cli
railway login
```

### Paso 3: Deploy desde GitHub
1. En Railway: "New Project" → "Deploy from GitHub repo"
2. Seleccionar tu repositorio
3. Railway detectará automáticamente Python
4. Configurar variables de entorno:

```
DATABASE_SERVER=tu-sql-server.database.windows.net
DATABASE_NAME=InventariosDB
DATABASE_USER=admin
DATABASE_PASSWORD=tu_password
DATABASE_DRIVER=ODBC Driver 17 for SQL Server
SECRET_KEY=tu-clave-secreta-super-segura
DEBUG=False
CORS_ORIGINS=https://tu-app.netlify.app
```

### Paso 4: Configurar Base de Datos SQL Server

**Opción A: Azure SQL Database (Recomendado para producción)**
1. Crear cuenta en Azure
2. Crear SQL Database
3. Configurar firewall para permitir Railway IPs
4. Obtener connection string

**Opción B: SQL Server en Railway**
```bash
# Agregar servicio de PostgreSQL como alternativa
# Railway no soporta SQL Server nativamente
# Considera migrar a PostgreSQL para producción
```

**Opción C: SQL Server Local (Solo desarrollo)**
- Usar ngrok para exponer SQL Server local

### Paso 5: Obtener URL del backend
Después del deploy, Railway te dará una URL como:
```
https://inventarios-api-production.up.railway.app
```

---

## 🌐 2. Deploy Frontend en Netlify

### Paso 1: Preparar el proyecto
```powershell
cd frontend

# Crear archivo .env para producción
echo "VITE_API_URL=https://tu-backend.railway.app" > .env.production

# Probar build local
npm run build
```

### Paso 2: Deploy manual (método rápido)

**Opción A: Drag & Drop**
1. Ejecutar: `npm run build`
2. Ir a: https://app.netlify.com/drop
3. Arrastrar la carpeta `frontend/dist`
4. ¡Listo! Tu sitio estará en línea

**Opción B: Netlify CLI**
```powershell
# Instalar Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy desde carpeta raíz del proyecto
cd ..
netlify deploy --prod
```

### Paso 3: Deploy automático desde GitHub

1. Push tu código a GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tu-usuario/inventarios.git
git push -u origin main
```

2. En Netlify:
   - "Add new site" → "Import from Git"
   - Conectar GitHub
   - Seleccionar repositorio
   
3. Configuración de build:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`

4. Variables de entorno en Netlify:
   ```
   VITE_API_URL=https://tu-backend.railway.app
   ```

---

## 🎯 3. Configuración para usar Mock Data (Opcional)

Si no tienes backend listo, el frontend funcionará con datos locales:

### En Netlify:
1. No configurar `VITE_API_URL`
2. O agregar: `VITE_USE_MOCK=true`
3. El frontend usará `public/mock-data.json`

---

## ✅ 4. Verificación

### Backend (Railway):
```bash
curl https://tu-backend.railway.app/health
# Debe retornar: {"status": "healthy"}
```

### Frontend (Netlify):
1. Abrir: https://tu-app.netlify.app
2. Verificar que se muestren los KPIs
3. Revisar consola del navegador (F12)

---

## 🔒 5. Configuración de SQL Server en Azure (Producción)

### Crear Azure SQL Database:
```bash
# Instalar Azure CLI
az login

# Crear grupo de recursos
az group create --name InventariosRG --location eastus

# Crear servidor SQL
az sql server create \
  --name inventarios-sql-server \
  --resource-group InventariosRG \
  --location eastus \
  --admin-user sqladmin \
  --admin-password TuPasswordSeguro123!

# Crear base de datos
az sql db create \
  --resource-group InventariosRG \
  --server inventarios-sql-server \
  --name InventariosDB \
  --service-objective S0

# Configurar firewall (permitir Railway)
az sql server firewall-rule create \
  --resource-group InventariosRG \
  --server inventarios-sql-server \
  --name AllowRailway \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 255.255.255.255
```

### Connection String para Railway:
```
SERVER=inventarios-sql-server.database.windows.net
DATABASE_NAME=InventariosDB
DATABASE_USER=sqladmin
DATABASE_PASSWORD=TuPasswordSeguro123!
```

---

## 📝 Resumen de URLs

| Servicio | URL | Propósito |
|----------|-----|-----------|
| Frontend | https://inventarios.netlify.app | Dashboard web |
| Backend | https://inventarios-api.railway.app | API REST |
| API Docs | https://inventarios-api.railway.app/docs | Documentación Swagger |
| Database | Azure SQL Server | Almacenamiento de datos |

---

## 🐛 Troubleshooting

### Error de CORS
Verificar en `backend/config.py`:
```python
CORS_ORIGINS=https://tu-app.netlify.app
```

### Backend no conecta con SQL Server
1. Verificar firewall de Azure
2. Verificar credenciales en Railway
3. Revisar logs: `railway logs`

### Frontend no carga datos
1. Verificar URL del backend en `.env.production`
2. Revisar consola del navegador (F12)
3. Verificar que `/mock-data.json` exista

---

## 🎉 ¡Listo para Producción!

Ahora tu sistema está desplegado y accesible desde cualquier lugar:
- ✅ Frontend en Netlify (CDN global)
- ✅ Backend en Railway (auto-scaling)
- ✅ Base de datos SQL Server en Azure
- ✅ HTTPS automático en ambos servicios
