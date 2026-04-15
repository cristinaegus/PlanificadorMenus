#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Planificador Semanal Simplificado - Dietas 2
Versión sin dependencias externas (pandas, openpyxl)
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any

class PlanificadorSemanalSimple:
    def __init__(self, json_file: str = 'dietas_2.json'):
        """Inicializar el planificador con el archivo JSON de dietas"""
        self.json_file = json_file
        self.dietas_data = self.cargar_dietas()
        self.dias_semana = [
            'Lunes', 'Martes', 'Miércoles', 'Jueves', 
            'Viernes', 'Sábado', 'Domingo'
        ]
        
    def cargar_dietas(self) -> Dict[str, Any]:
        """Cargar datos del archivo JSON"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data['dietas_2']
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.json_file}")
            return {}
        except json.JSONDecodeError:
            print(f"Error: El archivo {self.json_file} no tiene formato JSON válido")
            return {}
    
    def obtener_opciones_desayuno(self) -> List[Dict]:
        """Extraer opciones de desayuno"""
        opciones = []
        for opcion in self.dietas_data['desayunos']['opciones']:
            for key, value in opcion.items():
                opciones.append({
                    'tipo': key.replace('_', ' ').title(),
                    'alimentos': value['alimentos']
                })
        return opciones
    
    def obtener_opciones_snacks(self) -> List[Dict]:
        """Extraer opciones de snacks/merienda"""
        opciones = []
        for opcion in self.dietas_data['snacks_media_manana_merienda']['opciones']:
            for key, value in opcion.items():
                opciones.append({
                    'tipo': key.replace('_', ' ').title(),
                    'alimentos': value['alimentos']
                })
        return opciones
    
    def obtener_opciones_comidas(self) -> List[Dict]:
        """Extraer opciones de comidas"""
        opciones = []
        complementos = self.dietas_data['comidas']['complementos_fijos']
        
        for plato in self.dietas_data['comidas']['opciones']:
            opciones.append({
                'plato_principal': plato.get('plato', ''),
                'detalles': plato.get('cantidad_total', ''),
                'complementos': complementos
            })
        return opciones
    
    def obtener_opciones_cenas(self) -> List[Dict]:
        """Extraer opciones de cenas"""
        opciones = []
        complementos = self.dietas_data['cenas']['complementos_fijos']
        
        for plato in self.dietas_data['cenas']['opciones']:
            opciones.append({
                'plato_principal': plato.get('plato', ''),
                'detalles': plato.get('detalles', {}),
                'complementos': complementos
            })
        return opciones
    
    def formatear_alimentos(self, alimentos: List[Dict]) -> str:
        """Formatear lista de alimentos para mostrar"""
        texto_alimentos = []
        for alimento in alimentos:
            nombre = alimento.get('nombre', '')
            cantidad = alimento.get('cantidad', '')
            unidades = alimento.get('unidades', '')
            opciones = alimento.get('opciones', [])
            
            if opciones:
                # Manejar opciones que pueden ser strings o diccionarios
                opciones_texto = []
                for opcion in opciones:
                    if isinstance(opcion, str):
                        opciones_texto.append(opcion)
                    elif isinstance(opcion, dict):
                        tipo = opcion.get('tipo', '')
                        cant_opcion = opcion.get('cantidad', '')
                        if cant_opcion:
                            opciones_texto.append(f"{tipo} ({cant_opcion})")
                        else:
                            opciones_texto.append(tipo)
                    else:
                        opciones_texto.append(str(opcion))
                
                if cantidad:
                    texto_alimentos.append(f"  • {nombre} ({cantidad}) - Opciones: {', '.join(opciones_texto)}")
                else:
                    texto_alimentos.append(f"  • {nombre} - Opciones: {', '.join(opciones_texto)}")
            elif unidades:
                texto_alimentos.append(f"  • {nombre}: {cantidad} ({unidades})")
            elif cantidad:
                texto_alimentos.append(f"  • {nombre}: {cantidad}")
            else:
                texto_alimentos.append(f"  • {nombre}")
                
        return '\n'.join(texto_alimentos)
    
    def formatear_complementos(self, complementos: List[Dict]) -> str:
        """Formatear complementos fijos"""
        texto_complementos = []
        for complemento in complementos:
            nombre = complemento.get('nombre', '')
            cantidad = complemento.get('cantidad', '')
            if cantidad:
                texto_complementos.append(f"  • {nombre}: {cantidad}")
            else:
                texto_complementos.append(f"  • {nombre}")
        return '\n'.join(texto_complementos)
    
    def generar_menu_semanal(self, modo: str = 'aleatorio') -> List[Dict]:
        """
        Generar menú semanal
        
        Args:
            modo: 'aleatorio' para selección aleatoria, 'secuencial' para rotar opciones
        """
        opciones_desayuno = self.obtener_opciones_desayuno()
        opciones_snacks = self.obtener_opciones_snacks()
        opciones_comidas = self.obtener_opciones_comidas()
        opciones_cenas = self.obtener_opciones_cenas()
        
        menu_semanal = []
        
        for i, dia in enumerate(self.dias_semana):
            if modo == 'aleatorio':
                desayuno = random.choice(opciones_desayuno)
                snack = random.choice(opciones_snacks)
                comida = random.choice(opciones_comidas)
                cena = random.choice(opciones_cenas)
            else:  # secuencial
                desayuno = opciones_desayuno[i % len(opciones_desayuno)]
                snack = opciones_snacks[i % len(opciones_snacks)]
                comida = opciones_comidas[i % len(opciones_comidas)]
                cena = opciones_cenas[i % len(opciones_cenas)]
            
            menu_semanal.append({
                'dia': dia,
                'desayuno': desayuno,
                'snack': snack,
                'comida': comida,
                'cena': cena
            })
        
        return menu_semanal
    
    def imprimir_menu_semanal(self, menu_semanal: List[Dict]):
        """Imprimir menú semanal en consola con formato mejorado"""
        print("\n" + "="*80)
        print("🍽️  PLANIFICADOR SEMANAL - DIETAS 2")
        print("="*80)
        
        # Imprimir requisitos diarios
        requisitos = self.dietas_data.get('requisitos_diarios', {})
        print("📋 REQUISITOS DIARIOS:")
        for key, value in requisitos.items():
            nombre = key.replace('_', ' ').title()
            print(f"  • {nombre}: {value}")
        print("="*80 + "\n")
        
        for menu_dia in menu_semanal:
            dia = menu_dia['dia']
            desayuno = menu_dia['desayuno']
            snack = menu_dia['snack']
            comida = menu_dia['comida']
            cena = menu_dia['cena']
            
            print(f"📅 {dia.upper()}")
            print("-" * 50)
            
            # Desayuno
            print(f"🌅 DESAYUNO - {desayuno['tipo']}")
            print(self.formatear_alimentos(desayuno['alimentos']))
            print()
            
            # Snack/Merienda
            print(f"🥪 SNACK/MERIENDA - {snack['tipo']}")
            print(self.formatear_alimentos(snack['alimentos']))
            print()
            
            # Comida
            print(f"🍽️ COMIDA - {comida['plato_principal']}")
            if comida['detalles']:
                print(f"  📝 {comida['detalles']}")
            print("  Complementos:")
            print(self.formatear_complementos(comida['complementos']))
            print()
            
            # Cena
            print(f"🌙 CENA - {cena['plato_principal']}")
            if cena['detalles']:
                detalles_texto = []
                for key, value in cena['detalles'].items():
                    detalles_texto.append(f"{key}: {value}")
                if detalles_texto:
                    print(f"  📝 {', '.join(detalles_texto)}")
            print("  Complementos:")
            print(self.formatear_complementos(cena['complementos']))
            print()
            
            print("="*80 + "\n")
    
    def guardar_menu_txt(self, menu_semanal: List[Dict], filename: str = None) -> str:
        """Guardar menú en archivo de texto"""
        if filename is None:
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"menu_semanal_dietas2_{fecha_actual}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("PLANIFICADOR SEMANAL - DIETAS 2\n")
            f.write("="*80 + "\n\n")
            
            # Escribir requisitos diarios
            requisitos = self.dietas_data.get('requisitos_diarios', {})
            f.write("REQUISITOS DIARIOS:\n")
            for key, value in requisitos.items():
                nombre = key.replace('_', ' ').title()
                f.write(f"• {nombre}: {value}\n")
            f.write("\n" + "="*80 + "\n\n")
            
            for menu_dia in menu_semanal:
                dia = menu_dia['dia']
                desayuno = menu_dia['desayuno']
                snack = menu_dia['snack']
                comida = menu_dia['comida']
                cena = menu_dia['cena']
                
                f.write(f"{dia.upper()}\n")
                f.write("-" * 50 + "\n\n")
                
                # Desayuno
                f.write(f"DESAYUNO - {desayuno['tipo']}\n")
                f.write(self.formatear_alimentos(desayuno['alimentos']) + "\n\n")
                
                # Snack/Merienda
                f.write(f"SNACK/MERIENDA - {snack['tipo']}\n")
                f.write(self.formatear_alimentos(snack['alimentos']) + "\n\n")
                
                # Comida
                f.write(f"COMIDA - {comida['plato_principal']}\n")
                if comida['detalles']:
                    f.write(f"Detalles: {comida['detalles']}\n")
                f.write("Complementos:\n")
                f.write(self.formatear_complementos(comida['complementos']) + "\n\n")
                
                # Cena
                f.write(f"CENA - {cena['plato_principal']}\n")
                if cena['detalles']:
                    detalles_texto = []
                    for key, value in cena['detalles'].items():
                        detalles_texto.append(f"{key}: {value}")
                    if detalles_texto:
                        f.write(f"Detalles: {', '.join(detalles_texto)}\n")
                f.write("Complementos:\n")
                f.write(self.formatear_complementos(cena['complementos']) + "\n\n")
                
                f.write("="*80 + "\n\n")
        
        return filename
    
    def generar_menu_csv(self, menu_semanal: List[Dict], filename: str = None) -> str:
        """Generar archivo CSV simple del menú"""
        if filename is None:
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"menu_semanal_dietas2_{fecha_actual}.csv"
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Encabezados
            f.write("Día,Desayuno,Snack/Merienda,Comida,Cena\n")
            
            for menu_dia in menu_semanal:
                dia = menu_dia['dia']
                
                # Simplificar contenido para CSV
                desayuno_simple = f"{menu_dia['desayuno']['tipo']}: " + \
                    " + ".join([a.get('nombre', '') for a in menu_dia['desayuno']['alimentos']])
                
                snack_simple = f"{menu_dia['snack']['tipo']}: " + \
                    " + ".join([a.get('nombre', '') for a in menu_dia['snack']['alimentos']])
                
                comida_simple = menu_dia['comida']['plato_principal']
                
                cena_simple = menu_dia['cena']['plato_principal']
                
                # Escapar comillas para CSV
                f.write(f'"{dia}","{desayuno_simple}","{snack_simple}","{comida_simple}","{cena_simple}"\n')
        
        return filename

def main():
    """Función principal"""
    print("Iniciando Planificador Semanal Simplificado de Dietas 2...")
    
    # Crear instancia del planificador
    planificador = PlanificadorSemanalSimple()
    
    # Verificar que se cargaron los datos
    if not planificador.dietas_data:
        print("Error: No se pudieron cargar los datos de dietas.")
        return
    
    print(f"✅ Datos cargados correctamente de {planificador.json_file}")
    
    # Generar menú semanal aleatorio
    print("\n🎲 Generando menú semanal aleatorio...")
    menu_aleatorio = planificador.generar_menu_semanal(modo='aleatorio')
    
    # Mostrar menú en consola
    planificador.imprimir_menu_semanal(menu_aleatorio)
    
    # Guardar archivos
    archivo_txt = planificador.guardar_menu_txt(menu_aleatorio)
    archivo_csv = planificador.generar_menu_csv(menu_aleatorio)
    
    print(f"💾 Menú guardado en formato texto: {archivo_txt}")
    print(f"📊 Menú guardado en formato CSV: {archivo_csv}")
    
    # Opción para generar menú secuencial
    respuesta = input("\n¿Deseas generar también un menú secuencial? (s/n): ").lower()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        print("\n📋 Generando menú semanal secuencial...")
        menu_secuencial = planificador.generar_menu_semanal(modo='secuencial')
        
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M")
        archivo_txt_seq = planificador.guardar_menu_txt(
            menu_secuencial, 
            f"menu_semanal_dietas2_secuencial_{fecha_actual}.txt"
        )
        archivo_csv_seq = planificador.generar_menu_csv(
            menu_secuencial, 
            f"menu_semanal_dietas2_secuencial_{fecha_actual}.csv"
        )
        
        print(f"💾 Menú secuencial guardado en: {archivo_txt_seq}")
        print(f"📊 Menú secuencial guardado en: {archivo_csv_seq}")

if __name__ == "__main__":
    main()