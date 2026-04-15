#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Planificador Semanal de Dietas 2
Genera un menú semanal combinando las opciones del archivo dietas_2.json
"""

import json
import random
from typing import Dict, List, Any
import pandas as pd
from datetime import datetime, timedelta

class PlanificadorSemanalDietas2:
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
                    texto_alimentos.append(f"• {nombre} ({cantidad}) - Opciones: {', '.join(opciones_texto)}")
                else:
                    texto_alimentos.append(f"• {nombre} - Opciones: {', '.join(opciones_texto)}")
            elif unidades:
                texto_alimentos.append(f"• {nombre}: {cantidad} ({unidades})")
            elif cantidad:
                texto_alimentos.append(f"• {nombre}: {cantidad}")
            else:
                texto_alimentos.append(f"• {nombre}")
                
        return '\n'.join(texto_alimentos)
    
    def formatear_complementos(self, complementos: List[Dict]) -> str:
        """Formatear complementos fijos"""
        texto_complementos = []
        for complemento in complementos:
            nombre = complemento.get('nombre', '')
            cantidad = complemento.get('cantidad', '')
            if cantidad:
                texto_complementos.append(f"• {nombre}: {cantidad}")
            else:
                texto_complementos.append(f"• {nombre}")
        return '\n'.join(texto_complementos)
    
    def generar_menu_semanal(self, modo: str = 'aleatorio') -> pd.DataFrame:
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
            
            # Formatear desayuno
            desayuno_texto = f"**{desayuno['tipo']}**\n{self.formatear_alimentos(desayuno['alimentos'])}"
            
            # Formatear snack
            snack_texto = f"**{snack['tipo']}**\n{self.formatear_alimentos(snack['alimentos'])}"
            
            # Formatear comida
            comida_texto = f"**{comida['plato_principal']}**"
            if comida['detalles']:
                comida_texto += f"\n📝 {comida['detalles']}"
            comida_texto += f"\n\n**Complementos:**\n{self.formatear_complementos(comida['complementos'])}"
            
            # Formatear cena
            cena_texto = f"**{cena['plato_principal']}**"
            if cena['detalles']:
                detalles_texto = []
                for key, value in cena['detalles'].items():
                    detalles_texto.append(f"{key}: {value}")
                if detalles_texto:
                    cena_texto += f"\n📝 {', '.join(detalles_texto)}"
            cena_texto += f"\n\n**Complementos:**\n{self.formatear_complementos(cena['complementos'])}"
            
            menu_semanal.append({
                'Día': dia,
                'Desayuno': desayuno_texto,
                'Snack/Merienda': snack_texto,
                'Comida': comida_texto,
                'Cena': cena_texto
            })
        
        return pd.DataFrame(menu_semanal)
    
    def generar_resumen_requisitos(self) -> str:
        """Generar resumen de requisitos diarios"""
        requisitos = self.dietas_data.get('requisitos_diarios', {})
        texto = "## 📋 REQUISITOS DIARIOS\n"
        for key, value in requisitos.items():
            nombre = key.replace('_', ' ').title()
            texto += f"• **{nombre}**: {value}\n"
        return texto
    
    def guardar_menu_excel(self, df: pd.DataFrame, filename: str = None) -> str:
        """Guardar menú en archivo Excel"""
        if filename is None:
            fecha_actual = datetime.now().strftime("%Y%m%d")
            filename = f"menu_semanal_dietas2_{fecha_actual}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Menú Semanal', index=False)
            
            # Ajustar ancho de columnas
            worksheet = writer.sheets['Menú Semanal']
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
        
        return filename
    
    def imprimir_menu_semanal(self, df: pd.DataFrame):
        """Imprimir menú semanal en consola con formato mejorado"""
        print("\n" + "="*80)
        print("🍽️  PLANIFICADOR SEMANAL - DIETAS 2")
        print("="*80)
        print(self.generar_resumen_requisitos())
        print("="*80 + "\n")
        
        for _, fila in df.iterrows():
            print(f"📅 **{fila['Día'].upper()}**")
            print("-" * 50)
            print(f"🌅 **DESAYUNO:**\n{fila['Desayuno']}\n")
            print(f"🥪 **SNACK/MERIENDA:**\n{fila['Snack/Merienda']}\n")
            print(f"🍽️ **COMIDA:**\n{fila['Comida']}\n")
            print(f"🌙 **CENA:**\n{fila['Cena']}\n")
            print("="*80 + "\n")

def main():
    """Función principal"""
    print("Iniciando Planificador Semanal de Dietas 2...")
    
    # Crear instancia del planificador
    planificador = PlanificadorSemanalDietas2()
    
    # Verificar que se cargaron los datos
    if not planificador.dietas_data:
        print("Error: No se pudieron cargar los datos de dietas.")
        return
    
    # Generar menú semanal aleatorio
    print("\n🎲 Generando menú semanal aleatorio...")
    menu_aleatorio = planificador.generar_menu_semanal(modo='aleatorio')
    
    # Mostrar menú en consola
    planificador.imprimir_menu_semanal(menu_aleatorio)
    
    # Guardar en Excel
    filename_excel = planificador.guardar_menu_excel(menu_aleatorio)
    print(f"📊 Menú guardado en: {filename_excel}")
    
    # Opción para generar menú secuencial
    respuesta = input("\n¿Deseas generar también un menú secuencial? (s/n): ")
    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        print("\n📋 Generando menú semanal secuencial...")
        menu_secuencial = planificador.generar_menu_semanal(modo='secuencial')
        filename_secuencial = planificador.guardar_menu_excel(
            menu_secuencial, 
            f"menu_semanal_dietas2_secuencial_{datetime.now().strftime('%Y%m%d')}.xlsx"
        )
        print(f"📊 Menú secuencial guardado en: {filename_secuencial}")

if __name__ == "__main__":
    main()