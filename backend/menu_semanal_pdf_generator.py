"""
Generador de PDF para menús semanales - Diets 2
Planificador de Menús - 2026
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import black, blue, red, green, darkblue, darkgreen
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from planificador_semanal_simple import PlanificadorSemanalSimple


class MenuSemanalPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Configura estilos personalizados para el PDF"""
        # Estilo para el título principal
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=darkblue,
            fontName='Helvetica-Bold'
        )
        
        # Estilo para subtítulos
        self.subtitle_style = ParagraphStyle(
            'SubTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=10,
            alignment=TA_CENTER,
            textColor=darkgreen
        )
        
        # Estilo para texto normal
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceBefore=3,
            spaceAfter=3
        )
        
        # Estilo para encabezados de tabla
        self.header_style = ParagraphStyle(
            'HeaderStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_CENTER,
            textColor=colors.white,
            fontName='Helvetica-Bold'
        )
        
        # Estilo para contenido de tabla
        self.cell_style = ParagraphStyle(
            'CellStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_LEFT,
            spaceBefore=2,
            spaceAfter=2
        )
    
    def crear_encabezado_y_pie(self, canvas_obj, doc):
        """Crear encabezado y pie de página para cada página"""
        canvas_obj.saveState()
        
        # === ENCABEZADO ===
        # Línea superior
        canvas_obj.setStrokeColor(darkblue)
        canvas_obj.setLineWidth(2)
        canvas_obj.line(2*cm, A4[1] - 2*cm, A4[0] - 2*cm, A4[1] - 2*cm)
        
        # Título en encabezado
        canvas_obj.setFont("Helvetica-Bold", 12)
        canvas_obj.setFillColor(darkblue)
        width = A4[0]
        text = "PLANIFICADOR SEMANAL - DIETAS 2"
        text_width = canvas_obj.stringWidth(text, "Helvetica-Bold", 12)
        canvas_obj.drawString((width - text_width) / 2, A4[1] - 1.5*cm, text)
        
        # Fecha de generación
        canvas_obj.setFont("Helvetica", 10)
        canvas_obj.setFillColor(black)
        fecha_actual = datetime.now().strftime("%d/%m/%Y - %H:%M")
        canvas_obj.drawRightString(A4[0] - 2*cm, A4[1] - 1.5*cm, f"Generado: {fecha_actual}")
        
        # === PIE DE PÁGINA ===
        # Línea inferior
        canvas_obj.setStrokeColor(colors.grey)
        canvas_obj.setLineWidth(1)
        canvas_obj.line(2*cm, 2*cm, A4[0] - 2*cm, 2*cm)
        
        # Número de página
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor(colors.grey)
        text = f"Página {doc.page}"
        text_width = canvas_obj.stringWidth(text, "Helvetica", 9)
        canvas_obj.drawString((width - text_width) / 2, 1.5*cm, text)
        
        # Información adicional
        info_text = "Planificador de Menús - Sistema Automatizado"
        info_width = canvas_obj.stringWidth(info_text, "Helvetica", 9)
        canvas_obj.drawString((width - info_width) / 2, 1*cm, info_text)
        
        canvas_obj.restoreState()
    
    def formatear_texto_comida(self, comida_info: Dict) -> str:
        """Formatear información de comida para mostrar en tabla"""
        if isinstance(comida_info, dict):
            if 'alimentos' in comida_info:
                # Es un desayuno o snack
                tipo = comida_info.get('tipo', '')
                alimentos = comida_info['alimentos']
                
                texto_alimentos = []
                for alimento in alimentos:
                    nombre = alimento.get('nombre', '')
                    cantidad = alimento.get('cantidad', '')
                    opciones = alimento.get('opciones', [])
                    
                    if opciones:
                        # Formatear opciones
                        opciones_texto = []
                        for opcion in opciones:
                            if isinstance(opcion, dict):
                                tipo_op = opcion.get('tipo', '')
                                cant_op = opcion.get('cantidad', '')
                                if cant_op:
                                    opciones_texto.append(f"{tipo_op} ({cant_op})")
                                else:
                                    opciones_texto.append(tipo_op)
                            else:
                                opciones_texto.append(str(opcion))
                        
                        if cantidad:
                            texto_alimentos.append(f"• {nombre} ({cantidad})")
                        else:
                            texto_alimentos.append(f"• {nombre}")
                        texto_alimentos.append(f"  Opciones: {', '.join(opciones_texto)}")
                    elif cantidad:
                        texto_alimentos.append(f"• {nombre}: {cantidad}")
                    else:
                        texto_alimentos.append(f"• {nombre}")
                
                resultado = f"<b>{tipo}</b><br/>"
                resultado += "<br/>".join(texto_alimentos)
                return resultado
                
            elif 'plato_principal' in comida_info:
                # Es una comida o cena
                plato = comida_info['plato_principal']
                detalles = comida_info.get('detalles', {})
                complementos = comida_info.get('complementos', [])
                
                resultado = f"<b>{plato}</b><br/>"
                
                # Agregar detalles si existen
                if detalles:
                    if isinstance(detalles, dict):
                        detalles_texto = []
                        for key, value in detalles.items():
                            detalles_texto.append(f"{key}: {value}")
                        if detalles_texto:
                            resultado += f"<i>{', '.join(detalles_texto)}</i><br/>"
                    else:
                        resultado += f"<i>{detalles}</i><br/>"
                
                # Agregar complementos
                if complementos:
                    resultado += "<br/><b>Complementos:</b><br/>"
                    for complemento in complementos:
                        nombre = complemento.get('nombre', '')
                        cantidad = complemento.get('cantidad', '')
                        if cantidad:
                            resultado += f"• {nombre}: {cantidad}<br/>"
                        else:
                            resultado += f"• {nombre}<br/>"
                
                return resultado
        
        return str(comida_info)
    
    def crear_tabla_menu(self, menu_semanal: List[Dict]) -> Table:
        """Crear tabla con el menú semanal"""
        # Encabezados de la tabla
        encabezados = ['Día', 'Desayuno', 'Snack/Merienda', 'Comida', 'Cena']
        
        # Datos de la tabla
        datos_tabla = []
        datos_tabla.append([Paragraph(header, self.header_style) for header in encabezados])
        
        for menu_dia in menu_semanal:
            dia = menu_dia['dia']
            desayuno = self.formatear_texto_comida(menu_dia['desayuno'])
            snack = self.formatear_texto_comida(menu_dia['snack'])
            comida = self.formatear_texto_comida(menu_dia['comida'])
            cena = self.formatear_texto_comida(menu_dia['cena'])
            
            # Crear párrafos para cada celda
            fila = [
                Paragraph(f"<b>{dia}</b>", self.cell_style),
                Paragraph(desayuno, self.cell_style),
                Paragraph(snack, self.cell_style),
                Paragraph(comida, self.cell_style),
                Paragraph(cena, self.cell_style)
            ]
            datos_tabla.append(fila)
        
        # Crear tabla
        tabla = Table(datos_tabla, 
                     colWidths=[3*cm, 4.2*cm, 3.8*cm, 4.5*cm, 4.5*cm],
                     repeatRows=1)
        
        # Estilo de la tabla
        tabla.setStyle(TableStyle([
            # Estilo para encabezados
            ('BACKGROUND', (0, 0), (-1, 0), darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Estilo para datos
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Columna días centrada
            ('ALIGN', (1, 1), (-1, -1), 'LEFT'),   # Resto alineado izquierda
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('LEFTPADDING', (0, 1), (-1, -1), 6),
            ('RIGHTPADDING', (0, 1), (-1, -1), 6),
            
            # Bordes
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, darkblue),
            
            # Alternar colores de fila para mejor legibilidad
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        return tabla
    
    def generar_menu_semanal_pdf(self, filename: str = None, modo: str = 'aleatorio') -> str:
        """
        Generar PDF con menú semanal
        
        Args:
            filename: Nombre del archivo PDF (opcional)
            modo: 'aleatorio' o 'secuencial'
        
        Returns:
            Ruta del archivo PDF generado
        """
        # Generar menú usando el planificador
        planificador = PlanificadorSemanalSimple('dietas_2.json')
        
        if not planificador.dietas_data:
            raise Exception("No se pudieron cargar los datos de dietas_2.json")
        
        menu_semanal = planificador.generar_menu_semanal(modo=modo)
        requisitos = planificador.dietas_data.get('requisitos_diarios', {})
        
        # Configurar nombre del archivo
        if filename is None:
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"menu_semanal_dieta2_{fecha_actual}.pdf"
        
        # Crear documento PDF
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=3*cm,
            bottomMargin=2.5*cm,
            title="Menú Semanal - Dietas 2"
        )
        
        # Crear contenido
        contenido = []
        
        # Título principal
        titulo = "MENÚ SEMANAL - DIETAS 2"
        contenido.append(Paragraph(titulo, self.title_style))
        contenido.append(Spacer(1, 0.5*cm))
        
        # Fecha de generación y tipo de menú
        fecha_generacion = datetime.now().strftime("%d de %B de %Y")
        tipo_menu = "Aleatorio" if modo == 'aleatorio' else "Secuencial"
        info_generacion = f"Generado el {fecha_generacion} | Tipo: {tipo_menu}"
        contenido.append(Paragraph(info_generacion, self.subtitle_style))
        contenido.append(Spacer(1, 0.3*cm))
        
        # Requisitos diarios
        if requisitos:
            req_texto = "<b>REQUISITOS DIARIOS:</b><br/>"
            for key, value in requisitos.items():
                nombre = key.replace('_', ' ').title()
                req_texto += f"• <b>{nombre}</b>: {value}<br/>"
            contenido.append(Paragraph(req_texto, self.normal_style))
            contenido.append(Spacer(1, 0.4*cm))
        
        # Tabla del menú semanal
        tabla_menu = self.crear_tabla_menu(menu_semanal)
        contenido.append(tabla_menu)
        
        # Espacio final
        contenido.append(Spacer(1, 1*cm))
        
        # Nota final
        nota_final = """
        <b>NOTAS IMPORTANTES:</b><br/>
        • Este menú ha sido generado automáticamente combinando las opciones disponibles<br/>
        • Todos los complementos indicados deben ser incluidos en cada comida<br/>
        • Respetar las cantidades y requisitos diarios especificados<br/>
        • Para dudas consulte con su especialista en nutrición
        """
        contenido.append(Paragraph(nota_final, self.normal_style))
        
        # Crear PDF con encabezado y pie de página personalizados
        doc.build(contenido, 
                 onFirstPage=self.crear_encabezado_y_pie,
                 onLaterPages=self.crear_encabezado_y_pie)
        
        return filename


# Función de conveniencia para uso directo
def generar_menu_semanal_pdf(filename: str = None, modo: str = 'aleatorio') -> str:
    """
    Función de conveniencia para generar PDF de menú semanal
    
    Args:
        filename: Nombre del archivo PDF (opcional)
        modo: 'aleatorio' o 'secuencial'
    
    Returns:
        Ruta del archivo PDF generado
    """
    generador = MenuSemanalPDFGenerator()
    return generador.generar_menu_semanal_pdf(filename, modo)


# Función de prueba
def main():
    """Función de prueba"""
    print("Generando PDF de menú semanal...")
    try:
        archivo_pdf = generar_menu_semanal_pdf(modo='aleatorio')
        print(f"✅ PDF generado exitosamente: {archivo_pdf}")
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")


if __name__ == "__main__":
    main()