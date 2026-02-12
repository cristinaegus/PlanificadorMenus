import os
import requests
from dotenv import load_dotenv
import random

# Cargar variables de entorno
load_dotenv()

# API Key de Spoonacular
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
SPOONACULAR_BASE_URL = "https://api.spoonacular.com"

# Banco de recetas locales para cuando la API no esté disponible
RECETAS_LOCALES = {
    "mediterranean": {
        "lunch": [
            "Ensalada Griega con Queso Feta",
            "Pasta con Tomate y Albahaca",
            "Pescado al Horno con Limón",
            "Arroz con Verduras Mediterráneas",
            "Pollo a la Plancha con Hierbas",
            "Berenjena a la Parmesana",
            "Lentejas con Verduras",
            "Salmón a la Parrilla con Espárragos",
            "Risotto de Champiñones",
            "Pimientos Rellenos de Arroz"
        ],
        "dinner": [
            "Sopa de Verduras",
            "Tortilla de Patatas",
            "Crema de Calabacín",
            "Lubina al Vapor con Verduras",
            "Pechuga de Pavo con Ensalada",
            "Gazpacho Andaluz",
            "Merluza a la Plancha",
            "Revuelto de Setas",
            "Calabacín Relleno",
            "Sepia a la Plancha"
        ]
    },
    "italian": {
        "lunch": [
            "Lasaña Boloñesa",
            "Risotto alla Milanese",
            "Pizza Margherita",
            "Pasta Carbonara",
            "Pollo Parmesano",
            "Gnocchi al Pesto",
            "Ossobuco con Risotto",
            "Penne Arrabbiata",
            "Saltimbocca alla Romana",
            "Pasta Primavera"
        ],
        "dinner": [
            "Minestrone",
            "Carpaccio de Ternera",
            "Caprese de Tomate y Mozzarella",
            "Bruschetta Italiana",
            "Calamares a la Romana",
            "Panzanella",
            "Frittata de Verduras",
            "Sopa de Tomate",
            "Vitello Tonnato",
            "Arancini de Arroz"
        ]
    },
    "asian": {
        "lunch": [
            "Arroz Tres Delicias",
            "Pollo Teriyaki",
            "Pad Thai de Verduras",
            "Sushi Variado",
            "Fideos Yakisoba",
            "Curry Rojo Tailandés",
            "Arroz Frito con Gambas",
            "Pollo con Almendras",
            "Wok de Verduras",
            "Tempura de Gambas"
        ],
        "dinner": [
            "Sopa Miso",
            "Rollitos Primavera",
            "Edamame al Vapor",
            "Ensalada Asiática",
            "Gyozas al Vapor",
            "Sopa de Wonton",
            "Tataki de Atún",
            "Sashimi Variado",
            "Seaweed Salad",
            "Dim Sum Variado"
        ]
    },
    "mexican": {
        "lunch": [
            "Tacos de Pollo",
            "Enchiladas de Queso",
            "Quesadillas de Verduras",
            "Burrito Bowl",
            "Fajitas de Ternera",
            "Chiles Rellenos",
            "Arroz Mexicano con Frijoles",
            "Tostadas de Pollo",
            "Chimichangas",
            "Nachos Supremos"
        ],
        "dinner": [
            "Guacamole con Nachos",
            "Sopa de Tortilla",
            "Ceviche Mexicano",
            "Elote Asado",
            "Ensalada de Nopales",
            "Pozole Verde",
            "Sopa de Frijoles",
            "Aguacate Relleno",
            "Pico de Gallo",
            "Queso Fundido"
        ]
    },
    "spanish": {
        "lunch": [
            "Paella Valenciana",
            "Fabada Asturiana",
            "Cocido Madrileño",
            "Pollo al Chilindrón",
            "Bacalao al Pil Pil",
            "Arroz a Banda",
            "Caldereta de Cordero",
            "Marmitako de Bonito",
            "Fideuá",
            "Rabo de Toro"
        ],
        "dinner": [
            "Croquetas Caseras",
            "Patatas Bravas",
            "Tortilla Española",
            "Pimientos de Padrón",
            "Pulpo a la Gallega",
            "Gambas al Ajillo",
            "Jamón Ibérico con Pan",
            "Ensaladilla Rusa",
            "Boquerones en Vinagre",
            "Queso Manchego con Membrillo"
        ]
    },
    "recetas casa": {
        "lunch": [
            "Estofado de Ternera Casero",
            "Macarrones con Tomate",
            "Pollo Asado con Patatas",
            "Albóndigas en Salsa",
            "Guiso de Lentejas",
            "Arroz con Pollo",
            "Pescado Rebozado con Ensalada",
            "Canelones de Carne",
            "Costillas al Horno",
            "Codillo con Verduras"
        ],
        "dinner": [
            "Sopa de Fideos",
            "Tortilla Francesa",
            "Puré de Verduras",
            "Empanadillas Caseras",
            "Crema de Zanahoria",
            "Caldo de Pollo",
            "Revuelto de Huevos",
            "San Jacobo Casero",
            "Salchichas con Patatas",
            "Flamenquines"
        ]
    }
}

