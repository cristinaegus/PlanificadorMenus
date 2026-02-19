"""
Módulo para generar menús de casa para Cristina y Marisa
Lee los archivos JSON de menús y genera PDFs imprimibles
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, 
    Spacer, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def cargar_menus(archivo_json: str) -> Dict:
    """
    Carga los menús desde un archivo JSON
    
    Args:
        archivo_json: Ruta al archivo JSON con los menús
        
    Returns:
        Dict con los menús cargados
    """
    try:
        with open(archivo_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo: {archivo_json}")
        return {"menus": []}
    except json.JSONDecodeError:
        print(f"❌ Error al decodificar el JSON: {archivo_json}")
        return {"menus": []}


def listar_menus_disponibles(archivo_json: str) -> List[Dict]:
    """
    Lista todos los menús disponibles en un archivo JSON
    
    Args:
        archivo_json: Ruta al archivo JSON
        
    Returns:
        Lista de menús disponibles
    """
    datos = cargar_menus(archivo_json)
    menus = datos.get("menus", [])
    
    if not menus:
        print(f"No hay menús disponibles en {archivo_json}")
        return []
    
    print(f"\n📋 Menús disponibles en {archivo_json}:")
    print("=" * 60)
    for menu in menus:
        print(f"ID: {menu['id']} | {menu['nombre']} | {menu['tipo_cocina']}")
        print(f"   Fecha: {menu.get('fecha_creacion', 'N/A')}")
    print("=" * 60)
    
    return menus


def obtener_menu_por_id(archivo_json: str, menu_id: int) -> Optional[Dict]:
    """
    Obtiene un menú específico por su ID
    
    Args:
        archivo_json: Ruta al archivo JSON
        menu_id: ID del menú a obtener
        
    Returns:
        Dict con el menú o None si no se encuentra
    """
    datos = cargar_menus(archivo_json)
    menus = datos.get("menus", [])
    
    for menu in menus:
        if menu['id'] == menu_id:
            return menu
    
    print(f"❌ No se encontró el menú con ID {menu_id}")
    return None


def generar_pdf_menu_semanal(
    menu_cristina: Dict,
    menu_marisa: Dict,
    archivo_salida: str = "menu_semanal_casa.pdf"
):
    """
    Genera un PDF con los menús semanales de Cristina y Marisa
    Formato optimizado para impresión
    
    Args:
        menu_cristina: Diccionario con el menú de Cristina
        menu_marisa: Diccionario con el menú de Marisa
        archivo_salida: Nombre del archivo PDF de salida
    """
    doc = SimpleDocTemplate(
        archivo_salida,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Elementos del documento
    elementos = []
    
    # Título principal
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    titulo = Paragraph(f"🏠 MENÚ SEMANAL DE CASA", title_style)
    fecha = Paragraph(f"Semana del {fecha_actual}", subtitle_style)
    
    elementos.append(titulo)
    elementos.append(fecha)
    elementos.append(Spacer(1, 1*cm))
    
    # Función auxiliar para crear tabla de menú
    def crear_tabla_menu(menu: Dict, nombre_persona: str, color_header):
        datos = []
        
        # Encabezado de la persona
        datos.append([Paragraph(f"<b>{nombre_persona}</b>", styles['Heading2']), '', ''])
        datos.append([Paragraph(f"<i>{menu['nombre']}</i>", styles['Normal']), '', ''])
        datos.append(['', '', ''])
        
        # Encabezado de columnas
        datos.append([
            Paragraph('<b>DÍA</b>', styles['Normal']),
            Paragraph('<b>COMIDA</b>', styles['Normal']),
            Paragraph('<b>CENA</b>', styles['Normal'])
        ])
        
        # Días de la semana
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        semana = menu.get('semana', {})
        
        for dia in dias:
            dia_menu = semana.get(dia, {})
            lunch = dia_menu.get('lunch', 'No disponible')
            dinner = dia_menu.get('dinner', 'No disponible')
            
            datos.append([
                Paragraph(f'<b>{dia}</b>', styles['Normal']),
                Paragraph(lunch, styles['Normal']),
                Paragraph(dinner, styles['Normal'])
            ])
        
        # Crear tabla
        tabla = Table(datos, colWidths=[3.5*cm, 7*cm, 7*cm])
        
        # Estilo de la tabla
        tabla.setStyle(TableStyle([
            # Encabezado de persona
            ('SPAN', (0, 0), (2, 0)),
            ('BACKGROUND', (0, 0), (2, 0), color_header),
            ('TEXTCOLOR', (0, 0), (2, 0), colors.white),
            ('ALIGN', (0, 0), (2, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (2, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (2, 0), 14),
            ('BOTTOMPADDING', (0, 0), (2, 0), 12),
            
            # Nombre del menú
            ('SPAN', (0, 1), (2, 1)),
            ('ALIGN', (0, 1), (2, 1), 'CENTER'),
            ('FONTSIZE', (0, 1), (2, 1), 10),
            ('TEXTCOLOR', (0, 1), (2, 1), colors.grey),
            
            # Encabezado de columnas
            ('BACKGROUND', (0, 3), (2, 3), colors.HexColor('#ECF0F1')),
            ('TEXTCOLOR', (0, 3), (2, 3), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 3), (2, 3), 'CENTER'),
            ('FONTNAME', (0, 3), (2, 3), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 3), (2, 3), 10),
            ('BOTTOMPADDING', (0, 3), (2, 3), 8),
            
            # Contenido de la tabla
            ('BACKGROUND', (0, 4), (0, 10), colors.HexColor('#F8F9FA')),
            ('FONTNAME', (0, 4), (0, 10), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 4), (0, 10), 9),
            ('FONTSIZE', (1, 4), (2, 10), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 4), (0, 10), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 4), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 4), (-1, -1), 6),
            
            # Bordes
            ('GRID', (0, 3), (-1, -1), 1, colors.HexColor('#BDC3C7')),
            ('BOX', (0, 0), (-1, -1), 2, color_header),
            
            # Alternar colores de filas
            ('ROWBACKGROUNDS', (0, 4), (-1, -1), [colors.white, colors.HexColor('#FAFAFA')])
        ]))
        
        return tabla
    
    # Menú de Cristina
    color_cristina = colors.HexColor('#E74C3C')
    tabla_cristina = crear_tabla_menu(menu_cristina, "👩 CRISTINA", color_cristina)
    elementos.append(tabla_cristina)
    elementos.append(Spacer(1, 1*cm))
    
    # Salto de página
    elementos.append(PageBreak())
    
    # Repetir título en segunda página
    elementos.append(titulo)
    elementos.append(fecha)
    elementos.append(Spacer(1, 1*cm))
    
    # Menú de Marisa
    color_marisa = colors.HexColor('#3498DB')
    tabla_marisa = crear_tabla_menu(menu_marisa, "👩 MARISA", color_marisa)
    elementos.append(tabla_marisa)
    
    # Generar PDF
    doc.build(elementos)
    print(f"\n✅ PDF generado exitosamente: {archivo_salida}")
    return archivo_salida


def generar_menu_desde_cristina_menu1(archivo_salida: str = "menu_semanal_casa.pdf"):
    """
    Genera menú usando cristina_menu1.json (con Primeros y Segundos)
    y marisa_menus.json
    
    Args:
        archivo_salida: Nombre del archivo de salida
    """
    import random
    
    print("\n" + "="*60)
    print("🏠 GENERADOR DE MENÚ SEMANAL DE CASA")
    print("="*60)
    
    # Cargar cristina_menu1.json
    try:
        with open("cristina_menu1.json", 'r', encoding='utf-8') as f:
            cristina_recetas = json.load(f)
    except FileNotFoundError:
        print("❌ No se encontró cristina_menu1.json")
        return None
    
    primeros = cristina_recetas.get("Primeros", [])
    segundos = cristina_recetas.get("Segundos", [])
    
    if not primeros or not segundos:
        print("❌ El archivo cristina_menu1.json no tiene Primeros o Segundos")
        return None
    
    # Crear menú semanal para Cristina seleccionando aleatoriamente
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    semana_cristina = {}
    
    # Seleccionar recetas únicas para la semana
    primeros_semana = random.sample(primeros, min(7, len(primeros)))
    segundos_semana = random.sample(segundos, min(7, len(segundos)))
    
    for i, dia in enumerate(dias):
        semana_cristina[dia] = {
            "lunch": primeros_semana[i] if i < len(primeros_semana) else random.choice(primeros),
            "dinner": segundos_semana[i] if i < len(segundos_semana) else random.choice(segundos)
        }
    
    menu_cristina = {
        "id": 1,
        "nombre": "Menú Casa de Cristina",
        "fecha_creacion": datetime.now().strftime("%Y-%m-%d"),
        "tipo_cocina": "casa",
        "semana": semana_cristina
    }
    
    # Cargar menú de Marisa
    menu_marisa = obtener_menu_por_id("marisa_menus.json", 1)
    
    if not menu_marisa:
        print("\n❌ No se pudo cargar el menú de Marisa")
        return None
    
    print(f"\n📋 Menú generado para Cristina desde cristina_menu1.json")
    print(f"📋 Menú seleccionado para Marisa: {menu_marisa['nombre']}")
    
    # Generar PDF
    return generar_pdf_menu_semanal(menu_cristina, menu_marisa, archivo_salida)

def generar_menu_casa_automatico(
    id_cristina: int = 1,
    id_marisa: int = 1,
    archivo_salida: str = "menu_semanal_casa.pdf"
):
    """
    Genera automáticamente el PDF del menú de casa
    
    Args:
        id_cristina: ID del menú de Cristina (por defecto 1)
        id_marisa: ID del menú de Marisa (por defecto 1)
        archivo_salida: Nombre del archivo de salida
    """
    print("\n" + "="*60)
    print("🏠 GENERADOR DE MENÚ SEMANAL DE CASA")
    print("="*60)
    
    # Cargar menús
    menu_cristina = obtener_menu_por_id("cristina_menus.json", id_cristina)
    menu_marisa = obtener_menu_por_id("marisa_menus.json", id_marisa)
    
    if not menu_cristina or not menu_marisa:
        print("\n❌ No se pudieron cargar los menús")
        return None
    
    print(f"\n📋 Menú seleccionado para Cristina: {menu_cristina['nombre']}")
    print(f"📋 Menú seleccionado para Marisa: {menu_marisa['nombre']}")
    
    # Generar PDF
    return generar_pdf_menu_semanal(menu_cristina, menu_marisa, archivo_salida)


# Script principal
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🏠 SISTEMA DE MENÚS DE CASA")
    print("="*60)
    
    # Generar PDF usando cristina_menu1.json
    print("\n🔄 Generando PDF con cristina_menu1.json...")
    generar_menu_desde_cristina_menu1(
        archivo_salida="menu_semanal_casa.pdf"
    )
    
    print("\n" + "="*60)
    print("✅ Proceso completado")
    print("="*60)
