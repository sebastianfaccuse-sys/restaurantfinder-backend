from fastapi import APIRouter, Query
from outscraper import ApiClient
from typing import Optional
from app.config import CONFIG

router = APIRouter()

# Cliente de Outscraper
cliente = ApiClient(api_key=CONFIG["OUTSCRAPER_API_KEY"])


def buscar_restaurantes(ubicacion: str, limite: int, idioma: str) -> list:
    """
    Busca todos los restaurantes en una ubicación.
    
    Returns:
        Lista de restaurantes encontrados
    """
    try:
        query = f"Restaurantes, {ubicacion}"
        
        results = cliente.google_maps_search(
            [query],
            limit=limite,
            language=idioma
        )
        
        if not results or not results[0]:
            return []
        
        return results[0]
    except Exception as e:
        print(f"Error en búsqueda: {e}")
        return []


def formatear_restaurante(r: dict) -> dict:
    """
    Formatea un restaurante para la respuesta.
    """
    return {
        "place_id": r.get("place_id"),
        "nombre": r.get("name"),
        "direccion": r.get("full_address"),
        "rating": r.get("rating") or 0,
        "total_reseñas": r.get("reviews") or 0,
        "rango_precio": r.get("range"),
        "tipo": r.get("type"),
        "telefono": r.get("phone"),
        "sitio_web": r.get("site"),
        "horario": r.get("working_hours"),
        "location_link": r.get("location_link"),
        "foto": r.get("photo")
    }


def ordenar_restaurantes(restaurantes: list) -> list:
    """
    Ordena restaurantes por rating (desc) y luego por reseñas (desc) para desempate.
    """
    return sorted(
        restaurantes,
        key=lambda x: (x.get("rating") or 0, x.get("total_reseñas") or 0),
        reverse=True
    )


def extraer_ciudad(ubicacion: str) -> Optional[str]:
    """
    Intenta extraer la ciudad de una ubicación.
    Ej: "Usaquén, Bogotá, Colombia" -> "Bogotá, Colombia"
    """
    partes = [p.strip() for p in ubicacion.split(",")]
    if len(partes) >= 2:
        return ", ".join(partes[1:])
    return None


@router.get("/search")
async def search(
    ubicacion: str = Query(..., description="Ubicación (ciudad, barrio, etc.)"),
    idioma: str = Query(CONFIG["DEFAULT_IDIOMA"], description="Idioma")
):
    """
    Busca todos los restaurantes en una ubicación.
    El filtrado por tipo y reseñas mínimas se hace en el frontend.
    """
    # Buscar restaurantes (límite amplio para tener suficientes datos)
    limite_busqueda = 100
    resultados = buscar_restaurantes(ubicacion, limite_busqueda, idioma)
    
    # Formatear restaurantes
    restaurantes = [formatear_restaurante(r) for r in resultados]
    
    # Ordenar por rating y reseñas (desempate)
    restaurantes = ordenar_restaurantes(restaurantes)
    
    # Verificar si hay pocos resultados y ampliar búsqueda
    busqueda_ampliada = False
    mensaje_ampliacion = None
    
    if len(restaurantes) < CONFIG["MIN_RESULTADOS_ANTES_AMPLIAR"]:
        ciudad = extraer_ciudad(ubicacion)
        
        if ciudad and ciudad.lower() != ubicacion.lower():
            resultados_ciudad = buscar_restaurantes(ciudad, limite_busqueda, idioma)
            restaurantes_ciudad = [formatear_restaurante(r) for r in resultados_ciudad]
            
            # Obtener IDs existentes para no duplicar
            place_ids_existentes = {r["place_id"] for r in restaurantes}
            nuevos = [r for r in restaurantes_ciudad if r["place_id"] not in place_ids_existentes]
            
            if nuevos:
                busqueda_ampliada = True
                mensaje_ampliacion = f"Encontramos {len(restaurantes)} en tu zona y {len(nuevos)} más en {ciudad}"
                restaurantes.extend(nuevos)
                restaurantes = ordenar_restaurantes(restaurantes)
    
    # Extraer tipos únicos para el frontend (para mostrar solo filtros relevantes)
    tipos_encontrados = list(set(r["tipo"] for r in restaurantes if r["tipo"]))
    tipos_encontrados.sort()
    
    return {
        "success": True,
        "ubicacion": ubicacion,
        "busqueda_ampliada": busqueda_ampliada,
        "mensaje_ampliacion": mensaje_ampliacion,
        "total": len(restaurantes),
        "tipos_encontrados": tipos_encontrados,
        "restaurantes": restaurantes
    }


@router.get("/restaurant/{place_id}/reviews")
async def get_reviews(
    place_id: str,
    limite: int = Query(CONFIG["DEFAULT_LIMITE_RESEÑAS"], ge=1, le=CONFIG["MAX_RESEÑAS"]),
    idioma: str = Query(CONFIG["DEFAULT_IDIOMA"])
):
    """
    Obtiene las reseñas de un restaurante específico.
    """
    try:
        results = cliente.google_maps_reviews(
            [place_id],
            reviews_limit=limite,
            sort="newest",
            language=idioma
        )
        
        if not results or not results[0]:
            return {
                "success": False,
                "error": "No se encontraron reseñas"
            }
        
        data = results[0]
        
        # Formatear reseñas
        reseñas = []
        for r in data.get("reviews_data", []):
            reseñas.append({
                "review_id": r.get("review_id"),
                "autor": r.get("author_title"),
                "autor_foto": r.get("author_image"),
                "rating": r.get("review_rating"),
                "fecha": r.get("review_datetime_utc"),
                "fecha_relativa": r.get("review_date"),
                "texto": r.get("review_text"),
                "likes": r.get("review_likes", 0),
                "respuesta_dueño": r.get("owner_answer"),
                "respuesta_dueño_fecha": r.get("owner_answer_timestamp_datetime_utc")
            })
        
        return {
            "success": True,
            "place_id": place_id,
            "restaurante": {
                "nombre": data.get("name"),
                "rating": data.get("rating"),
                "total_reseñas": data.get("reviews")
            },
            "reseñas": reseñas
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/config")
async def get_config():
    """
    Retorna la configuración para el frontend.
    """
    return {
        "success": True,
        "tipos_comida": [
            {"label": t["label"], "value": t["value"], "googleTypes": t["googleTypes"]}
            for t in CONFIG["TIPOS_COMIDA"]
        ],
        "reseñas_minimas_opciones": [
            {"value": 0, "label": "No aplica"},
            {"value": 50, "label": "+50 reseñas"},
            {"value": 100, "label": "+100 reseñas"},
            {"value": 500, "label": "+500 reseñas"},
            {"value": 1000, "label": "+1000 reseñas"},
            {"value": 5000, "label": "+5000 reseñas"}
        ],
        "limite_default": CONFIG["DEFAULT_LIMITE_RESULTADOS"]
    }


@router.get("/health")
async def health():
    """
    Verifica que el servidor esté funcionando.
    """
    return {
        "status": "ok",
        "api_key_configured": bool(CONFIG["OUTSCRAPER_API_KEY"])
    }