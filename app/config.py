import os
from dotenv import load_dotenv

# Cargar variables desde config.env
load_dotenv('config.env')

CONFIG = {
    # API Key de Outscraper
    "OUTSCRAPER_API_KEY": os.getenv("OUTSCRAPER_API_KEY"),
    
    # Límites por defecto
    "DEFAULT_LIMITE_RESULTADOS": 10,
    "DEFAULT_LIMITE_RESEÑAS": 10,
    "DEFAULT_IDIOMA": "es",
    
    # Límites máximos permitidos
    "MAX_RESULTADOS": 20,
    "MAX_RESEÑAS": 50,
    
    # Mínimo de resultados antes de ampliar búsqueda
    "MIN_RESULTADOS_ANTES_AMPLIAR": 5,
    
    # Opciones de reseñas mínimas permitidas
    "RESEÑAS_MINIMAS_OPCIONES": [0, 50, 100, 500, 1000, 5000],
    
    # Tipos de comida con mapeo a Google Maps
    "TIPOS_COMIDA": [
        # Opción general
        {"label": "Todos", "value": "todos", "googleTypes": ["Restaurante"]},
        
        # Por país/región
        {"label": "Americana", "value": "americana", "googleTypes": ["Restaurante americano"]},
        {"label": "Argentina", "value": "argentina", "googleTypes": ["Restaurante argentino"]},
        {"label": "Asiática", "value": "asiatica", "googleTypes": ["Restaurante asiático", "Restaurante de cocina panasiática"]},
        {"label": "Brasileña", "value": "brasilena", "googleTypes": ["Restaurante brasileño"]},
        {"label": "Chilena", "value": "chilena", "googleTypes": ["Restaurante chileno"]},
        {"label": "China", "value": "china", "googleTypes": ["Restaurante chino", "Restaurante cantonés"]},
        {"label": "Colombiana", "value": "colombiana", "googleTypes": ["Restaurante colombiano"]},
        {"label": "Coreana", "value": "coreana", "googleTypes": ["Restaurante coreano"]},
        {"label": "Cubana", "value": "cubana", "googleTypes": ["Restaurante cubano"]},
        {"label": "Española", "value": "espanola", "googleTypes": ["Restaurante de cocina española", "Restaurante andaluz", "Restaurante asturiano", "Restaurante gallego", "Restaurante vasco", "Restaurante de comida madrileña"]},
        {"label": "Francesa", "value": "francesa", "googleTypes": ["Restaurante francés"]},
        {"label": "Griega", "value": "griega", "googleTypes": ["Restaurante griego"]},
        {"label": "India", "value": "india", "googleTypes": ["Restaurante indio"]},
        {"label": "Italiana", "value": "italiana", "googleTypes": ["Restaurante italiano"]},
        {"label": "Japonesa", "value": "japonesa", "googleTypes": ["Restaurante japonés", "Restaurante japonés auténtico", "Restaurante de sushi", "Restaurante especializado en ramen"]},
        {"label": "Latina", "value": "latina", "googleTypes": ["Restaurante latinoamericano", "Restaurante de cocina criolla"]},
        {"label": "Libanesa/Árabe", "value": "libanesa", "googleTypes": ["Restaurante libanés", "Restaurante marroquí"]},
        {"label": "Mediterránea", "value": "mediterranea", "googleTypes": ["Restaurante mediterráneo"]},
        {"label": "Mexicana", "value": "mexicana", "googleTypes": ["Restaurante mexicano", "Taquería", "Restaurante tex-mex"]},
        {"label": "Peruana", "value": "peruana", "googleTypes": ["Restaurante peruano"]},
        {"label": "Tailandesa", "value": "tailandesa", "googleTypes": ["Restaurante tailandés"]},
        {"label": "Turca", "value": "turca", "googleTypes": ["Restaurante turco", "Restaurante turcomano"]},
        {"label": "Venezolana", "value": "venezolana", "googleTypes": ["Restaurante venezolano"]},
        {"label": "Vietnamita", "value": "vietnamita", "googleTypes": ["Restaurante vietnamita"]},
        
        # Por especialidad
        {"label": "Carnes/Parrilla", "value": "carnes", "googleTypes": ["Parrilla", "Brasería", "Restaurante especializado en filetes", "Restaurante especializado en barbacoa"]},
        {"label": "Hamburguesas", "value": "hamburguesas", "googleTypes": ["Hamburguesería"]},
        {"label": "Mariscos", "value": "mariscos", "googleTypes": ["Marisquería"]},
        {"label": "Pizza", "value": "pizza", "googleTypes": ["Pizzería"]},
        {"label": "Pollo", "value": "pollo", "googleTypes": ["Pollería", "Restaurante especializado en pollo"]},
        {"label": "Sushi", "value": "sushi", "googleTypes": ["Restaurante de sushi"]},
        {"label": "Tapas", "value": "tapas", "googleTypes": ["Bar de tapas", "Restaurante especializado en tapas"]},
        
        # Por estilo/ocasión
        {"label": "Alta cocina", "value": "alta_cocina", "googleTypes": ["Restaurante de alta cocina"]},
        {"label": "Buffet", "value": "buffet", "googleTypes": ["Buffet libre"]},
        {"label": "Comida rápida", "value": "comida_rapida", "googleTypes": ["Restaurante de comida rápida"]},
        {"label": "Desayuno/Brunch", "value": "desayuno", "googleTypes": ["Restaurante de brunch", "Restaurante de desayunos"]},
        {"label": "Familiar", "value": "familiar", "googleTypes": ["Restaurante familiar"]},
        {"label": "Saludable", "value": "saludable", "googleTypes": ["Restaurante de comida saludable", "Tienda de ensaladas"]},
        {"label": "Vegana/Vegetariana", "value": "vegana", "googleTypes": ["Restaurante vegano", "Restaurante vegetariano"]},
        
        # Bares
        {"label": "Bar/Cervecería", "value": "bar", "googleTypes": ["Bar", "Bar restaurante", "Cervecería", "Cervecería artesanal", "Pub restaurante", "Taberna"]},
        {"label": "Coctelería", "value": "cocteleria", "googleTypes": ["Coctelería"]}
    ]
}


def get_google_types(tipo_value: str) -> list:
    """
    Obtiene los tipos de Google Maps para un valor de tipo de comida.
    
    Args:
        tipo_value: El value del tipo (ej: "italiana", "mexicana")
    
    Returns:
        Lista de tipos de Google Maps
    """
    for tipo in CONFIG["TIPOS_COMIDA"]:
        if tipo["value"] == tipo_value:
            return tipo["googleTypes"]
    return ["Restaurante"]  # Default