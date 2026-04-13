"""
Generador de PDFs para los modelos de dieta médica
Osakidetza - Unidad de Nutrición 2015
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.lib.colors import black, blue, red, green
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


class DietaPDFGenerator:
    def __init__(self):
        self.modelos_dieta = self.cargar_modelos_dieta()
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Configura estilos personalizados para el PDF"""
        # Estilo para el título principal
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Estilo para títulos de modelo
        self.model_title_style = ParagraphStyle(
            'ModelTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=15,
            spaceBefore=15,
            textColor=colors.darkgreen
        )
        
        # Estilo para comidas
        self.meal_title_style = ParagraphStyle(
            'MealTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=10,
            textColor=colors.darkred
        )
        
        # Estilo para texto normal
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            spaceBefore=3
        )
        
        # Estilo para ingredientes
        self.ingredient_style = ParagraphStyle(
            'Ingredient',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            spaceAfter=3
        )
    
    def cargar_modelos_dieta(self) -> Dict[str, Any]:
        """Carga los modelos de dieta desde el archivo JSON"""
        try:
            ruta_json = os.path.join(os.path.dirname(__file__), 'modelos_dieta.json')
            with open(ruta_json, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("No se encontró el archivo modelos_dieta.json")
        except json.JSONDecodeError:
            raise ValueError("Error al decodificar el archivo JSON")
    
    def crear_header_footer(self, canvas, doc):
        """Crea header y footer personalizados"""
        canvas.saveState()
        
        # Header
        canvas.setFont('Helvetica-Bold', 12)
        canvas.setFillColor(colors.darkblue)
        canvas.drawString(2*cm, A4[1] - 2*cm, "OSAKIDETZA - Modelos de Dieta")
        canvas.drawString(A4[0] - 8*cm, A4[1] - 2*cm, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
        
        # Footer
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.grey)
        canvas.drawString(2*cm, 2*cm, "Unidad de Nutrición 2015")
        canvas.drawCentredString(A4[0]/2, 2*cm, f"Página {doc.page}")
        
        canvas.restoreState()
    
    def formatear_alimento(self, alimento: Dict[str, Any]) -> str:
        """Formatea la información de un alimento"""
        texto = f"• {alimento['nombre']}"
        
        if 'cantidad' in alimento:
            texto += f": {alimento['cantidad']}"
        
        if 'unidades' in alimento:
            texto += f" ({alimento['unidades']})"
        
        if 'aceite' in alimento:
            texto += f" con {alimento['aceite']}"
        
        if 'opciones' in alimento:
            opciones = ", ".join(alimento['opciones'])
            texto += f" (Opciones: {opciones})"
        
        if 'descripcion' in alimento:
            texto += f" - {alimento['descripcion']}"
        
        return texto
    
    def formatear_plato_complejo(self, alimento: Dict[str, Any]) -> List[str]:
        """Formatea platos que tienen ingredientes múltiples"""
        lines = [f"• {alimento['plato']}:"]
        
        for ingrediente in alimento.get('ingredientes', []):
            ingredient_text = f"  - {ingrediente['nombre']}: {ingrediente['cantidad']}"
            lines.append(ingredient_text)
        
        return lines
    
    def generar_contenido_comida(self, nombre_comida: str, datos_comida: Dict[str, Any]) -> List:
        """Genera el contenido para una comida específica"""
        elementos = []
        
        # Título de la comida
        elementos.append(Paragraph(nombre_comida.upper(), self.meal_title_style))
        
        # Procesar alimentos
        for alimento in datos_comida.get('alimentos', []):
            if 'plato' in alimento:
                # Es un plato complejo con ingredientes
                lineas = self.formatear_plato_complejo(alimento)
                for linea in lineas:
                    elementos.append(Paragraph(linea, self.ingredient_style))
            else:
                # Es un alimento simple
                texto = self.formatear_alimento(alimento)
                elementos.append(Paragraph(texto, self.normal_style))
        
        elementos.append(Spacer(1, 0.3*cm))
        return elementos
    
    def generar_modelo_completo(self, modelo_key: str, modelo_data: Dict[str, Any]) -> List:
        """Genera el contenido completo para un modelo de dieta"""
        elementos = []
        
        # Título del modelo
        titulo_modelo = f"{modelo_key.replace('_', ' ').title()}"
        elementos.append(Paragraph(titulo_modelo, self.model_title_style))
        
        # Descripción
        if 'descripcion' in modelo_data:
            elementos.append(Paragraph(f"<b>Descripción:</b> {modelo_data['descripcion']}", self.normal_style))
            elementos.append(Spacer(1, 0.5*cm))
        
        # Procesar cada comida
        comidas_orden = ['desayuno', 'media_mañana', 'comida', 'merienda', 'cena']
        
        for comida in comidas_orden:
            if comida in modelo_data:
                nombre_comida = comida.replace('_', ' ')
                contenido_comida = self.generar_contenido_comida(nombre_comida, modelo_data[comida])
                elementos.extend(contenido_comida)
        
        elementos.append(PageBreak())
        return elementos
    
    def generar_pdf_todos_los_modelos(self, nombre_archivo: str = "modelos_dieta_completos.pdf") -> str:
        """Genera un PDF con todos los modelos de dieta"""
        ruta_archivo = os.path.join(os.path.dirname(__file__), nombre_archivo)
        
        # Crear documento
        doc = SimpleDocTemplate(
            ruta_archivo,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=3*cm,
            bottomMargin=3*cm
        )
        
        # Contenido del documento
        contenido = []
        
        # Título principal
        contenido.append(Paragraph("MODELOS DE DIETA MÉDICA", self.title_style))
        contenido.append(Paragraph("OSAKIDETZA - UNIDAD DE NUTRICIÓN", self.normal_style))
        contenido.append(Spacer(1, 1*cm))
        
        # Información general
        contenido.append(Paragraph("INSTRUCCIONES GENERALES:", self.meal_title_style))
        
        notas = self.modelos_dieta.get('notas_importantes', [])
        for nota in notas:
            contenido.append(Paragraph(f"• {nota}", self.normal_style))
        
        contenido.append(Spacer(1, 1*cm))
        contenido.append(PageBreak())
        
        # Generar cada modelo
        modelos = self.modelos_dieta.get('modelos_dieta', {})
        
        for modelo_key, modelo_data in modelos.items():
            modelo_contenido = self.generar_modelo_completo(modelo_key, modelo_data)
            contenido.extend(modelo_contenido)
        
        # Construir PDF
        doc.build(contenido, onFirstPage=self.crear_header_footer, onLaterPages=self.crear_header_footer)
        
        return ruta_archivo
    
    def generar_pdf_modelo_individual(self, modelo_numero: int, nombre_archivo: str = None) -> str:
        """Genera un PDF para un modelo específico"""
        if nombre_archivo is None:
            nombre_archivo = f"modelo_dieta_{modelo_numero}.pdf"
        
        ruta_archivo = os.path.join(os.path.dirname(__file__), nombre_archivo)
        modelo_key = f"modelo_{modelo_numero}"
        
        if modelo_key not in self.modelos_dieta.get('modelos_dieta', {}):
            raise ValueError(f"Modelo {modelo_numero} no encontrado")
        
        modelo_data = self.modelos_dieta['modelos_dieta'][modelo_key]
        
        # Crear documento
        doc = SimpleDocTemplate(
            ruta_archivo,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=3*cm,
            bottomMargin=3*cm
        )
        
        # Contenido del documento
        contenido = []
        
        # Título
        contenido.append(Paragraph(f"MODELO DE DIETA {modelo_numero}", self.title_style))
        contenido.append(Paragraph("OSAKIDETZA - UNIDAD DE NUTRICIÓN", self.normal_style))
        contenido.append(Spacer(1, 1*cm))
        
        # Generar contenido del modelo
        modelo_contenido = self.generar_modelo_completo(modelo_key, modelo_data)
        contenido.extend(modelo_contenido[:-1])  # Quitar el PageBreak final
        
        # Construir PDF
        doc.build(contenido, onFirstPage=self.crear_header_footer, onLaterPages=self.crear_header_footer)
        
        return ruta_archivo
    
    def generar_tabla_resumen(self) -> str:
        """Genera un PDF con tabla resumen de todos los modelos"""
        nombre_archivo = "resumen_modelos_dieta.pdf"
        ruta_archivo = os.path.join(os.path.dirname(__file__), nombre_archivo)
        
        # Crear documento
        doc = SimpleDocTemplate(ruta_archivo, pagesize=A4)
        contenido = []
        
        # Título
        contenido.append(Paragraph("RESUMEN DE MODELOS DE DIETA", self.title_style))
        contenido.append(Spacer(1, 1*cm))
        
        # Crear tabla de resumen
        datos_tabla = [['Modelo', 'Descripción', 'Características']]
        
        modelos = self.modelos_dieta.get('modelos_dieta', {})
        for modelo_key, modelo_data in modelos.items():
            modelo_num = modelo_key.replace('modelo_', '')
            descripcion = modelo_data.get('descripcion', 'N/A')
            
            # Contar alimentos aproximadamente
            total_alimentos = 0
            for comida_key, comida_data in modelo_data.items():
                if comida_key != 'descripcion' and isinstance(comida_data, dict):
                    total_alimentos += len(comida_data.get('alimentos', []))
            
            caracteristicas = f"{total_alimentos} elementos alimentarios"
            datos_tabla.append([f"Modelo {modelo_num}", descripcion, caracteristicas])
        
        tabla = Table(datos_tabla, colWidths=[2*cm, 8*cm, 4*cm])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        contenido.append(tabla)
        
        doc.build(contenido, onFirstPage=self.crear_header_footer, onLaterPages=self.crear_header_footer)
        return ruta_archivo


def main():
    """Función principal para testing"""
    generator = DietaPDFGenerator()
    
    try:
        # Generar PDF con todos los modelos
        print("Generando PDF con todos los modelos...")
        archivo_completo = generator.generar_pdf_todos_los_modelos()
        print(f"PDF generado: {archivo_completo}")
        
        # Generar tabla resumen
        print("Generando tabla resumen...")
        archivo_resumen = generator.generar_tabla_resumen()
        print(f"Resumen generado: {archivo_resumen}")
        
        # Generar PDFs individuales para cada modelo
        for i in range(1, 5):
            print(f"Generando PDF para modelo {i}...")
            archivo_individual = generator.generar_pdf_modelo_individual(i)
            print(f"Modelo {i} generado: {archivo_individual}")
        
        print("¡Todos los PDFs generados exitosamente!")
        
    except Exception as e:
        print(f"Error al generar PDFs: {e}")


if __name__ == "__main__":
    main()