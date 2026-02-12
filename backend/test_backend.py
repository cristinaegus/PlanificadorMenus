"""
Script para verificar que el backend local está funcionando
"""
import requests

print("=" * 60)
print("VERIFICANDO BACKEND EN LOCALHOST:8000")
print("=" * 60)

try:
    # Probar endpoint de health
    print("\n🔍 Probando endpoint /health...")
    response = requests.get("http://localhost:8000/health", timeout=5)
    
    if response.status_code == 200:
        print("✅ Backend funcionando correctamente!")
        print(f"Respuesta: {response.json()}")
    else:
        print(f"⚠️ Respuesta inesperada: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ ERROR: No se pudo conectar al backend en localhost:8000")
    print("   El servidor no está corriendo o no está disponible en ese puerto.")
except requests.exceptions.Timeout:
    print("❌ ERROR: Timeout al intentar conectar con el backend")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")

print("\n" + "=" * 60)

# Probar endpoint raíz
try:
    print("\n🔍 Probando endpoint raíz /...")
    response = requests.get("http://localhost:8000/", timeout=5)
    
    if response.status_code == 200:
        print("✅ Endpoint raíz funcionando!")
        data = response.json()
        print(f"Mensaje: {data.get('message', '')}")
        print(f"Versión: {data.get('version', '')}")
        print("\nEndpoints disponibles:")
        for endpoint, desc in data.get('endpoints', {}).items():
            print(f"  - {endpoint}: {desc}")
    else:
        print(f"⚠️ Respuesta inesperada: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ No se pudo conectar al endpoint raíz")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")

print("\n" + "=" * 60)
