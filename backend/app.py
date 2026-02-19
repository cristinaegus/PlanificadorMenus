from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import ai_menu
import menu_casa
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

@app.get("/")
def read_root():
    """Endpoint raíz para verificar que la API está funcionando"""
    return {
        "message": "Menu Generator API - Backend activo",
        "version": "1.0.0",
        "endpoints": {
            "/generar-menu": "POST - Genera un menú semanal completo",
            "/sugerir-comida": "POST - Sugiere un plato específico",
            "/generar-menu-casa": "POST - Genera PDF del menú de casa",
            "/health": "GET - Verifica el estado del servidor"
        }
    }

@app.get("/health")
def health_check():
    """Endpoint para verificar el estado del servidor"""
    return {"status": "ok", "message": "Servidor funcionando correctamente"}

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
