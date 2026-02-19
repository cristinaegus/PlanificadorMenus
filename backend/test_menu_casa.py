"""
Script para probar el endpoint de menú casa
"""
import requests

print("=" * 60)
print("PROBANDO ENDPOINT /generar-menu-casa")
print("=" * 60)

try:
    print("\n🔄 Generando PDF del menú de casa...")
    
    response = requests.post(
        "http://localhost:8000/generar-menu-casa",
        json={
            "id_cristina": 1,
            "id_marisa": 1
        },
        timeout=30
    )
    
    if response.status_code == 200:
        # Guardar el PDF
        with open("menu_casa_test.pdf", "wb") as f:
            f.write(response.content)
        
        print("✅ PDF generado y guardado como 'menu_casa_test.pdf'")
        print(f"   Tamaño: {len(response.content)} bytes")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   Respuesta: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ No se pudo conectar al backend en localhost:8000")
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "=" * 60)
