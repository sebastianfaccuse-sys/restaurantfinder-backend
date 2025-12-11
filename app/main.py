from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

# Crear aplicación FastAPI
app = FastAPI(
    title="RestaurantFinder API",
    description="API para buscar restaurantes y obtener reseñas",
    version="1.0.0"
)

# Configurar CORS (permite que el frontend se conecte)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambiar por la URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(router, prefix="/api")

# Ruta raíz
@app.get("/")
async def root():
    return {
        "message": "RestaurantFinder API",
        "docs": "/docs",
        "health": "/api/health"
    }