def generar_menu_semanal(preferencias: str = "", restricciones: str = "", tipo_cocina: str = "mediterránea"):
    """
    Genera un menú semanal usando Spoonacular API
    
    Args:
        preferencias: Preferencias alimentarias del usuario
        restricciones: Restricciones dietéticas (vegetariano, sin gluten, etc.)
        tipo_cocina: Tipo de cocina (mediterránea, asiática, etc.)
    
    Returns:
        dict: Menú semanal con comida y cena para cada día
    """
    
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    menu_semanal = {}
    
    # Mapear tipo de cocina a cuisine de Spoonacular
    cuisine_map = {
        "mediterránea": "mediterranean",
        "asiática": "asian",
        "mexicana": "mexican",
        "italiana": "italian",
        "española": "spanish",
        "vegetariana": "vegetarian",
        "saludable": "healthy"
    }
    
    cuisine = cuisine_map.get(tipo_cocina.lower(), "mediterranean")
    
    # Mapear restricciones a diets de Spoonacular
    diet = ""
    if "vegetariano" in restricciones.lower():
        diet = "vegetarian"
    elif "vegano" in restricciones.lower():
        diet = "vegan"
    elif "sin gluten" in restricciones.lower() or "gluten free" in restricciones.lower():
        diet = "gluten free"
    
    try:
        # Lista para almacenar IDs de recetas ya usadas y evitar repetición
        used_recipe_ids = []
        
        for dia in dias:
            # Buscar receta para comida (asegurando que sea diferente)
            lunch_recipe, lunch_id = buscar_receta(cuisine, diet, "lunch", preferencias, used_recipe_ids)
            used_recipe_ids.append(lunch_id)
            
            # Buscar receta para cena (asegurando que sea diferente)
            dinner_recipe, dinner_id = buscar_receta(cuisine, diet, "dinner", preferencias, used_recipe_ids)
            used_recipe_ids.append(dinner_id)
            
            menu_semanal[dia] = {
                "lunch": lunch_recipe,
                "dinner": dinner_recipe
            }
        
        return menu_semanal
        
    except Exception as e:
        print(f"Error al generar menú: {e}")
        return None


