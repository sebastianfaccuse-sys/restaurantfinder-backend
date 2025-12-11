# RestaurantFinder API

API para buscar restaurantes y obtener reseñas desde Google Maps.

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/search?ubicacion=...` | Busca restaurantes en una ubicación |
| GET | `/api/restaurant/{place_id}/reviews` | Obtiene reseñas de un restaurante |
| GET | `/api/config` | Retorna configuración para el frontend |
| GET | `/api/health` | Verifica estado del servidor |

## Ejecutar localmente
```bash
# Activar entorno virtual
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn app.main:app --reload
```

## Variables de entorno

Crear archivo `config.env`:
```
OUTSCRAPER_API_KEY=tu_api_key
```