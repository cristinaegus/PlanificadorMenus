"""
Script de prueba para el generador de PDFs de dietas
Ejecuta este script para probar la funcionalidad de generación de PDFs
"""

import os
import sys

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def probar_generador():
    """Función para probar el generador de PDFs"""
    try:
        # Importar el generador
        from dieta_pdf_generator import DietaPDFGenerator
        
        print("=== PRUEBA DEL GENERADOR DE PDFs DE DIETAS ===")
        print("Inicializando generador...")
        
        generator = DietaPDFGenerator()
        print("✓ Generador inicializado correctamente")
        print("✓ Archivo JSON cargado correctamente")
        
        # Mostrar información de los modelos cargados
        modelos = generator.modelos_dieta.get('modelos_dieta', {})
        print(f"✓ Se cargaron {len(modelos)} modelos de dieta")
        
        for modelo_key in modelos.keys():
            print(f"  - {modelo_key.replace('_', ' ').title()}")
        
        print("\n=== GENERANDO PDFs DE PRUEBA ===")
        
        # Generar PDF completo
        print("1. Generando PDF con todos los modelos...")
        try:
            archivo_completo = generator.generar_pdf_todos_los_modelos("test_modelos_completos.pdf")
            if os.path.exists(archivo_completo):
                print(f"✓ PDF completo generado: {os.path.basename(archivo_completo)}")
            else:
                print("❌ Error: PDF completo no se generó")
        except Exception as e:
            print(f"❌ Error generando PDF completo: {e}")
        
        # Generar resumen
        print("2. Generando resumen...")
        try:
            archivo_resumen = generator.generar_tabla_resumen()
            if os.path.exists(archivo_resumen):
                print(f"✓ Resumen generado: {os.path.basename(archivo_resumen)}")
            else:
                print("❌ Error: Resumen no se generó")
        except Exception as e:
            print(f"❌ Error generando resumen: {e}")
        
        # Generar PDF individual para modelo 1
        print("3. Generando PDF para modelo 1...")
        try:
            archivo_modelo1 = generator.generar_pdf_modelo_individual(1, "test_modelo_1.pdf")
            if os.path.exists(archivo_modelo1):
                print(f"✓ Modelo 1 generado: {os.path.basename(archivo_modelo1)}")
            else:
                print("❌ Error: Modelo 1 no se generó")
        except Exception as e:
            print(f"❌ Error generando modelo 1: {e}")
        
        print("\n=== PRUEBA COMPLETADA ===")
        print("Si todos los archivos se generaron correctamente, el sistema está funcionando.")
        print("Los archivos PDF se encuentran en el directorio backend/")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("Asegúrate de haber instalado reportlab: pip install reportlab")
    except FileNotFoundError as e:
        print(f"❌ Archivo no encontrado: {e}")
        print("Asegúrate de que el archivo modelos_dieta.json existe")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def mostrar_instrucciones():
    """Muestra instrucciones para el usuario"""
    print("=== INSTRUCCIONES DE INSTALACIÓN ===")
    print("1. Activar el entorno virtual:")
    print("   .venv\\Scripts\\Activate.ps1  # Windows PowerShell")
    print("   source .venv/bin/activate     # Linux/Mac")
    print()
    print("2. Instalar las nuevas dependencias:")
    print("   pip install -r requirements.txt")
    print()
    print("3. Ejecutar este script de prueba:")
    print("   python test_dieta_pdf.py")
    print()
    print("4. Iniciar el servidor FastAPI:")
    print("   python app.py")
    print()
    print("=== ENDPOINTS DISPONIBLES ===")
    print("• GET /dieta-modelos/generar-pdf-completo")
    print("• GET /dieta-modelos/generar-pdf-modelo/{1,2,3,4}")
    print("• GET /dieta-modelos/generar-resumen")
    print("• GET /dieta-modelos/info")
    print()

if __name__ == "__main__":
    mostrar_instrucciones()
    
    respuesta = input("¿Deseas ejecutar la prueba ahora? (y/N): ").lower()
    if respuesta in ['y', 'yes', 'sí', 'si']:
        probar_generador()
    else:
        print("Prueba cancelada. Ejecuta 'python test_dieta_pdf.py' cuando estés listo.")