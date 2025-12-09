from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Importar routers
from routes.scanner import router as scanner_router
from routes.notificaciones import router as notificaciones_router

# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Inventarios API",
    description="API REST para gestión de inventarios automatizado",
    version="1.0.0"
)

# Configurar CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear directorio para QR codes
os.makedirs("static/qr_codes", exist_ok=True)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Registrar routers
app.include_router(scanner_router)
app.include_router(notificaciones_router)

@app.get("/")
async def root():
    return {
        "message": "Sistema de Inventarios API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "pending"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("DEBUG", "True") == "True"
    )