def buscar_receta(cuisine: str, diet: str, meal_type: str, query: str = "", exclude_ids: list = None):
    """
    Busca una receta aleatoria en Spoonacular o banco local asegurando variedad
    
    Args:
        cuisine: Tipo de cocina
        diet: Restricción dietética
        meal_type: Tipo de comida (lunch/dinner)
        query: Búsqueda adicional
        exclude_ids: Lista de IDs de recetas a excluir para evitar repetición
    
    Returns:
        tuple: (nombre de la receta, ID de la receta)
    """
    
    if exclude_ids is None:
        exclude_ids = []
    
    # Intentar primero usar recetas locales si la API tiene problemas
    meal_key = "lunch" if meal_type == "lunch" else "dinner"
    
    if cuisine in RECETAS_LOCALES and meal_key in RECETAS_LOCALES[cuisine]:
        recetas_disponibles = RECETAS_LOCALES[cuisine][meal_key].copy()
        
        # Mezclar para más variedad
        random.shuffle(recetas_disponibles)
        
        # Buscar una receta que no esté en exclude_ids (usando índice como ID)
        for idx, receta in enumerate(recetas_disponibles):
            recipe_id = hash(receta) % 10000  # Generar un ID único basado en el nombre
            if recipe_id not in exclude_ids:
                print(f"✨ Receta local seleccionada: {receta}")
                return (receta, recipe_id)
        
        # Si todas están usadas, usar la primera
        if recetas_disponibles:
            receta = recetas_disponibles[0]
            recipe_id = hash(receta) % 10000
            print(f"⚠️ Reutilizando receta local: {receta}")
            return (receta, recipe_id)
    
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "number": 10,  # Pedimos más recetas para tener variedad
        "cuisine": cuisine,
        "type": meal_type if meal_type != "lunch" else "main course",
        "addRecipeInformation": False,
        "sort": "random",  # Ordenar aleatoriamente
    }
    
    if diet:
        params["diet"] = diet
    
    if query:
        params["query"] = query
    
    try:
        print(f"🔍 Buscando receta: cuisine={cuisine}, meal={meal_type}, diet={diet}")
        print(f"📡 API URL: {SPOONACULAR_BASE_URL}/recipes/complexSearch")
        print(f"🔑 API Key presente: {'Sí' if SPOONACULAR_API_KEY else 'No'}")
        
        response = requests.get(
            f"{SPOONACULAR_BASE_URL}/recipes/complexSearch",
            params=params,
            timeout=10
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Resultados recibidos: {len(data.get('results', []))} recetas")
            
            if data.get("results") and len(data["results"]) > 0:
                # Filtrar recetas que no estén en la lista de excluidas
                available_recipes = [r for r in data["results"] if r["id"] not in exclude_ids]
                print(f"🎲 Recetas disponibles después de filtrar: {len(available_recipes)}")
                
                if available_recipes:
                    # Seleccionar una receta aleatoria de las disponibles
                    selected_recipe = random.choice(available_recipes)
                    print(f"✨ Receta seleccionada: {selected_recipe['title']}")
                    return (selected_recipe["title"], selected_recipe["id"])
                elif data["results"]:
                    # Si todas están excluidas, usar la primera disponible
                    selected_recipe = data["results"][0]
                    print(f"⚠️ Todas excluidas, usando: {selected_recipe['title']}")
                    return (selected_recipe["title"], selected_recipe["id"])
            
            # Si no hay resultados, buscar sin restricciones específicas
            print("⚠️ Sin resultados, intentando búsqueda simplificada...")
            params_simple = {
                "apiKey": SPOONACULAR_API_KEY,
                "number": 10,
                "type": "main course",
                "sort": "random",
            }
            response_simple = requests.get(
                f"{SPOONACULAR_BASE_URL}/recipes/complexSearch",
                params=params_simple,
                timeout=10
            )
            if response_simple.status_code == 200:
                data_simple = response_simple.json()
                if data_simple.get("results") and len(data_simple["results"]) > 0:
                    available_recipes = [r for r in data_simple["results"] if r["id"] not in exclude_ids]
                    if available_recipes:
                        selected_recipe = random.choice(available_recipes)
                        print(f"✨ Receta simplificada: {selected_recipe['title']}")
                        return (selected_recipe["title"], selected_recipe["id"])
        else:
            print(f"❌ Error API: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
        
        print(f"⚠️ Retornando receta genérica")
        return (f"Receta {cuisine.capitalize()}", random.randint(1000, 9999))
        
    except Exception as e:
        print(f"❌ Error al buscar receta: {e}")
        import traceback
        traceback.print_exc()
        return (f"Plato {cuisine.capitalize()}", random.randint(1000, 9999))


def generar_sugerencia_comida(dia: str, tipo_comida: str = "comida", estilo: str = "mediterráneo"):
    """
    Genera una sugerencia para una comida específica usando Spoonacular
    
    Args:
        dia: Día de la semana
        tipo_comida: 'comida' o 'cena'
        estilo: Estilo de cocina
    
    Returns:
        str: Sugerencia de plato
    """
    
    cuisine_map = {
        "mediterráneo": "mediterranean",
        "asiático": "asian",
        "mexicano": "mexican",
        "italiano": "italian",
        "español": "spanish"
    }
    
    cuisine = cuisine_map.get(estilo.lower(), "mediterranean")
    meal_type = "dinner" if tipo_comida.lower() == "cena" else "main course"
    
    try:
        params = {
            "apiKey": SPOONACULAR_API_KEY,
            "number": 5,  # Pedir múltiples opciones
            "cuisine": cuisine,
            "type": meal_type,
            "sort": "random",
        }
        
        response = requests.get(
            f"{SPOONACULAR_BASE_URL}/recipes/complexSearch",
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("results") and len(data["results"]) > 0:
                # Seleccionar una receta aleatoria
                selected = random.choice(data["results"])
                return selected["title"]
        
        return f"Plato {estilo.capitalize()} para {tipo_comida}"
        
    except Exception as e:
        print(f"Error al generar sugerencia: {e}")
        return None
