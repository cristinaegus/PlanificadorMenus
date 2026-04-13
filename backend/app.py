from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional
import ai_menu
import menu_casa
import dieta_pdf_generator
import os

app = FastAPI(title="Menu Generator API", version="1.0.0")

# Configurar CORS para permitir peticiones desde el frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:5175",
        "http://localhost:3000"
    ],  # Vite y otros puertos comunes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class MenuRequest(BaseModel):
    preferencias: Optional[str] = ""
    restricciones: Optional[str] = ""
    tipo_cocina: Optional[str] = "mediterránea"

class SugerenciaRequest(BaseModel):
    dia: str
    tipo_comida: str = "comida"  # 'comida' o 'cena'
    estilo: Optional[str] = "mediterráneo"

class MenuCasaRequest(BaseModel):
    id_cristina: Optional[int] = 1
    id_marisa: Optional[int] = 1

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Página principal con interfaz web para la aplicación"""
    html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Planificador de Menús - OSAKIDETZA</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white; 
            padding: 30px; 
            text-align: center; 
        }
        .header h1 { 
            font-size: 2.5em; 
            margin-bottom: 10px;
            font-weight: 300;
        }
        .header p { 
            font-size: 1.2em; 
            opacity: 0.9;
        }
        .content { 
            padding: 40px; 
        }
        .section { 
            margin-bottom: 40px; 
        }
        .section h2 { 
            color: #2c3e50; 
            border-bottom: 3px solid #3498db; 
            padding-bottom: 10px; 
            margin-bottom: 25px;
            font-size: 1.8em;
        }
        .cards { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 25px; 
            margin-bottom: 30px;
        }
        .card { 
            background: #f8f9fa; 
            border-radius: 10px; 
            padding: 25px; 
            border-left: 5px solid #3498db;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .card:hover { 
            transform: translateY(-5px); 
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        .card h3 { 
            color: #2c3e50; 
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        .card p { 
            color: #7f8c8d; 
            margin-bottom: 15px;
            line-height: 1.6;
        }
        .btn { 
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white; 
            padding: 12px 25px; 
            border: none; 
            border-radius: 25px; 
            cursor: pointer; 
            text-decoration: none; 
            display: inline-block;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
        }
        .btn:hover { 
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
        }
        .btn-success { 
            background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
            box-shadow: 0 4px 15px rgba(39, 174, 96, 0.3);
        }
        .btn-warning { 
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            box-shadow: 0 4px 15px rgba(243, 156, 18, 0.3);
        }
        .status { 
            background: #d5f4e6; 
            color: #27ae60; 
            padding: 15px; 
            border-radius: 10px; 
            margin-bottom: 25px;
            border-left: 5px solid #27ae60;
            font-weight: 500;
        }
        .api-info { 
            background: #e8f4f8; 
            padding: 20px; 
            border-radius: 10px;
            border-left: 5px solid #3498db;
        }
        .footer { 
            background: #2c3e50; 
            color: white; 
            text-align: center; 
            padding: 20px;
            opacity: 0.9;
        }
        @media (max-width: 768px) {
            .header h1 { font-size: 2em; }
            .content { padding: 20px; }
            .cards { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 Planificador de Menús</h1>
            <p>OSAKIDETZA - Sistema de Dietas Médicas</p>
        </div>
        
        <div class="content">
            <div class="status">
                ✅ Servidor activo y funcionando correctamente
            </div>
            
            <div class="section">
                <h2>🏥 Modelos de Dieta Médica</h2>
                <p style="margin-bottom: 20px; color: #7f8c8d;">
                    Dietas de 1000 kcal para cirugía de obesidad - Unidad de Nutrición 2015
                </p>
                <div class="cards">
                    <div class="card">
                        <h3>📄 PDF Completo</h3>
                        <p>Descarga todos los 4 modelos de dieta en un solo documento PDF.</p>
                        <a href="/dieta-modelos/generar-pdf-completo" class="btn btn-success">Descargar Completo</a>
                    </div>
                    <div class="card">
                        <h3>📋 Modelos Individuales</h3>
                        <p>Descarga un modelo específico de dieta.</p>
                        <a href="/dieta-modelos/generar-pdf-modelo/1" class="btn">Modelo 1</a>
                        <a href="/dieta-modelos/generar-pdf-modelo/2" class="btn">Modelo 2</a>
                        <a href="/dieta-modelos/generar-pdf-modelo/3" class="btn">Modelo 3</a>
                        <a href="/dieta-modelos/generar-pdf-modelo/4" class="btn">Modelo 4</a>
                    </div>
                    <div class="card">
                        <h3>📊 Tabla Resumen</h3>
                        <p>Vista resumida de todos los modelos en formato tabla.</p>
                        <a href="/dieta-modelos/generar-resumen" class="btn btn-warning">Ver Resumen</a>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🍽️ Otros Servicios</h2>
                <div class="cards">
                    <div class="card">
                        <h3>🏠 Menú Casa</h3>
                        <p>Genera menús semanales personalizados para el hogar.</p>
                        <button onclick="generarMenuCasa()" class="btn">Generar Menú</button>
                    </div>
                    <div class="card">
                        <h3>🤖 IA Menús</h3>
                        <p>Generación inteligente de menús con preferencias personalizadas.</p>
                        <button onclick="alert('Función disponible via API')" class="btn">Usar IA</button>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🔧 Información de API</h2>
                <div class="api-info">
                    <h3>Endpoints Disponibles:</h3>
                    <ul style="margin: 15px 0; padding-left: 20px; line-height: 1.8;">
                        <li><code>GET /</code> - Esta página principal</li>
                        <li><code>GET /health</code> - Estado del servidor</li>
                        <li><code>GET /dieta-modelos/info</code> - Información JSON de modelos</li>
                        <li><code>POST /generar-menu</code> - Generar menú con IA</li>
                        <li><code>POST /generar-menu-casa</code> - Generar PDF menú casa</li>
                    </ul>
                    <p style="margin-top: 15px;">
                        <a href="/dieta-modelos/info" class="btn">Ver API JSON</a>
                        <a href="/health" class="btn">Check Health</a>
                    </p>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>&copy; 2026 OSAKIDETZA - Unidad de Nutrición | Sistema de Dietas Médicas</p>
        </div>
    </div>
    
    <script>
        function generarMenuCasa() {
            fetch('/generar-menu-casa', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id_cristina: 1, id_marisa: 1})
            })
            .then(response => response.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'menu_semanal_casa.pdf';
                a.click();
                window.URL.revokeObjectURL(url);
            })
            .catch(error => alert('Error: ' + error));
        }
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
def health_check():
    """Endpoint para verificar el estado del servidor"""
    return {"status": "ok", "message": "Servidor funcionando correctamente"}

@app.get("/favicon.ico")
def favicon():
    """Endpoint para manejar la petición del favicon y evitar error 404"""
    return {"message": "No favicon configured"}

@app.post("/generar-menu")
def generar_menu(request: MenuRequest):
    """
    Genera un menú semanal completo usando IA
    
    Body:
    {
        "preferencias": "Me gusta el pescado y las verduras",
        "restricciones": "Sin gluten",
        "tipo_cocina": "mediterránea"
    }
    """
    try:
        menu = ai_menu.generar_menu_semanal(
            preferencias=request.preferencias,
            restricciones=request.restricciones,
            tipo_cocina=request.tipo_cocina
        )
        
        if menu is None:
            raise HTTPException(status_code=500, detail="Error al generar el menú con IA")
        
        return {
            "success": True,
            "menu": menu,
            "parametros": {
                "preferencias": request.preferencias,
                "restricciones": request.restricciones,
                "tipo_cocina": request.tipo_cocina
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar menú: {str(e)}")

@app.post("/sugerir-comida")
def sugerir_comida(request: SugerenciaRequest):
    """
    Genera una sugerencia para una comida específica
    
    Body:
    {
        "dia": "Lunes",
        "tipo_comida": "comida",
        "estilo": "mediterráneo"
    }
    """
    try:
        sugerencia = ai_menu.generar_sugerencia_comida(
            dia=request.dia,
            tipo_comida=request.tipo_comida,
            estilo=request.estilo
        )
        
        if sugerencia is None:
            raise HTTPException(status_code=500, detail="Error al generar sugerencia con IA")
        
        return {
            "success": True,
            "sugerencia": sugerencia,
            "dia": request.dia,
            "tipo_comida": request.tipo_comida
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar sugerencia: {str(e)}")

@app.post("/generar-menu-casa")
def generar_menu_casa(request: MenuCasaRequest):
    """
    Genera un PDF con el menú de casa para Cristina y Marisa
    Usa cristina_menu1.json para Cristina (selección aleatoria de Primeros y Segundos)
    
    Body:
    {
        "id_cristina": 1,
        "id_marisa": 1
    }
    """
    try:
        # Generar el PDF usando cristina_menu1.json
        archivo_pdf = menu_casa.generar_menu_desde_cristina_menu1(
            archivo_salida="menu_semanal_casa.pdf"
        )
        
        if archivo_pdf is None or not os.path.exists(archivo_pdf):
            raise HTTPException(status_code=500, detail="Error al generar el PDF")
        
        # Devolver el PDF como descarga
        return FileResponse(
            path=archivo_pdf,
            media_type="application/pdf",
            filename="menu_semanal_casa.pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar menú casa: {str(e)}")

@app.get("/menus-disponibles")
def menus_disponibles():
    """
    Lista todos los menús disponibles para Cristina y Marisa
    """
    try:
        menus_cristina = menu_casa.listar_menus_disponibles("cristina_menus.json")
        menus_marisa = menu_casa.listar_menus_disponibles("marisa_menus.json")
        
        return {
            "success": True,
            "cristina": menus_cristina,
            "marisa": menus_marisa
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar menús: {str(e)}")

@app.get("/dieta-modelos/generar-pdf-completo")
def generar_pdf_dieta_completo():
    """
    Genera un PDF con todos los modelos de dieta médica (1-4)
    """
    try:
        generator = dieta_pdf_generator.DietaPDFGenerator()
        archivo_pdf = generator.generar_pdf_todos_los_modelos("modelos_dieta_completos.pdf")
        
        if not os.path.exists(archivo_pdf):
            raise HTTPException(status_code=500, detail="Error al generar el PDF completo")
        
        return FileResponse(
            path=archivo_pdf,
            media_type="application/pdf",
            filename="modelos_dieta_completos.pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar PDF completo: {str(e)}")

@app.get("/dieta-modelos/generar-pdf-modelo/{modelo_numero}")
def generar_pdf_dieta_modelo(modelo_numero: int):
    """
    Genera un PDF para un modelo específico de dieta (1, 2, 3, o 4)
    """
    if modelo_numero not in [1, 2, 3, 4]:
        raise HTTPException(status_code=400, detail="El número de modelo debe ser 1, 2, 3 o 4")
    
    try:
        generator = dieta_pdf_generator.DietaPDFGenerator()
        nombre_archivo = f"modelo_dieta_{modelo_numero}.pdf"
        archivo_pdf = generator.generar_pdf_modelo_individual(modelo_numero, nombre_archivo)
        
        if not os.path.exists(archivo_pdf):
            raise HTTPException(status_code=500, detail=f"Error al generar el PDF del modelo {modelo_numero}")
        
        return FileResponse(
            path=archivo_pdf,
            media_type="application/pdf",
            filename=nombre_archivo
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar PDF modelo {modelo_numero}: {str(e)}")

@app.get("/dieta-modelos/generar-resumen")
def generar_resumen_dieta():
    """
    Genera un PDF con tabla resumen de todos los modelos de dieta
    """
    try:
        generator = dieta_pdf_generator.DietaPDFGenerator()
        archivo_pdf = generator.generar_tabla_resumen()
        
        if not os.path.exists(archivo_pdf):
            raise HTTPException(status_code=500, detail="Error al generar el resumen")
        
        return FileResponse(
            path=archivo_pdf,
            media_type="application/pdf",
            filename="resumen_modelos_dieta.pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar resumen: {str(e)}")

@app.get("/dieta-modelos/info")
def obtener_info_modelos():
    """
    Obtiene la información de los modelos de dieta en formato JSON
    """
    try:
        generator = dieta_pdf_generator.DietaPDFGenerator()
        return {
            "success": True,
            "modelos_disponibles": [1, 2, 3, 4],
            "descripcion": "Modelos de dieta de 1000 kcal para cirugía de obesidad",
            "modelos": generator.modelos_dieta
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener información: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
