#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para el planificador semanal
"""

from planificador_semanal_simple import PlanificadorSemanalSimple
import os

def test_planificador():
    """Probar el planificador semanal"""
    print("🧪 Ejecutando pruebas del planificador semanal...")
    
    # Verificar que existe el archivo JSON
    json_file = 'dietas_2.json'
    if not os.path.exists(json_file):
        print(f"❌ Error: No se encuentra el archivo {json_file}")
        return False
    
    # Crear planificador
    try:
        planificador = PlanificadorSemanalSimple(json_file)
        print("✅ Planificador creado correctamente")
    except Exception as e:
        print(f"❌ Error al crear planificador: {e}")
        return False
    
    # Verificar carga de datos
    if not planificador.dietas_data:
        print("❌ Error: No se cargaron datos del JSON")
        return False
    print("✅ Datos JSON cargados correctamente")
    
    # Verificar opciones disponibles
    desayunos = planificador.obtener_opciones_desayuno()
    snacks = planificador.obtener_opciones_snacks()
    comidas = planificador.obtener_opciones_comidas()
    cenas = planificador.obtener_opciones_cenas()
    
    print(f"✅ {len(desayunos)} opciones de desayuno disponibles")
    print(f"✅ {len(snacks)} opciones de snacks disponibles")
    print(f"✅ {len(comidas)} opciones de comida disponibles")
    print(f"✅ {len(cenas)} opciones de cena disponibles")
    
    # Generar un menú de prueba
    try:
        menu_test = planificador.generar_menu_semanal(modo='secuencial')
        print(f"✅ Menú semanal generado: {len(menu_test)} días")
    except Exception as e:
        print(f"❌ Error al generar menú: {e}")
        return False
    
    # Verificar estructura del menú
    dia_ejemplo = menu_test[0]
    campos_requeridos = ['dia', 'desayuno', 'snack', 'comida', 'cena']
    for campo in campos_requeridos:
        if campo not in dia_ejemplo:
            print(f"❌ Error: Campo {campo} no encontrado en menú")
            return False
    print("✅ Estructura del menú validada")
    
    print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
    return True

if __name__ == "__main__":
    test_planificador()