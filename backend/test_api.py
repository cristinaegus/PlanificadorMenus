"""
Script de prueba para verificar la conexión con Spoonacular API
"""
import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
SPOONACULAR_BASE_URL = "https://api.spoonacular.com"

print("=" * 60)
print("PRUEBA DE SPOONACULAR API")
print("=" * 60)
print(f"API Key: {SPOONACULAR_API_KEY}")
print(f"Base URL: {SPOONACULAR_BASE_URL}")
print()

# Prueba 1: Búsqueda simple
print("🧪 PRUEBA 1: Búsqueda simple de recetas")
print("-" * 60)

params = {
    "apiKey": SPOONACULAR_API_KEY,
    "number": 5,
    "cuisine": "mediterranean",
    "type": "main course",
}

try:
    response = requests.get(
        f"{SPOONACULAR_BASE_URL}/recipes/complexSearch",
        params=params,
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"URL solicitada: {response.url}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Respuesta exitosa!")
        print(f"Total resultados: {data.get('totalResults', 0)}")
        print(f"Recetas recibidas: {len(data.get('results', []))}")
        print()
        
        if data.get("results"):
            print("📋 Recetas encontradas:")
            for i, recipe in enumerate(data["results"], 1):
                print(f"  {i}. {recipe.get('title')} (ID: {recipe.get('id')})")
        else:
            print("⚠️ No se encontraron recetas")
    else:
        print(f"❌ Error en la respuesta: {response.status_code}")
        print(f"Respuesta: {response.text}")
        
except Exception as e:
    print(f"❌ Error durante la petición: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
print("FIN DE LA PRUEBA")
print("=" * 60)
